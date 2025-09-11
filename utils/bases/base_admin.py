from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class BaseAdmin(admin.ModelAdmin):
    def soft_delete_selected(self, request, queryset):
        count = 0
        for item in queryset:
            item.soft_delete()
            count += 1
        self.message_user(request, _("%(count)d item is_deleted.") % {"count": count})

    soft_delete_selected.short_description = _(
        "Delete selected %(verbose_name_plural)s"
    )

    def soft_undelete_selected(self, request, queryset):
        count = 0
        for item in queryset:
            item.soft_undelete()
            count += 1
        self.message_user(request, _("%(count)d item restored.") % {"count": count})

    soft_undelete_selected.short_description = _("Restore selected")

    def activate_selected(self, request, queryset):
        count = 0
        for item in queryset:
            item.activate(request.user)
            count += 1
        self.message_user(request, _("%(count)d item activated.") % {"count": count})

    activate_selected.short_description = _("Activate selected")

    def deactivate_selected(self, request, queryset):
        count = 0
        for item in queryset:
            item.deactivate(request.user)
            count += 1
        self.message_user(request, _("%(count)d item deactivated.") % {"count": count})

    deactivate_selected.short_description = _("Deactivate selected")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    actions = [
        "soft_delete_selected",
        "soft_undelete_selected",
        "activate_selected",
        "deactivate_selected",
    ]
