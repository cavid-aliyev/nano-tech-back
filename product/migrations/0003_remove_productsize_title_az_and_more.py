# Generated by Django 4.2.11 on 2024-07-05 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_productcolor_title_az_productcolor_title_en_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productsize",
            name="title_az",
        ),
        migrations.RemoveField(
            model_name="productsize",
            name="title_en",
        ),
        migrations.RemoveField(
            model_name="productsize",
            name="title_ru",
        ),
    ]
