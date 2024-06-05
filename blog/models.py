from django.db import models
from utils import DateAbstractModel
from django_ckeditor_5.fields import CKEditor5Field



class Blog(DateAbstractModel):
    title = models.CharField(max_length=255)
    content = CKEditor5Field('Content')
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    review_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ["-created_at"]


class Category(DateAbstractModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]