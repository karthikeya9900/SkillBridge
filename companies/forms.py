from django import forms

from .models import CompanyProfile


class CompanyProfileForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CompanyProfile
        fields = ["name", "industry", "website", "contact_phone", "description", "logo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        company = super().save(commit=False)
        company.user.email = self.cleaned_data["email"]
        if commit:
            company.user.save()
            company.save()
        return company
