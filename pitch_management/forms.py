from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from tempus_dominus.widgets import DatePicker

from .models import Pitch, Profile, Booking


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, help_text="First Name")
    last_name = forms.CharField(max_length=100, help_text="Last Name")
    address = forms.CharField(max_length=150, help_text="Address")
    phone_number = forms.CharField(max_length=100, help_text="Phone Numer")

    class Meta:
        model = Profile
        fields = (
            "username",
            "first_name",
            "last_name",
            "address",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class NewPitchForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text="Name")
    size = forms.CharField(max_length=100, help_text="Size")
    price = forms.CharField(max_length=100, help_text="Price")

    class Meta:
        model = Pitch
        fields = (
            "name",
            "size",
            "price",
        )


class DateForm(forms.Form):
    date_field = forms.DateField(
        label="Find an available pitch!",
        required=True,
        widget=DatePicker(
            options={
                "minDate": str(date.today()),
            },
        ),
    )
