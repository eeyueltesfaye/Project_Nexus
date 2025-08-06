from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, CustomUser, RoleRequest

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=RoleRequest)
def apply_role_change(sender, instance, **kwargs):
    if instance.approved and instance.reviewed:
        user = instance.user
        if user.role != instance.requested_role:
            user.role = instance.requested_role
            user.save()
