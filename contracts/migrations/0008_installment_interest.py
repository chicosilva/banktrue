# Generated by Django 2.2 on 2019-06-07 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0007_installment_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='installment',
            name='interest',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]