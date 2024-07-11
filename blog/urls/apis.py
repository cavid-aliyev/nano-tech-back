from django.urls import path

from blog.apis import *


urlpatterns = [
    path("crud/", BlogApiView.as_view(), name="blog-get-create-put-delete"),
    path('blog/<int:pk>/', blog_detail_view, name='blog_detail'),
    path("crud/<int:pk>/", DeleteBlogApiView.as_view(), name="blog-delete"),
]
