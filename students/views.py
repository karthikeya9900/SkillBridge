from django.contrib import messages
from django.shortcuts import redirect, render

from accounts.decorators import role_required
from accounts.models import User
from broadcasts.models import Broadcast
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
def notifications(request):
    profile = request.user.student_profile
    audiences = [Broadcast.Audience.ALL]
    if profile.year == profile.Year.FINAL:
        audiences.append(Broadcast.Audience.FINAL_YEAR)
    broadcasts = Broadcast.objects.filter(is_active=True, audience__in=audiences).select_related("created_by")
    return render(request, "students/notifications.html", {"broadcasts": broadcasts})
