from django.conf import settings
from django.db import models


class CompanyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_profile")
    name = models.CharField(max_length=180)
    industry = models.CharField(max_length=120, blank=True)
    website = models.URLField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="companies/logos/", blank=True)
    receive_email_notifications = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
