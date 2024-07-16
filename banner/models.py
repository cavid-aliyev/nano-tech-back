from django.db import models
# from django.db.models.fields.files import ImageField

# Create your models here.

from utils import DateAbstractModel


class Banner(DateAbstractModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Home Page Banner'
        verbose_name_plural = 'Home Page Banner'
        ordering = ['-created_at']

