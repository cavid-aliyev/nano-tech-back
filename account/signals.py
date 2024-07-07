from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(pre_delete, sender=User)
def cleanup_related_data(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.delete()
    
