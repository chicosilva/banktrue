# Generated by Django 2.2 on 2019-06-07 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0005_auto_20190607_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='number',
            field=models.CharField(editable=False, max_length=100, unique=True),
        ),
    ]