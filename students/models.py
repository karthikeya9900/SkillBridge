from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    class Year(models.TextChoices):
        FIRST = "1", "First Year"
        SECOND = "2", "Second Year"
        THIRD = "3", "Third Year"
        FINAL = "4", "Final Year"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=120, blank=True)
    branch = models.CharField(max_length=120, blank=True)
    year = models.CharField(max_length=1, choices=Year.choices, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    photo = models.ImageField(upload_to="students/photos/", blank=True)
    resume = models.FileField(upload_to="students/resumes/", blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def skill_list(self):
        return [skill.strip() for skill in self.skills.split(",") if skill.strip()]
