from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegistrationForm
from .models import User
from .services import create_profile_for_user


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "accounts/home.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            create_profile_for_user(user)
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("dashboard")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect("home")
    if request.user.is_authenticated:
        messages.info(request, "Use the logout button to end your session.")
        return redirect("dashboard")
    return redirect("home")


@login_required
def dashboard(request):
    user = request.user
    if user.is_platform_admin:
        return redirect("reports:dashboard")
    if user.role == User.Role.COMPANY:
        return redirect("companies:dashboard")
    return redirect("students:dashboard")
