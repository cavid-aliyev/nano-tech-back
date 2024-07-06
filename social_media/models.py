from django.db import models


class InstagramProfile(models.Model):
    link = models.URLField()

    def __str__(self):
        return self.link
    
    def save(self, *args, **kwargs):
        if not self.link.startswith("https://www.instagram.com/") and not self.link.startswith("https://instagram.com/"):
            raise ValueError("Invalid Instagram link. It must start with 'https://www.instagram.com/' or 'https://instagram.com/'")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Instagram Profile"
        


class FacebookProfile(models.Model):
    link = models.URLField()

    def __str__(self):
        return self.link
    
    def save(self, *args, **kwargs):
        if not self.link.startswith("https://www.facebook.com/") and not self.link.startswith("https://facebook.com/"):
            raise ValueError("Invalid Facebook link. It must start with 'https://www.facebook.com/' or 'https://facebook.com/'")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Facebook Profile"

class WhatsappProfile(models.Model):
    link = models.URLField()

    def __str__(self):
        return self.link
    
    def save(self, *args, **kwargs):
        if not self.link.startswith("https://wa.me/"):
            raise ValueError("Invalid Whatsapp link. It must start with 'https://wa.me/'")
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Whatsapp Profile"

class TelegramProfile(models.Model):
    link = models.URLField()

    def __str__(self):
        return self.link

    def save(self, *args, **kwargs):
        if not self.link.startswith("https://t.me/") and not self.link.startswith("https://telegram.me/"):
            raise ValueError("Invalid Telegram link. It must start with 'https://t.me/' or 'https://telegram.me/'")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Telegram Profile"

class TiktokProfile(models.Model):
    link = models.URLField()

    def __str__(self):
        return self.link

    def save(self, *args, **kwargs):
        if not self.link.startswith("https://www.tiktok.com/") and not self.link.startswith("https://tiktok.com/"):
            raise ValueError("Invalid Tiktok link. It must start with 'https://www.tiktok.com/' or 'https://tiktok.com/'")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tiktok Profile"