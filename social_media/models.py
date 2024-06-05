from django.db import models


class InstagramProfile(models.Model):
    link = models.URLField()

    def __str__(self):
        return self.link
    
    def save(self, *args, **kwargs):
        if not self.link.startswith("https://www.instagram.com/"):
            raise ValueError("Invalid Instagram link")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Instagram Profile"
        


class FacebookProfile(models.Model):
    link = models.URLField()

    def __str__(self):
        return self.link
    
    def save(self, *args, **kwargs):
        if not self.link.startswith("https://www.facebook.com/"):
            raise ValueError("Invalid Facebook link")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Facebook Profile"

class WhatsappProfile(models.Model):
    link = models.URLField()

    def __str__(self):
        return self.number
    
    def save(self, *args, **kwargs):
        if not self.link.startswith("https://wa.me/"):
            raise ValueError("Invalid Whatsapp link")
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Whatsapp Profile"

class TelegramProfile(models.Model):
    link = models.URLField()

    def __str__(self):
        return self.link

    def save(self, *args, **kwargs):
        if not self.link.startswith("https://t.me/"):
            raise ValueError("Invalid Telegram link")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Telegram Profile"

class TiktokProfile(models.Model):
    link = models.URLField()

    def __str__(self):
        return self.link

    def save(self, *args, **kwargs):
        if not self.link.startswith("https://www.tiktok.com/"):
            raise ValueError("Invalid Tiktok link")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tiktok Profile"