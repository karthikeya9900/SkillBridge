from django.contrib import admin

from .models import CompanyProfile


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "industry", "is_approved", "created_at")
    list_filter = ("industry", "is_approved")
    search_fields = ("name", "user__email")
