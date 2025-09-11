from django.db import models
from django.utils import timezone


class VerificationMixin(models.Model):
    is_verified = models.BooleanField(default=False, db_index=True)
    verified_by = models.ForeignKey(
        "account.User",
        on_delete=models.SET_NULL,
        related_name="verified_%(class)s_set",
        null=True,
        blank=True,
    )
    verified_at = models.DateTimeField(blank=True, null=True)

    def verify(self, user):
        if not self.is_verified:
            self.is_verified = True
            self.verified_by = user
            self.verified_at = timezone.now()
            self.save()

    def unverify(self):
        if self.is_verified:
            self.is_verified = False
            self.verified_by = None
            self.verified_at = None
            self.save()

    class Meta:
        abstract = True
