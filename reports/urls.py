from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("students/", views.students, name="students"),
    path("students/<int:pk>/toggle-verification/", views.toggle_student_verification, name="toggle_student"),
    path("companies/", views.companies, name="companies"),
    path("companies/<int:pk>/toggle-approval/", views.toggle_company_approval, name="toggle_company"),
    path("drives/", views.drives, name="drives"),
    path("drives/<int:pk>/toggle-active/", views.toggle_drive_active, name="toggle_drive"),
    path("applications/", views.applications, name="applications"),
]
