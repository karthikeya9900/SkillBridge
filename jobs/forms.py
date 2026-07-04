from django import forms

from .models import Application, PlacementDrive


class PlacementDriveForm(forms.ModelForm):
    package_lpa = forms.DecimalField(label="Package (LPA)", max_digits=6, decimal_places=2, required=False)
    min_cgpa = forms.DecimalField(label="Minimum CGPA", max_digits=4, decimal_places=2, required=False)

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
