from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User
from jobs.models import Application

from .forms import StudentProfileForm
from .services import student_dashboard_context


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
    return redirect("notifications:list")
