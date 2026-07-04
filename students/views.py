from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.decorators import role_required
from accounts.models import User

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
