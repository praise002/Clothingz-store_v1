# Generated by Django 5.1 on 2024-12-02 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='user',
            new_name='profile',
        ),
    ]
