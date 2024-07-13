from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Category

@receiver(m2m_changed, sender=Category.brands.through)
def update_parent_category_brands(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove']:
        if instance.parent_category:  # If the instance is a subcategory
            print('Subcategory---------')
            # Get the parent category
            parent_category = instance.parent_category
            # Update the parent category's brands to include all brands from its subcategories
            for brand in instance.brands.all():
                parent_category.brands.add(brand)
            # Ensure to save the parent category
            parent_category.save()
