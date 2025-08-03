from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.conf import settings

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        RECRUITER = 'RECRUITER', _('Recruiter')
        JOB_SEEKER = 'JOB_SEEKER', _('Job Seeker')

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.JOB_SEEKER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.role:
            self.role = self.role.upper()
        super().save(*args, **kwargs)

    objects = UserManager()

    def __str__(self):
        return self.email


def user_directory_path(instance, filename):
    # Files will be uploaded to MEDIA_ROOT/profile/user_<id>/<filename>
    return f'profile/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    profile_picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    linkedin = models.URLField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)  # or ManyToMany to a Skill model
    portfolio = models.URLField(blank=True)
    profile_completed = models.BooleanField(default=False)

    def check_completion(self):
        required_fields = [self.phone_number, self.country, self.gender]
        self.profile_completed = all(required_fields)
        self.save()


class RoleRequest(models.Model):
    ROLE_CHOICES = [
        ('RECRUITER', 'Recruiter'),
        ('ADMIN', 'Admin'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requested_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    reason = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} requests {self.requested_role}"
