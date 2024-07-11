from django.urls import path

from blog.apis import *


urlpatterns = [
    path("blogs/", BlogApiView.as_view(), name="blog-get-create-put-delete"),
    path('blog/<int:pk>/', blog_detail_view, name='blog_detail'),
    path("blog/<int:pk>/", DeleteBlogApiView.as_view(), name="blog-delete"),
]
