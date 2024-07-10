from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class CustomUserAdmin(admin.ModelAdmin):
    # model = User
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ('full_name',)}),
    # )
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     (None, {'fields': ('full_name',)}),
    # )

    def delete_model(self, request, obj):
        if hasattr(obj, 'profile'):
            obj.profile.delete()
        super().delete_model(request, obj)

# admin.site.register(User, CustomUserAdmin)

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "get_full_name", "email"]
    list_display_links = ['id', 'get_full_name', "email"] 
    # list_editable = ["is_active"]
    # list_per_page = 10


    # def get_photo(self, obj):
    #     if obj.image:
    #         img_str = f"<img src='{obj.image.url}' width='100px'>"
    #     return format_html(img_str)

# Register your models here.
# admin.site.register(User)