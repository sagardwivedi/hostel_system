from django import forms
from django.contrib.auth.models import User

from .models import Application


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=254,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your username"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password"}
        ),
    )


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Username",
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]  # Include username here

        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "name",
            "roll_number",
            "location",
            "cet_marks",
            "caste",
        ]
        labels = {
            "name": "Full Name",
            "roll_number": "Roll Number",
            "location": "Current Location",
            "cet_marks": "CET Score",
            "caste": "Category",
        }
        help_texts = {
            "roll_number": "Enter your college roll number",
            "cet_marks": "Enter your CET examination score",
            "location": "Enter your current residential address",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your full name",
                    "pattern": "[A-Za-z ]+",
                    "title": "Only letters and spaces allowed",
                }
            ),
            "roll_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your roll number",
                    "pattern": "[A-Za-z0-9]+",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your current location",
                }
            ),
            "cet_marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your CET marks",
                    "min": "0",
                    "max": "100",
                }
            ),
            "caste": forms.Select(attrs={"class": "form-control form-select"}),
        }

    def clean_cet_marks(self):
        marks = self.cleaned_data.get("cet_marks")
        if marks is not None and (marks < 0 or marks > 100):
            raise forms.ValidationError("CET marks must be between 0 and 100")
        return marks

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Name is required")
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Name can only contain letters and spaces")
        return name.title()

    def clean_roll_number(self):
        roll_number = self.cleaned_data.get("roll_number", "").strip()
        if not roll_number:
            raise forms.ValidationError("Roll Number is required")
        if not roll_number.isalnum():
            raise forms.ValidationError(
                "Roll Number can only contain letters and numbers"
            )
        return roll_number

    def clean_location(self):
        location = self.cleaned_data.get("location", "").strip()
        if not location:
            raise forms.ValidationError("Location is required")
        return location

    def clean_caste(self):
        caste = self.cleaned_data.get("caste")
        if caste is None:
            raise forms.ValidationError("Category selection is required")
        return caste
