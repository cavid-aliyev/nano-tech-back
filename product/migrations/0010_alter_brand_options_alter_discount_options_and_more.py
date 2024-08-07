# Generated by Django 4.2.11 on 2024-07-11 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0009_alter_productdetail_product"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="brand",
            options={
                "ordering": ["id"],
                "verbose_name": "Brand",
                "verbose_name_plural": "Brands",
            },
        ),
        migrations.AlterModelOptions(
            name="discount",
            options={
                "ordering": ["id"],
                "verbose_name": "Discount",
                "verbose_name_plural": "Discounts",
            },
        ),
        migrations.AlterModelOptions(
            name="productcategory",
            options={
                "ordering": ["id"],
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.AlterModelOptions(
            name="productcolor",
            options={
                "ordering": ["id"],
                "verbose_name": "Color",
                "verbose_name_plural": "Colors",
            },
        ),
        migrations.AlterModelOptions(
            name="productsize",
            options={
                "ordering": ["id"],
                "verbose_name": "Size",
                "verbose_name_plural": "Sizes",
            },
        ),
        migrations.AlterModelOptions(
            name="productsubcategory",
            options={
                "ordering": ["id"],
                "verbose_name": "Subcategory",
                "verbose_name_plural": "Subcategories",
            },
        ),
        migrations.AlterModelOptions(
            name="producttag",
            options={
                "ordering": ["id"],
                "verbose_name": "Tag",
                "verbose_name_plural": "Tags",
            },
        ),
        migrations.AlterModelOptions(
            name="productversionimage",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Product Image",
                "verbose_name_plural": "Product Images",
            },
        ),
        migrations.AlterModelOptions(
            name="slider",
            options={
                "ordering": ["id"],
                "verbose_name": "Slider",
                "verbose_name_plural": "Sliders",
            },
        ),
        migrations.AlterModelOptions(
            name="topbrand",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Top Brand",
                "verbose_name_plural": "Top Brands",
            },
        ),
    ]
