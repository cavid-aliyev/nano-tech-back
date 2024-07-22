from django.db import models
from django.db.models.fields.files import ImageField
from django.utils.text import slugify
from datetime import datetime
from django.utils import timezone
from decimal import Decimal
# from django.utils.translation import gettext_lazy as _


from utils import DateAbstractModel



class Brand(models.Model):
    title = models.CharField(max_length=200)
    image = ImageField(upload_to='brand_image', null=True)
    is_active = models.BooleanField(default=True)
   

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["id"]


class TopBrand(DateAbstractModel):
    image = ImageField(upload_to='brand_image', null=True)
    is_active = models.BooleanField(default=True)
   

    def __str__(self):
        return f"{self.id}'s top brand obj"
    
    class Meta:
        verbose_name = "Top Brand"
        verbose_name_plural = "Top Brands"
        ordering = ["-created_at"]


class ProductTag(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
   

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["id"]


class Category(DateAbstractModel):
    title = models.CharField(max_length=50)
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name='child_cats', on_delete=models.CASCADE)
    brands = models.ManyToManyField(Brand)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)  # New field for the category icon
   
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = "Category"
        ordering = ['id']

    def __str__(self) -> str:
        return self.title
    
    def get_parent(self) -> str:
        if self.parent_category:
            return self.parent_category.title
        else:
            return "Main Category"
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + '-' + str(datetime.now().timestamp()).replace('.', '')
        super(Category, self).save(*args, **kwargs)
        self.update_parent_brands()

    def update_parent_brands(self):
        if self.parent_category:
            for brand in self.brands.all():
                self.parent_category.brands.add(brand)
            self.parent_category.save()


class ProductColor(models.Model):
    title = models.CharField(max_length=200)
    hex_code = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"
        ordering = ["id"]
    

class ProductSize(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
        ordering = ["id"]
    

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
    
    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"
        ordering = ["id"]


class ProductDetailType(DateAbstractModel):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Product Detail Type"
        verbose_name_plural = "Product Detail Types"
        ordering = ["id"]

    
    def __str__(self):
        return self.name
    

class ProductVersion(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='product_versions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_versions', null=True, blank=True)
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
        ordering = ["created_at"]

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
    

class ProductDetail(DateAbstractModel):
    product = models.ForeignKey(ProductVersion, related_name='details', on_delete=models.CASCADE)
    detail_type = models.ForeignKey(ProductDetailType, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.product.title} - {self.detail_type.name}: {self.value}'
    

    class Meta:
        verbose_name = "Product Detail"
        verbose_name_plural = "Product Details"
        ordering = ["-created_at"]


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
    
    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ["-created_at"]
    



