# Generated by Django 4.2.11 on 2024-07-22 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0016_remove_productdetail_memory_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productdetail",
            name="value_az",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="productdetail",
            name="value_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="productdetail",
            name="value_ru",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
