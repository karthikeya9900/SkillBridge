from django.urls import path

from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.list_drives, name="list"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/apply/", views.apply, name="apply"),
    path("company/create/", views.create_drive, name="create"),
    path("company/<int:pk>/edit/", views.edit_drive, name="edit"),
    path("company/<int:pk>/applicants/", views.applicants, name="applicants"),
    path("applications/<int:pk>/update/", views.update_application, name="update_application"),
]
