from django import forms
from .models import *

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        exclude = []

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = []