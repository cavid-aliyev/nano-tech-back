# Generated by Django 4.2.11 on 2024-07-10 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0003_customuser_full_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="full_name",
        ),
    ]
