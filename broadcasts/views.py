from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User

from .forms import BroadcastForm
from .models import Broadcast
from notifications.services import notify_broadcast


@role_required(User.Role.ADMIN)
def list_broadcasts(request):
    broadcasts = Broadcast.objects.select_related("created_by")
    return render(request, "broadcasts/list.html", {"broadcasts": broadcasts})


@role_required(User.Role.ADMIN)
def create_broadcast(request):
    if request.method == "POST":
        form = BroadcastForm(request.POST)
        if form.is_valid():
            broadcast = form.save(commit=False)
            broadcast.created_by = request.user
            broadcast.save()
            broadcast.send_notifications()
            notify_broadcast(broadcast)
            messages.success(request, "Broadcast saved.")
            return redirect("broadcasts:list")
    else:
        form = BroadcastForm()
    return render(request, "broadcasts/form.html", {"form": form, "title": "Create Broadcast"})


@role_required(User.Role.ADMIN)
def edit_broadcast(request, pk):
    broadcast = get_object_or_404(Broadcast, pk=pk)
    if request.method == "POST":
        form = BroadcastForm(request.POST, instance=broadcast)
        if form.is_valid():
            form.save()
            messages.success(request, "Broadcast updated.")
            return redirect("broadcasts:list")
    else:
        form = BroadcastForm(instance=broadcast)
    return render(request, "broadcasts/form.html", {"form": form, "title": "Edit Broadcast"})


@role_required(User.Role.ADMIN)
def delete_broadcast(request, pk):
    broadcast = get_object_or_404(Broadcast, pk=pk)
    if request.method == "POST":
        title = broadcast.title
        broadcast.delete()
        messages.success(request, f"{title} was deleted.")
    else:
        messages.info(request, "Use the delete button on a broadcast to remove it.")
    return redirect("broadcasts:list")


def detail_broadcast(request, pk):
    broadcast = get_object_or_404(Broadcast.objects.select_related("created_by"), pk=pk, is_active=True)
    return render(request, "broadcasts/detail.html", {"broadcast": broadcast})
