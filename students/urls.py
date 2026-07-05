from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("profile/", views.edit_profile, name="profile"),
    path("applications/", views.applications, name="applications"),
    path("applications/<int:pk>/", views.application_detail, name="application_detail"),
    path("notifications/", views.notifications, name="notifications"),
]
