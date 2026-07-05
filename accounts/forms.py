from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, help_text="")
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[(User.Role.STUDENT, "Student"), (User.Role.COMPANY, "Company")])
    password2 = forms.CharField(
        label="Confirm password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Enter the same password as above, for verification.",
    )

    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user
