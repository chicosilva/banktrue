# Generated by Django 2.2 on 2019-06-07 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0006_auto_20190607_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='installment',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]