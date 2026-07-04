from django import forms

from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()
    cgpa = forms.DecimalField(label="CGPA", max_digits=4, decimal_places=2, required=False)
    receive_email_notifications = forms.BooleanField(required=False, label="Email me about important updates")

    class Meta:
        model = StudentProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "branch",
            "year",
            "cgpa",
            "skills",
            "photo",
            "resume",
            "receive_email_notifications",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance.user
        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name
        self.fields["email"].initial = user.email
        self.fields["receive_email_notifications"].initial = self.instance.receive_email_notifications

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile.save()
        return profile
