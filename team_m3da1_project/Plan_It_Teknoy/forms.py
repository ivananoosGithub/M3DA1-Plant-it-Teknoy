from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['id_number', 'password', 'email']
        exclude = []

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['StudentID','first_name','middle_name','last_name','gender','department','program','year_level','contact_number','home_address','city_address']
        exclude = ['permissions']

class TeachersForm(forms.ModelForm):
    class Meta:
        model = Teachers
        fields = ['TeacherID','first_name','middle_name','last_name','gender','department','program','contact_number','home_address','city_address']
        exclude = ['permissions']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = []

