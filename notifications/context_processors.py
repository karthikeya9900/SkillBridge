from .services import unread_count


def notification_context(request):
    if request.user.is_authenticated:
        return {"unread_notification_count": unread_count(request.user)}
    return {"unread_notification_count": 0}
