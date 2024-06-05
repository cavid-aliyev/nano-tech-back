from django.urls import path

from .views import *


urlpatterns = [
    path("crud/", BlogApiView.as_view(), name="blog-get-create-put-delete"),
    path("crud/<int:pk>/", DeleteBlogApiView.as_view(), name="blog-delete"),
    path("category/", CategoryApiView.as_view(), name="category-get-create"),
]