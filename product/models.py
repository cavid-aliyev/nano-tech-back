from django.db import models
from django.db.models.fields.files import ImageField
from django.utils.text import slugify
from datetime import datetime
from django.utils import timezone
from decimal import Decimal
# from django.utils.translation import gettext_lazy as _


from utils import DateAbstractModel


class Slider(DateAbstractModel):
    slider_image = ImageField(upload_to='slider_image')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}'s slider obj"

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Slider"
        ordering = ["id"]


class Brand(models.Model):
    title = models.CharField(max_length=200)
    image = ImageField(upload_to='brand_image', null=True)
    is_active = models.BooleanField(default=True)
   

    def __str__(self):
        return self.title

class TopBrand(DateAbstractModel):
    image = ImageField(upload_to='brand_image', null=True)
    is_active = models.BooleanField(default=True)
   

    def __str__(self):
        return f"{self.id}'s top brand obj"


class ProductTag(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
   

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
  

    def __str__(self):
        return self.title
    
class ProductSubcategory(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='subcategories')
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    


# class Product(models.Model):
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE,related_name='product_brand')
#     title = models.CharField(max_length=200)
#     subcategory = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE,related_name='product_category')
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title


class ProductColor(models.Model):
    title = models.CharField(max_length=200)
    hex_code = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class ProductSize(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    

class Discount(models.Model):
    title = models.CharField(max_length=200)
    DISCOUNT_TYPE_CHOICES = (
        ('percent', 'Percentage'),
        ('amount', 'Amount'),
    )
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.title


class ProductVersion(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='product_versions')
    subcategory = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE, related_name='product_versions')
    color = models.ManyToManyField(ProductColor, blank=True)
    size = models.ManyToManyField(ProductSize, blank=True)
    title = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.IntegerField()
    sales = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(ProductTag, blank=True, related_name='product_tags')
    description = models.TextField(blank=True)
    cover_image = ImageField(upload_to='product_version_image')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True, max_length=200)
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    def get_discounted_price(self):
        # today = timezone.now().date()
        special_discount = self.special_discounts.filter(is_active=True).first()

        if special_discount:
            if special_discount.discount_type == 'percent':
                discounted_price = self.price - (self.price * (special_discount.value / 100))
            elif special_discount.discount_type == 'amount':
                discounted_price = self.price - special_discount.value
        elif self.discount:
            if self.discount.discount_type == 'percent':
                discounted_price = self.price - (self.price * (self.discount.value / 100))
            elif self.discount.discount_type == 'amount':
                discounted_price = self.price - self.discount.value
        else:
            discounted_price = self.price
        
        return round(Decimal(discounted_price), 2)
    
    def has_active_special_discount(self):
        return self.special_discounts.filter(is_active=True).exists()
    
    
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        self.slug = self.slug + '-' + str(datetime.now().timestamp()).replace('.','')
        return super(ProductVersion,self).save()
    

class SpecialDiscount(DateAbstractModel):
    product_version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE, related_name='special_discounts')
    discount_type = models.CharField(max_length=10, choices=Discount.DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(decimal_places=2, max_digits=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Special Discount on {self.created_at} for {self.product_version}"
    
    class Meta:
        verbose_name = "Daily Special Discount"
        verbose_name_plural = "Daily Special Discounts"
        ordering = ["-created_at"]
    


class ProductVersionImage(models.Model):
    product_version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE,related_name="images")
    image = ImageField(upload_to='product_version_images')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product_version)
    



