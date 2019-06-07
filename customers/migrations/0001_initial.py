# Generated by Django 2.2 on 2019-06-06 19:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('canceled_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('taxid', models.CharField(max_length=25, unique=True)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('cellphone', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=200)),
                ('token', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
