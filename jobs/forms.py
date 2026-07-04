from django import forms

from .models import Application, PlacementDrive


class PlacementDriveForm(forms.ModelForm):
    class Meta:
        model = PlacementDrive
        fields = [
            "title",
            "description",
            "requirements",
            "location",
            "package_lpa",
            "min_cgpa",
            "eligible_branches",
            "deadline",
            "is_active",
        ]
        widgets = {"deadline": forms.DateInput(attrs={"type": "date"})}


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["status", "note"]
