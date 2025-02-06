from django.contrib import admin


from products.models import ProductCategory, Product, Basket

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'category')
    # readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('name',)


# для отображения корзины каждого пользователя в админке, можно вложить корзину в админку пользователя, используя admin.TabularInline
# и импортировав этот класс в админке User
class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
