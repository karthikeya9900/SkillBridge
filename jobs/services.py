from django.db import IntegrityError

from .models import Application, PlacementDrive


def visible_drives_for_user(user):
    queryset = PlacementDrive.objects.select_related("company").filter(is_active=True)
    if getattr(user, "is_student", False):
        student = user.student_profile
        return [drive for drive in queryset if drive.is_student_eligible(student)]
    return queryset


def filter_drives(drives, filters):
    query = filters.get("q", "").strip().lower()
    branch = filters.get("branch", "").strip().lower()
    location = filters.get("location", "").strip().lower()
    min_cgpa = filters.get("min_cgpa", "").strip()

    filtered = list(drives)
    if query:
        filtered = [
            drive
            for drive in filtered
            if query in drive.title.lower()
            or query in drive.company.name.lower()
            or query in drive.description.lower()
        ]
    if branch:
        filtered = [
            drive
            for drive in filtered
            if not drive.branch_list() or branch in drive.branch_list()
        ]
    if location:
        filtered = [drive for drive in filtered if location in drive.location.lower()]
    if min_cgpa:
        try:
            cgpa_value = float(min_cgpa)
        except ValueError:
            return filtered
        filtered = [
            drive
            for drive in filtered
            if drive.min_cgpa is None or float(drive.min_cgpa) <= cgpa_value
        ]
    return filtered


def apply_to_drive(student, drive):
    if not drive.is_student_eligible(student):
        return None, "You are not eligible for this placement drive."
    try:
        application = Application.objects.create(student=student, drive=drive)
    except IntegrityError:
        return None, "You have already applied for this drive."
    return application, "Application submitted."
