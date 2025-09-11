from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from utils.model_mixins import AllMixinInheritedMixin


class UserAddress(AllMixinInheritedMixin):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="addresses")
    country = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    phone_number = PhoneNumberField(blank=True, null=True)

    class Meta:
        ordering = ["id", "-created_at", "-updated_at"]
