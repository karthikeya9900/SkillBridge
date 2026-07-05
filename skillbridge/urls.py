from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic.base import RedirectView

from accounts import views as account_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="login", permanent=False), name="home"),
    path("dashboard/", account_views.dashboard, name="dashboard"),
    path("register/", account_views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", account_views.logout_view, name="logout"),
    path("password-change/", auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"), name="password_change"),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"), name="password_change_done"),
    path("password-reset/", account_views.password_reset_request, name="password_reset"),
    path("password-reset/done/", account_views.password_reset_done, name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", account_views.password_reset_confirm, name="password_reset_confirm"),
    path("password-reset/complete/", account_views.password_reset_complete, name="password_reset_complete"),
    path("students/", include("students.urls")),
    path("companies/", include("companies.urls")),
    path("jobs/", include("jobs.urls")),
    path("broadcasts/", include("broadcasts.urls")),
    path("reports/", include("reports.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
