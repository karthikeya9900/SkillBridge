from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from companies.models import CompanyProfile
from students.models import StudentProfile


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

    def get_recipient_emails(self):
        if self.audience == self.Audience.COMPANIES:
            companies = CompanyProfile.objects.filter(user__is_active=True, receive_email_notifications=True)
            return [company.user.email for company in companies if company.user.email]

        students = StudentProfile.objects.filter(user__is_active=True, receive_email_notifications=True)
        if self.audience == self.Audience.FINAL_YEAR:
            students = students.filter(year=StudentProfile.Year.FINAL)
        return [student.user.email for student in students if student.user.email]

    def send_notifications(self):
        recipient_emails = self.get_recipient_emails()
        if not recipient_emails:
            return 0
        send_mail(
            subject=f"SkillBridge: {self.title}",
            message=f"{self.message}\n\nPosted on SkillBridge.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_emails,
            fail_silently=False,
        )
        return len(recipient_emails)
