from django.contrib import admin

from .models import Application, PlacementDrive


@admin.register(PlacementDrive)
class PlacementDriveAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "deadline", "is_active", "min_cgpa")
    list_filter = ("is_active", "deadline", "company")
    search_fields = ("title", "company__name", "eligible_branches")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "drive", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("student__user__username", "drive__title")
