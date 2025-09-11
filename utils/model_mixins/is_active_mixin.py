from django.conf import settings
from django.db import models


class IsActiveMixin(models.Model):
    is_active = models.BooleanField(default=True, db_index=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_activated",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def activate(self, user=None):
        self.is_active = True
        self.changed_by = user
        self.save()

    def deactivate(self, user=None):
        self.is_active = False
        self.changed_by = user
        self.save()
