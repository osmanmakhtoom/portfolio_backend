from django.db import models

import ulid


class UlidMixin(models.Model):
    id = models.CharField(
        max_length=64,
        unique=True,
        primary_key=True,
        default=ulid.new,
        db_index=True,
        help_text="Unique ID",
    )

    class Meta:
        abstract = True
