from django.conf import settings
from django.db import models
from django.utils import timezone


class Broadcast(models.Model):
    class Audience(models.TextChoices):
        ALL = "all", "All Students"
        FINAL_YEAR = "final_year", "Final Year Students"
        COMPANIES = "companies", "Companies"

    title = models.CharField(max_length=180)
    message = models.TextField()
    audience = models.CharField(max_length=20, choices=Audience.choices, default=Audience.ALL)
    publish_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publish_at"]

    def __str__(self):
        return self.title
