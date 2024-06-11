from django.db import models
from utils import DateAbstractModel
from ckeditor.fields import RichTextField

from .category import Category


class Blog(DateAbstractModel):
    title = models.CharField(max_length=255)
    content = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    review_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ["-created_at"]
