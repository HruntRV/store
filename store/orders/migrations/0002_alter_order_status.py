# Generated by Django 5.1.4 on 2025-02-07 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Створений'), (1, 'Оплачений'), (2, 'В дорозі'), (3, 'Доставлений')], default=0),
        ),
    ]
