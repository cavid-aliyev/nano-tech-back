# Generated by Django 4.2.11 on 2024-06-28 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="description_az",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="description_en",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="description_ru",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="name_az",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="name_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="name_ru",
            field=models.CharField(max_length=255, null=True),
        ),
    ]