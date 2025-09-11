from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.account.managers.user_manager import CustomUserManager
from apps.account.models.user_profile import UserProfile
from utils.model_mixins import UlidMixin, SoftDeleteMixin, TimestampedMixin


class User(UlidMixin, AbstractUser, SoftDeleteMixin, TimestampedMixin):
    class GENDER(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    phone_number = PhoneNumberField(region="IR", unique=True, db_index=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER.choices,
        default=GENDER.MALE,
    )
    username = models.CharField(max_length=255, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"

    class Meta:
        ordering = ("id", "-date_joined")

    def __str__(self):
        return str(self.phone_number)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, "userprofile"):
            UserProfile.objects.create(user=self)
