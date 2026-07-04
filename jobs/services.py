from django.db import IntegrityError

from .models import Application, PlacementDrive


def visible_drives_for_user(user):
    queryset = PlacementDrive.objects.select_related("company").filter(is_active=True)
    if getattr(user, "is_student", False):
        student = user.student_profile
        return [drive for drive in queryset if drive.is_student_eligible(student)]
    return queryset


def apply_to_drive(student, drive):
    if not drive.is_student_eligible(student):
        return None, "You are not eligible for this placement drive."
    try:
        application = Application.objects.create(student=student, drive=drive)
    except IntegrityError:
        return None, "You have already applied for this drive."
    return application, "Application submitted."
