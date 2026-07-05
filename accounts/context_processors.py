def show_register(request):
    """Context processor that returns `show_register` boolean.

    Hides the Register link on auth-related pages and when the user is
    already authenticated.
    """
    hide_views = {
        "login",
        "password_reset",
        "password_reset_done",
        "password_reset_confirm",
        "password_reset_complete",
    }
    view_name = None
    try:
        view_name = request.resolver_match.view_name if request.resolver_match else None
    except Exception:
        view_name = None
    return {"show_register": not request.user.is_authenticated and (view_name not in hide_views)}
