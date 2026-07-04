from django.contrib import admin

from .models import Broadcast


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ("title", "audience", "publish_at", "is_active")
    list_filter = ("audience", "is_active", "publish_at")
    search_fields = ("title", "message")
