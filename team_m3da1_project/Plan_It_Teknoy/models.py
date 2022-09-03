from django.db import models

# Create your models here.
class Users(models.Model):
    id_number = models.CharField(primary_key=True, unique=True, max_length = 12)
    password = models.CharField(max_length = 256)
    email = models.CharField(max_length = 50)

    class meta:
        db_table = 'Users'

    def __str__(self):
        return self.user

class Students(models.Model):
    StudentID = models.OneToOneField(Users, to_field='id_number', on_delete = models.CASCADE, primary_key=True, unique=True)
    first_name = models.CharField(max_length = 50, default="Not set")
    middle_name = models.CharField(max_length = 50, default="Not set")
    last_name = models.CharField(max_length = 50, default="Not set")
    gender = models.CharField(max_length = 20, default="Not set")
    department = models.CharField(max_length = 50, default="Not set")
    program = models.CharField(max_length = 50, default="Not set")
    year_level = models.IntegerField(default="Not set")
    contact_number = models.CharField(max_length = 50, default="Not set")
    home_address = models.CharField(max_length = 100, default="Not set")
    city_address = models.CharField(max_length = 100, default="Not set")
    permissions = models.CharField(max_length = 100, default="Not set")

    class meta:
        db_table = 'Students'

    def __str__(self):
        return self.student

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

    class meta:
        db_table = 'Teachers'

    def __str__(self):
        return self.teacher