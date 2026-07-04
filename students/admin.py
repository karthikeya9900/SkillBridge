from django.contrib import admin

from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "branch", "year", "cgpa", "is_verified")
    list_filter = ("department", "branch", "year", "is_verified")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email")
