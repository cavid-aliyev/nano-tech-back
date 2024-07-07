from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        if hasattr(obj, 'profile'):
            obj.profile.delete()
        super().delete_model(request, obj)
admin.site.register(User, CustomUserAdmin)

# Register your models here.
# admin.site.register(User)