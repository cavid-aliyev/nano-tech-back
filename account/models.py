from django.db import models
from django.db.models.fields.files import ImageField
from django.contrib.auth.models import AbstractUser





# Create your models here.


class CustomUser(AbstractUser):
    otp = models.CharField(max_length=6, blank=True, null=True)
    # username = models.CharField(max_length=100, unique=True)
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    # ip_address = models.GenericIPAddressField(null=True, blank=True)
    # phone_number = models.CharField(max_length=20, blank=True)
    # email = models.EmailField(max_length=100)
    # bio = models.TextField(blank=True,default='salam')
    # profile_image = ImageField(upload_to='profile_images/', null=True, blank=True)
    # address = models.CharField(max_length=255, blank=True)
    # city = models.CharField(max_length=100, blank=True)
    # position = models.CharField(max_length=100, blank=True,default='mudur')

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email'] 

    # def __str__(self):
    #     return self.username
    

    # class Meta:
    #     db_table = 'account_customuser'