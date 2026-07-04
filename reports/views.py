from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User
from companies.models import CompanyProfile
from jobs.models import Application, PlacementDrive
from students.models import StudentProfile

from .services import placement_summary, recent_activity


@role_required(User.Role.ADMIN)
def dashboard(request):
    context = {"summary": placement_summary(), **recent_activity()}
    return render(request, "reports/dashboard.html", context)


@role_required(User.Role.ADMIN)
def students(request):
    students = StudentProfile.objects.select_related("user")
    query = request.GET.get("q", "").strip()
    if query:
        students = students.filter(user__username__icontains=query) | students.filter(user__email__icontains=query)
    return render(request, "reports/students.html", {"students": students, "query": query})


@role_required(User.Role.ADMIN)
def toggle_student_verification(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    if request.method == "POST":
        student.is_verified = not student.is_verified
        student.save(update_fields=["is_verified", "updated_at"])
        messages.success(request, f"{student} verification was updated.")
    return redirect("reports:students")


@role_required(User.Role.ADMIN)
def companies(request):
    companies = CompanyProfile.objects.select_related("user")
    query = request.GET.get("q", "").strip()
    if query:
        companies = companies.filter(name__icontains=query) | companies.filter(user__email__icontains=query)
    return render(request, "reports/companies.html", {"companies": companies, "query": query})


@role_required(User.Role.ADMIN)
def toggle_company_approval(request, pk):
    company = get_object_or_404(CompanyProfile, pk=pk)
    if request.method == "POST":
        company.is_approved = not company.is_approved
        company.save(update_fields=["is_approved", "updated_at"])
        messages.success(request, f"{company.name} approval was updated.")
    return redirect("reports:companies")


@role_required(User.Role.ADMIN)
def drives(request):
    drives = PlacementDrive.objects.select_related("company", "created_by")
    query = request.GET.get("q", "").strip()
    if query:
        drives = drives.filter(title__icontains=query) | drives.filter(company__name__icontains=query)
    return render(request, "reports/drives.html", {"drives": drives, "query": query})


@role_required(User.Role.ADMIN)
def toggle_drive_active(request, pk):
    drive = get_object_or_404(PlacementDrive, pk=pk)
    if request.method == "POST":
        drive.is_active = not drive.is_active
        drive.save(update_fields=["is_active", "updated_at"])
        messages.success(request, f"{drive.title} active state was updated.")
    return redirect("reports:drives")


@role_required(User.Role.ADMIN)
def applications(request):
    applications = Application.objects.select_related("student", "student__user", "drive", "drive__company")
    status = request.GET.get("status", "").strip()
    if status:
        applications = applications.filter(status=status)
    return render(
        request,
        "reports/applications.html",
        {
            "applications": applications,
            "status": status,
            "status_choices": Application.Status.choices,
        },
    )
