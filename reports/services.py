from accounts.models import User
from companies.models import CompanyProfile
from jobs.models import Application, PlacementDrive
from students.models import StudentProfile


def placement_summary():
    return {
        "students": StudentProfile.objects.count(),
        "companies": CompanyProfile.objects.count(),
        "approved_companies": CompanyProfile.objects.filter(is_approved=True).count(),
        "jobs": PlacementDrive.objects.count(),
        "active_jobs": PlacementDrive.objects.filter(is_active=True).count(),
        "applications": Application.objects.count(),
        "offers": Application.objects.filter(status=Application.Status.OFFERED).count(),
        "users": User.objects.count(),
    }


def recent_activity():
    return {
        "recent_jobs": PlacementDrive.objects.select_related("company")[:5],
        "recent_applications": Application.objects.select_related("student", "student__user", "drive")[:5],
    }
