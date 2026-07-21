from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User, Listing


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "autocomplete": "username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
    )


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
            }
        )
    )

    class Meta:
        model = User

        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "is_landlord",
            "is_tenant",
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Repeat password"

        self.fields["is_landlord"].widget.attrs["class"] = "form-check-input"
        self.fields["is_tenant"].widget.attrs["class"] = "form-check-input"

        self.fields["is_landlord"].label = "I am a landlord"
        self.fields["is_tenant"].label = "I am a tenant"


class ListingForm(forms.ModelForm):

    class Meta:

        model = Listing

        fields = [
            "title",
            "description",
            "image",
            "location",
            "price",
            "rooms",
            "housing_type",
            "is_active",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Describe your property..."
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

        self.fields["title"].widget.attrs["placeholder"] = "Apartment in Berlin"

        self.fields["location"].widget.attrs["placeholder"] = "Berlin"

        self.fields["price"].widget.attrs["placeholder"] = "1200"

        self.fields["rooms"].widget.attrs["placeholder"] = "3"

        self.fields["image"].widget.attrs["class"] = "form-control"

        self.fields["is_active"].widget.attrs["class"] = "form-check-input"

        self.fields["is_active"].label = "Listing is active"

        self.fields["housing_type"].empty_label = "Select housing type"