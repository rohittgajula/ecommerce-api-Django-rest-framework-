# Generated by Django 5.1 on 2024-08-28 08:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_product_brand_product_category_product_created_at_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="rating",
            new_name="ratings",
        ),
    ]
