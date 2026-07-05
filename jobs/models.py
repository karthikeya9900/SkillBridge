from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse

from companies.models import CompanyProfile
from students.models import StudentProfile

class PlacementDrive(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name="drives")
    title = models.CharField(max_length=180)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    package_lpa = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    eligible_branches = models.CharField(max_length=255, blank=True, help_text="Comma-separated branches")
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    def get_absolute_url(self):
        return reverse("jobs:detail", kwargs={"pk": self.pk})

    def branch_list(self):
        return [branch.strip().lower() for branch in self.eligible_branches.split(",") if branch.strip()]

    def is_student_eligible(self, student):
        if self.min_cgpa and (student.cgpa is None or student.cgpa < self.min_cgpa):
            return False
        branches = self.branch_list()
        if branches and student.branch.lower() not in branches:
            return False
        return self.is_active


class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED = "applied", "Applied"
        SHORTLISTED = "shortlisted", "Shortlisted"
        INTERVIEW = "interview", "Interview"
        OFFERED = "offered", "Offered"
        REJECTED = "rejected", "Rejected"

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="applications")
    drive = models.ForeignKey(PlacementDrive, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED)
    note = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_at"]
        constraints = [
            models.UniqueConstraint(fields=["student", "drive"], name="unique_student_drive_application")
        ]

    def __str__(self):
        return f"{self.student} - {self.drive}"

    def save(self, *args, **kwargs):
        previous_status = None
        if self.pk:
            previous_status = Application.objects.filter(pk=self.pk).values_list("status", flat=True).first()
        super().save(*args, **kwargs)

        from notifications.services import notify_application_status_change

        notify_application_status_change(self, previous_status)

        if previous_status and previous_status != self.status and self.student.user.email and self.student.receive_email_notifications:
            send_mail(
                subject=f"SkillBridge application update: {self.drive.title}",
                message=f"Your application status for {self.drive.title} is now {self.get_status_display()}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.student.user.email],
                fail_silently=False,
            )
