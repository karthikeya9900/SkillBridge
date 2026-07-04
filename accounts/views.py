from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

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


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = get_user_model().objects.filter(email__iexact=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token}))
                send_mail(
                    "Reset your SkillBridge password",
                    f"Use the following link to reset your password:\n\n{reset_url}",
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            messages.success(request, "We’ve emailed you instructions to reset your password.")
            return redirect("password_reset_done")
    else:
        form = PasswordResetForm()
    return render(request, "accounts/password_reset.html", {"form": form})


def password_reset_done(request):
    return render(request, "accounts/password_reset_done.html")


def password_reset_confirm(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset.")
                return redirect("password_reset_complete")
        else:
            form = SetPasswordForm(user)
        return render(request, "accounts/password_reset_confirm.html", {"form": form})

    return render(request, "accounts/password_reset_confirm.html", {"invalid_link": True})


def password_reset_complete(request):
    return render(request, "accounts/password_reset_complete.html")


@login_required
def dashboard(request):
    user = request.user
    if user.is_platform_admin:
        return redirect("reports:dashboard")
    if user.role == User.Role.COMPANY:
        return redirect("companies:dashboard")
    return redirect("students:dashboard")
