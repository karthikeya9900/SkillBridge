from django import forms

from .models import Broadcast


class BroadcastForm(forms.ModelForm):
    class Meta:
        model = Broadcast
        fields = ["title", "message", "audience", "publish_at", "is_active"]
        widgets = {"publish_at": forms.DateTimeInput(attrs={"type": "datetime-local"})}
