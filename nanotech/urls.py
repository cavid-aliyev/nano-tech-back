"""
URL configuration for nanotech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from product.api.views import set_language_api, get_language_options_api

schema_view = get_schema_view(
    openapi.Info(
        title="Nanotech API",
        default_version="v1",
        description="API for Nanotech",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


app_name="api"
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('set_language/', set_language_api, name='set_language_api'),
    # path('language_options/', get_language_options_api, name='get_language_options_api'),

    path('product-api/', include('product.api.urls')),

    path('account-api/', include('account.api.urls')),
    # path('api/account/', include('allauth.urls')),
    # path('social-auth/', include('social_django.urls', namespace='social')),

    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("blog-api/", include("blog.urls.apis")),
    path("social-media-api/", include("social_media.api.urls")),
    path("cart-api/", include('checkout.api.urls')),

    # re_path(r'^rosetta/', include('rosetta.urls')),
    
    # Swagger
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api-docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    # path('i18n/', include('django_translation_flags.urls')),

    # path('api/', include('product.api.urls')),

)
