import email
from django.db import models
from datetime import datetime
from django.db import models
from django.urls import reverse
from django.views.generic import ListView

# Create your models here.
class Users(models.Model):
    id_number = models.CharField(primary_key=True, unique=True, max_length = 100)
    password = models.CharField(max_length = 256)
    email = models.CharField(max_length = 50)

    class meta:
        db_table = 'Users'

    def __str__(self):
        return self.id_number

class Students(models.Model):
    StudentID = models.OneToOneField(Users, to_field='id_number', on_delete = models.CASCADE, primary_key=True, unique=True)
    first_name = models.CharField(max_length = 50, default="Not set")
    middle_name = models.CharField(max_length = 50, default="Not set")
    last_name = models.CharField(max_length = 50, default="Not set")
    gender = models.CharField(max_length = 20, default="Not set")
    department = models.CharField(max_length = 50, default="Not set")
    program = models.CharField(max_length = 50, default="Not set")
    year_level = models.IntegerField(default="1")
    contact_number = models.CharField(max_length = 50, default="Not set")
    home_address = models.CharField(max_length = 100, default="Not set")
    city_address = models.CharField(max_length = 100, default="Not set")
    permissions = models.CharField(max_length = 100, default="Not set")
    profile_pic = models.ImageField(upload_to='images/', null=True, default="Not set")

    class meta:
        db_table = 'Students'

    def __str__(self):
        return self.StudentID

class Teachers(models.Model):
    TeacherID = models.OneToOneField(Users, to_field='id_number', on_delete = models.CASCADE, primary_key=True, unique=True)
    first_name = models.CharField(max_length = 50, default="Not set")
    middle_name = models.CharField(max_length = 50, default="Not set")
    last_name = models.CharField(max_length = 50, default="Not set")
    gender = models.CharField(max_length = 20, default="Not set")
    department = models.CharField(max_length = 50, default="Not set")
    program = models.CharField(max_length = 50, default="Not set")
    contact_number = models.CharField(max_length = 50, default="Not set")
    home_address = models.CharField(max_length = 100, default="Not set")
    city_address = models.CharField(max_length = 100, default="Not set")
    permissions = models.CharField(max_length = 100, default="Not set")
    profile_pic = models.ImageField(upload_to='images/', null=True, default="Not set")

    class meta:
        db_table = 'Teachers'

    def __str__(self):
        return self.TeacherID

class Contact(models.Model):
    name = models.CharField(max_length = 50, default="Not set")
    email= models.CharField(max_length = 50)
    message = models.CharField(max_length = 250)

    class meta:
        db_table = 'Contact'
    
    def __str__(self):
        return self.email



class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, StudentID):
        events = Event.objects.filter(StudentID=StudentID)
        return events

    def get_running_events(self, StudentID):
        running_events = Event.objects.filter(
            StudentID=StudentID,
            # is_active=True,
            # is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events
    
    def get_completed_events(self, StudentID):
        completed_events = Event.objects.filter(
            StudentID=StudentID, 
            end_time__lt=datetime.now().date(),
            ).order_by("start_time")
        
        return completed_events


class Event(models.Model):
    EventID = models.AutoField(primary_key=True, unique=True)
    StudentID = models.CharField(max_length = 50, default="Not set")
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = EventManager()

    class meta:
        db_table = 'Event'

    def __str__(self):
        return str(self.EventID)
    