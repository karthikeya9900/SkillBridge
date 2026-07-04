from django.contrib import messages
from django.shortcuts import redirect, render

from accounts.decorators import role_required
from accounts.models import User

from .forms import CompanyProfileForm
from .services import company_dashboard_context


@role_required(User.Role.COMPANY)
def dashboard(request):
    company = request.user.company_profile
    return render(request, "companies/dashboard.html", company_dashboard_context(company))


@role_required(User.Role.COMPANY)
def edit_profile(request):
    company = request.user.company_profile
    if request.method == "POST":
        form = CompanyProfileForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company profile updated.")
            return redirect("companies:dashboard")
    else:
        form = CompanyProfileForm(instance=company)
    return render(request, "companies/profile_form.html", {"form": form})
