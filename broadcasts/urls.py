from django.urls import path

from . import views

app_name = "broadcasts"

urlpatterns = [
    path("", views.list_broadcasts, name="list"),
    path("create/", views.create_broadcast, name="create"),
    path("<int:pk>/edit/", views.edit_broadcast, name="edit"),
]
