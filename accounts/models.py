from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrator"
        STUDENT = "student", "Student"
        COMPANY = "company", "Company"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_company(self):
        return self.role == self.Role.COMPANY

    @property
    def is_platform_admin(self):
        return self.role == self.Role.ADMIN or self.is_staff
