from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import get_notifications_for_user, mark_notifications_read


@login_required
def list_notifications(request):
    notifications = get_notifications_for_user(request.user)
    mark_notifications_read(request.user)
    return render(request, "notifications/list.html", {"notifications": notifications})
