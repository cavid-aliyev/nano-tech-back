# Generated by Django 4.2.11 on 2024-07-22 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "product",
            "0015_productdetailtype_name_az_productdetailtype_name_en_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productdetail",
            name="memory",
        ),
        migrations.RemoveField(
            model_name="productdetail",
            name="operating_system",
        ),
        migrations.RemoveField(
            model_name="productdetail",
            name="processor",
        ),
        migrations.RemoveField(
            model_name="productdetail",
            name="ram",
        ),
        migrations.RemoveField(
            model_name="productdetail",
            name="screen_diagonal",
        ),
        migrations.RemoveField(
            model_name="productdetail",
            name="screen_indicators",
        ),
        migrations.RemoveField(
            model_name="productdetail",
            name="video_card",
        ),
        migrations.AddField(
            model_name="productdetail",
            name="detail_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="product.productdetailtype",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="productdetail",
            name="value",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="productdetail",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="details",
                to="product.productversion",
            ),
        ),
    ]
