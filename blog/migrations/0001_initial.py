# Generated by Django 4.2.11 on 2024-06-24 19:10

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Blog",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("title_en", models.CharField(max_length=255, null=True)),
                ("title_az", models.CharField(max_length=255, null=True)),
                ("title_ru", models.CharField(max_length=255, null=True)),
                ("content", ckeditor.fields.RichTextField()),
                ("content_en", ckeditor.fields.RichTextField(null=True)),
                ("content_az", ckeditor.fields.RichTextField(null=True)),
                ("content_ru", ckeditor.fields.RichTextField(null=True)),
                ("review_count", models.IntegerField(default=0)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.category"
                    ),
                ),
            ],
            options={
                "verbose_name": "Blog",
                "verbose_name_plural": "Blogs",
                "ordering": ["-created_at"],
            },
        ),
    ]
