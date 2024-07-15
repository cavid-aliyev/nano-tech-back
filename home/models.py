from django.db import models
from django.db.models.fields.files import ImageField

# Create your models here.

from utils import DateAbstractModel


class Banner(DateAbstractModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Home Page Banner'
        verbose_name_plural = 'Home Page Banner'
        ordering = ['-created_at']

    def __str__(self):
        return self.title



class Slider(DateAbstractModel):
    slider_image = ImageField(upload_to='slider_image')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}'s slider obj"

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"
        ordering = ["id"]
