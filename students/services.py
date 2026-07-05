from broadcasts.models import Broadcast
from jobs.models import Application, PlacementDrive
from django.db.models import Count
from companies.models import CompanyProfile
from students.models import StudentProfile
import json


def student_dashboard_context(student):
    applications = Application.objects.filter(student=student).select_related("drive", "drive__company")[:5]
    applied_drive_ids = set(Application.objects.filter(student=student).values_list("drive_id", flat=True))
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
        # Stats for dashboard
        "total_companies": CompanyProfile.objects.count(),
        "total_students": StudentProfile.objects.count(),
        "total_drives": PlacementDrive.objects.count(),
        "active_drives": PlacementDrive.objects.filter(is_active=True).count(),
        "applications_by_status": list(Application.objects.filter(student=student).values("status").annotate(count=Count("id")).order_by("status")),
        "year_distribution": list(StudentProfile.objects.values("year").annotate(count=Count("id")).order_by("year")),
        # JSON serialized versions for safe JS consumption
        "applications_by_status_json": json.dumps(list(Application.objects.filter(student=student).values("status").annotate(count=Count("id")).order_by("status"))),
        "year_distribution_json": json.dumps(list(StudentProfile.objects.values("year").annotate(count=Count("id")).order_by("year"))),
    }
