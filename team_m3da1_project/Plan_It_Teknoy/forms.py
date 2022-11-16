from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm, DateInput
# from calendarapp.models import Event, EventMember

from django import forms

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['id_number', 'password', 'email']
        exclude = []

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['StudentID','first_name','middle_name','last_name','gender','department','program','year_level','contact_number','home_address','city_address', 'profile_pic']
        exclude = ['permissions']

class TeachersForm(forms.ModelForm):
    class Meta:
        model = Teachers
        fields = ['TeacherID','first_name','middle_name','last_name','gender','department','program','contact_number','home_address','city_address', 'profile_pic']
        exclude = ['permissions']

class DocumentsForm(forms.ModelForm):
    class Meta:
        model = DocumentGen
        fields = ['DocumentID', 'filename', 'content']
        exclude = ['content']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = []

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['EventID','StudentID', "title", "description", "start_time", "end_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            "StudentID": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter user id"}
            ),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["EventID", 'StudentID']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)