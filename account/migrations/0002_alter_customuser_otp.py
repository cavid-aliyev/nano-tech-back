# Generated by Django 4.2.11 on 2024-06-21 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="otp",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]