from django.contrib import admin

from .models import Organization, BotSettings

# Register your models here.

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
@admin.register(BotSettings)
class BotSettingsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


