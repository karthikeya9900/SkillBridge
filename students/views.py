from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User
from broadcasts.models import Broadcast
from jobs.models import Application

from .forms import StudentProfileForm
from .services import student_dashboard_context
from django.db.models import Count
from companies.models import CompanyProfile
from jobs.models import PlacementDrive
from students.models import StudentProfile


@role_required(User.Role.STUDENT)
def dashboard(request):
    profile = request.user.student_profile
    return render(request, "students/dashboard.html", student_dashboard_context(profile))


@role_required(User.Role.STUDENT)
def edit_profile(request):
    profile = request.user.student_profile
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("students:dashboard")
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, "students/profile_form.html", {"form": form})


@role_required(User.Role.STUDENT)
def applications(request):
    profile = request.user.student_profile
    applications = Application.objects.filter(student=profile).select_related("drive", "drive__company")
    return render(request, "students/applications.html", {"applications": applications})


@role_required(User.Role.STUDENT)
def application_detail(request, pk):
    profile = request.user.student_profile
    application = get_object_or_404(
        Application.objects.select_related("drive", "drive__company"),
        pk=pk,
        student=profile,
    )

    timeline_steps = [
        {"label": "Applied", "order": 0},
        {"label": "Resume Reviewed", "order": 1},
        {"label": "Shortlisted", "order": 2},
        {"label": "Technical Interview", "order": 3},
        {"label": "HR Interview", "order": 4},
        {"label": "Offer Letter", "order": 5},
    ]

    status_order = {
        Application.Status.APPLIED: 0,
        Application.Status.SHORTLISTED: 2,
        Application.Status.INTERVIEW: 3,
        Application.Status.OFFERED: 5,
        Application.Status.REJECTED: 5,
    }
    current_order = status_order.get(application.status, 0)

    for step in timeline_steps:
        if step["order"] < current_order:
            step["state"] = "done"
        elif step["order"] == current_order:
            step["state"] = "current"
        else:
            step["state"] = "pending"

    rejected = application.status == Application.Status.REJECTED

    return render(
        request,
        "students/application_detail.html",
        {
            "application": application,
            "timeline_steps": timeline_steps,
            "rejected": rejected,
        },
    )


@role_required(User.Role.STUDENT)
def notifications(request):
    profile = request.user.student_profile
    audiences = [Broadcast.Audience.ALL]
    if profile.year == profile.Year.FINAL:
        audiences.append(Broadcast.Audience.FINAL_YEAR)
    broadcasts = Broadcast.objects.filter(is_active=True, audience__in=audiences).select_related("created_by")
    return render(request, "students/notifications.html", {"broadcasts": broadcasts})


@role_required(User.Role.STUDENT)
def stats_dashboard(request):
    # High-level counts
    total_companies = CompanyProfile.objects.count()
    total_students = StudentProfile.objects.count()
    total_drives = PlacementDrive.objects.count()
    active_drives = PlacementDrive.objects.filter(is_active=True).count()

    # Applications by status
    applications_by_status = (
        Application.objects.values("status").annotate(count=Count("id")).order_by("status")
    )

    # Students by year distribution
    year_distribution = (
        StudentProfile.objects.values("year").annotate(count=Count("id")).order_by("year")
    )

    context = {
        "total_companies": total_companies,
        "total_students": total_students,
        "total_drives": total_drives,
        "active_drives": active_drives,
        "applications_by_status": list(applications_by_status),
        "year_distribution": list(year_distribution),
    }
    return render(request, "students/stats.html", context)
