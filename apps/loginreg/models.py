from django.db import models
from django.core.exceptions import ValidationError

import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z\s]+$')

def nameValidation(value):
    if len(value) < 2:
        raise ValidationError(
            "Name must be at least 2 characters long"
        )
    
    elif not name_regex.match(value):
        raise ValidationError(
            "Name must contain only letters and spaces"
        )

def emailValidation(value):
    a = User.objects.filter(email = value)

    if not email_regex.match(value):
        raise ValidationError(
            "Not a valid email format"
        )

    elif a:
        raise ValidationError(
            "Email already exists in our system"
        )

def passwordValidation(value):
    if len(value) < 5:
        raise ValidationError(
            "Password must be at least 5 characters long"
        )


class User(models.Model):
    name = models.CharField(max_length = 45, validators = [nameValidation])
    email = models.CharField(max_length = 45, validators = [emailValidation])
    password = models.CharField(max_length = 25, validators = [passwordValidation])
    confirm_password = models.CharField(max_length = 25)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()