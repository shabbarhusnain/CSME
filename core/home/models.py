from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
User=get_user_model()
class DeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
# Create your models here.

class UserProfile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    image=models.ImageField(upload_to='profile')
    is_deleted=models.BooleanField(default=False)
    objects=DeleteManager()
    admin_objects=models.Manager()
    def __str__(self) -> str:
        return self.name
@receiver(post_save,sender=UserProfile)
def call_api(sender, instance, **kwargs):
        ProfileHistory.objects.create(
            user_create_by=instance.name, email=instance.email
        )
class ProfileHistory(models.Model):
    user_create_by=models.CharField(max_length=100)
    email=models.EmailField(null=True)
    date_of_creation=models.DateField(auto_now_add=True)


