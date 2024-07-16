from django.db import models
from django.db.models.fields.files import ImageField

# Create your models here.

from utils import DateAbstractModel


class Slider(DateAbstractModel):
    slider_image = ImageField(upload_to='slider_image')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}'s slider obj"

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"
        ordering = ["id"]
