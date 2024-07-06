from django.contrib import admin

from .models import *
from .forms import *

# admin.site.register(InstagramProfile)
# admin.site.register(FacebookProfile)
# admin.site.register(WhatsappProfile)
# admin.site.register(TelegramProfile)
# admin.site.register(TiktokProfile)


class InstagramProfileAdmin(admin.ModelAdmin):
    form = InstagramProfileForm

admin.site.register(InstagramProfile, InstagramProfileAdmin)

class FacebookProfileAdmin(admin.ModelAdmin):
    form = FacebookProfileForm

admin.site.register(FacebookProfile, FacebookProfileAdmin)

class WhatsappProfileAdmin(admin.ModelAdmin):
    form = WhatsappProfileForm 

admin.site.register(WhatsappProfile, WhatsappProfileAdmin)

class TelegramProfileAdmin(admin.ModelAdmin):
    form = TelegramProfileForm

admin.site.register(TelegramProfile, TelegramProfileAdmin)

class TiktokProfileAdmin(admin.ModelAdmin):
    form = TiktokProfileForm

admin.site.register(TiktokProfile, TiktokProfileAdmin)

