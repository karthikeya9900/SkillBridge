from companies.models import CompanyProfile
from students.models import StudentProfile

from .models import User


def create_profile_for_user(user):
    if user.role == User.Role.STUDENT:
        StudentProfile.objects.get_or_create(user=user)
    elif user.role == User.Role.COMPANY:
        CompanyProfile.objects.get_or_create(user=user, defaults={"name": user.get_full_name() or user.username})
