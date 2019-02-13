from django import forms
from .models import User

import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Register (forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ("name", "email", "password", "confirm_password")

    def clean(self):
        data = super(Register, self).clean()
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError (
                "Passwords do not match"
            )

class Login(forms.Form):
    email = forms.CharField(max_length = 25)
    password = forms.CharField(max_length = 25, widget = forms.PasswordInput)

    def clean(self):
        data = super(Login, self).clean()
        email = data.get("email")
        password = data.get("password")

        user = User.objects.filter(email = email)

        if not EMAIL_REGEX.match(email):
            raise forms.ValidationError (
                "Invalid email format"
            )
        elif len(user) == 0:
            raise forms.ValidationError (
                "Cannot find e-mail address in our system"
            )
        elif not bcrypt.checkpw(password.encode(), user[0].password.encode()):
            raise forms.ValidationError (
                "Incorrect password"
            )