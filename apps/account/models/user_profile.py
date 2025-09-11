from django.db import models

from utils.model_mixins import AllMixinInheritedMixin


class UserProfile(AllMixinInheritedMixin):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    cover_photo = models.ImageField(upload_to="covers/", blank=True, null=True)
    social_links = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        ordering = ["id", "-created_at", "-updated_at"]
