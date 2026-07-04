from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User

from .forms import ApplicationStatusForm, PlacementDriveForm
from .models import Application, PlacementDrive
from .services import apply_to_drive, filter_drives, visible_drives_for_user


@login_required
def list_drives(request):
    drives = filter_drives(visible_drives_for_user(request.user), request.GET)
    return render(request, "jobs/list.html", {"drives": drives, "filters": request.GET})


@login_required
def detail(request, pk):
    drive = get_object_or_404(PlacementDrive.objects.select_related("company"), pk=pk)
    existing_application = None
    if request.user.is_student:
        existing_application = Application.objects.filter(student=request.user.student_profile, drive=drive).first()
    return render(request, "jobs/detail.html", {"drive": drive, "existing_application": existing_application})


@role_required(User.Role.STUDENT)
def apply(request, pk):
    drive = get_object_or_404(PlacementDrive, pk=pk)
    _, message = apply_to_drive(request.user.student_profile, drive)
    messages.info(request, message)
    return redirect("jobs:detail", pk=drive.pk)


@role_required(User.Role.COMPANY)
def create_drive(request):
    company = request.user.company_profile
    if not company.is_approved:
        messages.error(request, "Your company must be approved before posting placement drives.")
        return redirect("companies:dashboard")
    if request.method == "POST":
        form = PlacementDriveForm(request.POST)
        if form.is_valid():
            drive = form.save(commit=False)
            drive.company = company
            drive.created_by = request.user
            drive.save()
            messages.success(request, "Placement drive created.")
            return redirect("companies:dashboard")
    else:
        form = PlacementDriveForm()
    return render(request, "jobs/drive_form.html", {"form": form, "title": "Create Placement Drive"})


@role_required(User.Role.COMPANY)
def edit_drive(request, pk):
    drive = get_object_or_404(PlacementDrive, pk=pk, company=request.user.company_profile)
    if request.method == "POST":
        form = PlacementDriveForm(request.POST, instance=drive)
        if form.is_valid():
            form.save()
            messages.success(request, "Placement drive updated.")
            return redirect("companies:dashboard")
    else:
        form = PlacementDriveForm(instance=drive)
    return render(request, "jobs/drive_form.html", {"form": form, "title": "Edit Placement Drive"})


@role_required(User.Role.COMPANY)
def delete_drive(request, pk):
    drive = get_object_or_404(PlacementDrive, pk=pk, company=request.user.company_profile)
    if request.method == "POST":
        title = drive.title
        drive.delete()
        messages.success(request, f"{title} was deleted.")
    else:
        messages.info(request, "Use the delete button on a drive to remove it.")
    return redirect("companies:dashboard")


@role_required(User.Role.COMPANY)
def close_drive(request, pk):
    drive = get_object_or_404(PlacementDrive, pk=pk, company=request.user.company_profile)
    if request.method == "POST":
        drive.is_active = False
        drive.save(update_fields=["is_active", "updated_at"])
        messages.success(request, f"{drive.title} was closed.")
    else:
        messages.info(request, "Use the close button on a drive to deactivate it.")
    return redirect("companies:dashboard")


@role_required(User.Role.COMPANY)
def applicants(request, pk):
    drive = get_object_or_404(PlacementDrive, pk=pk, company=request.user.company_profile)
    applications = drive.applications.select_related("student", "student__user")
    return render(request, "jobs/applicants.html", {"drive": drive, "applications": applications})


@role_required(User.Role.COMPANY)
def update_application(request, pk):
    application = get_object_or_404(
        Application.objects.select_related("drive"),
        pk=pk,
        drive__company=request.user.company_profile,
    )
    if request.method == "POST":
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Application status updated.")
            return redirect("jobs:applicants", pk=application.drive.pk)
    else:
        form = ApplicationStatusForm(instance=application)
    return render(request, "jobs/application_form.html", {"form": form, "application": application})
