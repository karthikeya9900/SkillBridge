from django.shortcuts import render

from accounts.decorators import role_required
from accounts.models import User

from .services import placement_summary, recent_activity


@role_required(User.Role.ADMIN)
def dashboard(request):
    context = {"summary": placement_summary(), **recent_activity()}
    return render(request, "reports/dashboard.html", context)
