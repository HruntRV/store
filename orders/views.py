from django.views.generic.edit import CreateView
from common.views import TitleMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from orders.forms import OrderForm
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from http import HTTPStatus
from django.views.decorators.csrf import csrf_exempt
import stripe

from products.models import Basket
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    title = 'Дякуємо за замовлення'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    print("Webhook received")
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event['type'] in ['checkout.session.completed', 'checkout.session.async_payment_succeeded']:
        session = event['data']['object']
        session_id = session.get('id')  # Get Stripe session ID

        try:
            order_id = session.get("metadata", {}).get("order_id")
            order = Order.objects.get(id=order_id)
            fulfill_checkout(order)  # Process the order after payment
        except Order.DoesNotExist:
            return HttpResponse(status=400)  # Order not found

    return HttpResponse(status=200)


def fulfill_checkout(order):
    print(order)
    order.update_after_payment()


