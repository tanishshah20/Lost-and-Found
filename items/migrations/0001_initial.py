# Generated by Django 5.2 on 2025-04-17 19:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Item Categories',
            },
        ),
        migrations.CreateModel(
            name='FoundItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='item_images/')),
                ('date_found', models.DateField()),
                ('is_claimed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_posted'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LostItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='item_images/')),
                ('date_lost', models.DateField()),
                ('is_found', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_posted'],
                'abstract': False,
            },
        ),
    ]
