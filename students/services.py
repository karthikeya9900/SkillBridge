from broadcasts.models import Broadcast
from jobs.models import Application, PlacementDrive


def student_dashboard_context(student):
    applications = Application.objects.filter(student=student).select_related("drive", "drive__company")[:5]
    applied_drive_ids = applications.values_list("drive_id", flat=True)
    jobs = [
        drive
        for drive in PlacementDrive.objects.select_related("company").filter(is_active=True)[:20]
        if drive.is_student_eligible(student) and drive.id not in applied_drive_ids
    ]
    broadcasts = Broadcast.objects.filter(is_active=True)[:5]
    return {
        "profile": student,
        "applications": applications,
        "recommended_jobs": jobs[:5],
        "broadcasts": broadcasts,
    }
