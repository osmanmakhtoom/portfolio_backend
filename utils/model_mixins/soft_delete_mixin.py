from django.db import models
from django.utils import timezone


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.updated_at = timezone.now()
        self.save()

    def soft_undelete(self):
        self.is_deleted = False
        self.deleted_at = None
        self.updated_at = timezone.now()
        self.save()

    class Meta:
        abstract = True
