from jobs.models import PlacementDrive


def company_dashboard_context(company):
    drives = PlacementDrive.objects.filter(company=company).prefetch_related("applications")
    return {
        "company": company,
        "drives": drives[:10],
        "active_drive_count": drives.filter(is_active=True).count(),
        "application_count": sum(drive.applications.count() for drive in drives),
    }
