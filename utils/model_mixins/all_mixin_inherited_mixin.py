from utils.model_mixins import (
    IsActiveMixin,
    TimestampedMixin,
    UlidMixin,
    SoftDeleteMixin,
    VerificationMixin,
)


class AllMixinInheritedMixin(
    IsActiveMixin, TimestampedMixin, UlidMixin, SoftDeleteMixin, VerificationMixin
):
    class Meta:
        abstract = True
