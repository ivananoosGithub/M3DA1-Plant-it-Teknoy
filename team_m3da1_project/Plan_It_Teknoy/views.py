import json
from multiprocessing import context
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic import View
from django.core.serializers.json import DjangoJSONEncoder
from .forms import *
from .models import *
from passlib.hash import pbkdf2_sha256
import calendar
from datetime import timedelta, datetime, date
from django.core.mail import send_mail
from django.conf import settings
import uuid
#from calendarapp.models import EventMember, Event
#from calendarapp.forms import EventForm
# Calendarapp Imports


#################################### Start of user pages ###################################

# Logout current_user session
def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('Plan_It_Teknoy:Home')
    return redirect('Plan_It_Teknoy:Home')

# Home and Landing Page
def home(response):
    return render(response, "Home.html", {})

# About Us Page
def about(response):
    return render(response, "About.html", {})


# Password Reset Send Mail Function
def send_forget_password_mail(email):
    code = str(uuid.uuid4())
    subject = 'Your forget password link'
    message = f'Hi, click on the link to reset your password http://127.0.0.1:8000/ForgotPassword/{code}/'
    email_from  = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

# listToString for Password Checking
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 

# Select Role Page
class SelectRoleView(View):
    def get(self, request):
        # return render(request, 'signup-role.html', {})
        return render(request, 'user-selection.html', {})

# Contact Us page
class contactView(View):
    def get(self, request): 
        if 'user' in request.session:
            current_user = request.session['user']
            students = Students.objects.filter(StudentID=current_user)     
            users = Users.objects.filter(id_number=current_user)

            context = {
                'current_user': current_user,
                'students' : students,
                'users' : users,
            }
            return render(request, 'Contact.html', context)
        else:
            return render(request, 'Contact.html', {})

    def post(self,request):
        form = ContactForm(request.POST, request.FILES)        
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get("email")
            message = request.POST.get('message')
            form = Contact(name = name, email = email, message = message)         
            form.save()
            return redirect('Plan_It_Teknoy:contact_view')
        else:
            print(form.errors)
            messages.info(request, 'Please complete the fields', extra_tags='try')
            return redirect('Plan_It_Teknoy:contact_view')

# Sign in page
class SignInView(View):
    def get(self, request):
        if 'user' in request.session:
            current_user = request.session['user']
            students = Students.objects.filter(StudentID=current_user)
            teachers = Teachers.objects.filter(TeacherID=current_user) 
            users = Users.objects.filter(id_number=current_user)

            context = {
                'current_user': current_user,
                'students' : students,
                'teachers' : teachers,
                'users' : users,
            }
            return render(request, 'signin.html', context)
        else:
            return render(request, 'signin.html', {})
    
    def post(self, request):
        if request.method == 'POST':
            if 'btnSignIn' in request.POST:
                id_number = request.POST.get('id_number')
                email = request.POST.get("email")
                password = request.POST.get('password')
                check_password = Users.objects.filter(id_number=id_number).values_list("password",flat=True)
                listpw = list(check_password)
                dec_password = pbkdf2_sha256.verify(password, listToString(listpw))
                check_id = Users.objects.filter(id_number=id_number)

                check_email = Users.objects.filter(email=email)
                if check_id and dec_password and check_email:
                    request.session['user'] = id_number
                    if Users.objects.filter(id_number=id_number).count()>0:
                        return redirect('Plan_It_Teknoy:dashboard_view')
                else:
                    # does not display
                    messages.info(request, 'Incorrect ID Number and Email and Password!')
                    return redirect('Plan_It_Teknoy:signin_view') 

            elif 'btnForgotPass' in request.POST:
                email = request.POST.get("email")

                if Users.objects.filter(email=email).count()>0:                   
                    request.session['email'] = email
                    send_forget_password_mail(email)
                    # add text that says email sent
                    return redirect('Plan_It_Teknoy:signin_view')

                # add else if email not in db
                return redirect('Plan_It_Teknoy:contact_view')

class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'forgotpass.html', {})

    def post(self, request):
        if request.method == 'POST':
            email = request.POST.get("email")

            if Users.objects.filter(email=email).count()>0:
                
                request.session['email'] = email
                send_forget_password_mail(email)
                return redirect('Plan_It_Teknoy:Home')
            return redirect('Plan_It_Teknoy:contact_view')

class ChangePasswordSentView(View):
    def get(self, request, *args, **kwargs):
        email = request.session['email']
        context = {
            'email':email,
        }
        return render(request, 'fpsent.html', context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            id_number = request.POST.get('id_number')
            email = request.POST.get("email")
            u = Users.objects.get(email=email)
            password = request.POST.get("password")
            cpassword = request.POST.get("cpassword")
            enc_password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
            if(cpassword == password):
                u.password = enc_password
                u.save()
                return redirect('Plan_It_Teknoy:signin_view')

        else:
            return redirect('Plan_It_Teknoy:signupS_view')

# Student Sign Up
class SignUpStudentView(View):
    def get(self, request):
        if 'user' in request.session:
            current_user = request.session['user']
            students = Students.objects.filter(StudentID=current_user)
            teachers = Teachers.objects.filter(TeacherID=current_user) 
            users = Users.objects.filter(id_number=current_user)

            context = {
                'current_user': current_user,
                'students' : students,
                'teachers' : teachers,
                'users' : users,
            }
            return render(request, 'Home.html', context)
        else:
            return render(request, 'signup-student.html', {})

    def post(self, request):        
        form1 = StudentsForm(request.POST, request.FILES)        
        form2 = UsersForm(request.POST, request.FILES)       
        if form1.is_valid() or form2.is_valid():
            # Personal Information
            first_name = request.POST.get("first_name")
            middle_name = request.POST.get("middle_name")
            last_name = request.POST.get("last_name")
            gender = request.POST.get("gender")
            department = request.POST.get("department")
            program = request.POST.get("program")
            year_level = request.POST.get("year_level")
            # Contact Information
            home_address = request.POST.get("home_address")
            city_address = request.POST.get("city_address")
            contact_number = request.POST.get("contact_number")
            # Account Information
            id_number = request.POST.get("id_number")
            password = request.POST.get("password")
            confirmpassword = request.POST.get("cpassword")
            enc_password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
            email = request.POST.get("email")
            if(confirmpassword == password):
                if Students.objects.filter(StudentID=id_number).count()>0 or Users.objects.filter(id_number=id_number).count()>0:
                    messages.info(request, 'ID Number already exists!')
                    return redirect('Plan_It_Teknoy:signupS_view') 
                else:              
                    form2 = Users(id_number = id_number, password = enc_password, email = email)
                    form2.save()
                    
                    fk_id_number = Users.objects.get(id_number = id_number)

                    form1 = Students(StudentID = fk_id_number, first_name = first_name, middle_name = middle_name, last_name = last_name, gender = gender, department = department, program = program, year_level = year_level, home_address = home_address, city_address = city_address, contact_number = contact_number)
                    form1.save()

                    check_user = Users.objects.filter(id_number=id_number, password=enc_password, email = email)
                    if check_user:
                        request.session['user'] = id_number
                        return redirect('Plan_It_Teknoy:signin_view')
            else:
                messages.info(request, 'Passwords do not match!', extra_tags='signin')
                return redirect('Plan_It_Teknoy:signupS_view')
        else:
            print(form1.errors,form2.errors)
            messages.info(request, 'Account already exists! Please try another unique one.', extra_tags='try')
            return redirect('Plan_It_Teknoy:signupS_view')

# Teacher Sign Up
class SignUpTeacherView(View):
    def get(self, request):
        if 'user' in request.session:
            current_user = request.session['user']
            students = Students.objects.filter(StudentID=current_user)
            teachers = Teachers.objects.filter(TeacherID=current_user) 
            users = Users.objects.filter(id_number=current_user)

            context = {
                'current_user': current_user,
                'students' : students,
                'teachers' : teachers,
                'users' : users,
            }
            return render(request, 'Home.html', context)
        else:
            return render(request, 'signup-teacher.html', {})

    def post(self, request):        
        form1 = StudentsForm(request.POST, request.FILES)        
        form2 = UsersForm(request.POST, request.FILES)          
        if form1.is_valid() or form2.is_valid():
            # Personal Information
            first_name = request.POST.get("first_name")
            middle_name = request.POST.get("middle_name")
            last_name = request.POST.get("last_name")
            gender = request.POST.get("gender")
            department = request.POST.get("department")
            program = request.POST.get("program")
            # Contact Information
            home_address = request.POST.get("home_address")
            city_address = request.POST.get("city_address")
            contact_number = request.POST.get("contact_number")
            # Account Information
            id_number = request.POST.get("id_number")
            password = request.POST.get("password")
            confirmpassword = request.POST.get("cpassword")
            enc_password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
            email = request.POST.get("email")
            if(confirmpassword == password):
                if Teachers.objects.filter(TeacherID=id_number).count()>0 or Users.objects.filter(id_number=id_number).count()>0:
                    messages.info(request, 'ID Number already exists!')
                    return redirect('Plan_It_Teknoy:signupT_view') 
                else:
                    form2 = Users(id_number = id_number, password = enc_password, email = email)
                    form2.save()

                    fk_id_number = Users.objects.get(id_number = id_number)

                    form1 = Teachers(TeacherID = fk_id_number, first_name = first_name, middle_name = middle_name, last_name = last_name, gender = gender, department = department, program = program, home_address = home_address, city_address = city_address, contact_number = contact_number)
                    form1.save()

                    check_user = Users.objects.filter(id_number=id_number, password=enc_password, email = email)
                    if check_user:
                        request.session['user'] = id_number
                        return redirect('Plan_It_Teknoy:signin_view')
            else:
                messages.info(request, 'Passwords do not match!', extra_tags='signin')
                return redirect('Plan_It_Teknoy:signupT_view')
        else:
            print(form1.errors,form2.errors)
            messages.info(request, 'Account already exists! Please try another unique one.', extra_tags='try')
            return redirect('Plan_It_Teknoy:signupT_view')

# Calendar View
class CalendarViewNew(View):

    def get(self, request):
        form = EventForm(request.POST or None)
        if 'user' in request.session:
            current_user = request.session['user']
            confirm_user_id = Users(id_number=current_user)
            current_student = Students(StudentID=confirm_user_id)
            # event = Event.objects.filter(StudentID = current_student.StudentID)
            running_events = Event.objects.get_running_events(StudentID=current_student.StudentID)
            # events = Event.objects.get_all_events(StudentID=current_student.StudentID)

            #accessing all student records in the database
            student_record = Students.objects.raw('SELECT StudentID_id, first_name, program, last_name, year_level, profile_pic FROM plan_it_teknoy_students WHERE StudentID_id = %s', [current_student.StudentID])
            # student_events = Event.objects.filter(StudentID=current_student.StudentID, end_time__gte=datetime.now().date())

            student_running_events = []

            for student_event in running_events:
                student_running_events.append(
                    {
                    "title":student_event.title,
                    "start":student_event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "end":student_event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

                print(student_event.start_time.strftime("%Y-%m-%d %H:%M:%S"))
                print(student_event.end_time.strftime("%Y-%m-%d %H:%M:%S"))

            context = {"student_running_events":student_running_events,  
            "running_events":running_events, "form":form, "student_record":student_record}

            return render(request, 'calendarapp/calendar.html', context)
            



            
            # Event.objects.raw('SELECT EventID, StudentID, title, start_time, end_time FROM plan_it_teknoy_event WHERE StudentID = %s', [current_student.StudentID])

            # data = dict.fromkeys(['context', 'events', 'forms', 'student_record', 'current_user'])
            # data.update(current_user=current_user, event=running_events, student_record=student_record, form=form)
            # contextArr = []
            # print(context)
            

            # for student_event in student_events:
            #     event_title = student_event.title
            #     event_start_time = json.dumps(
            #         student_event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            #         sort_keys=True,
            #         indent=1,
            #         cls=DjangoJSONEncoder)

            #     event_end_time = json.dumps(
            #         student_event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            #         sort_keys=True,
            #         indent=1,
            #         cls=DjangoJSONEncoder)

            #     print(event_title)
            #     # print(event_start_time)
            #     # print(event_end_time)

            #     currentContext = {
            #     "event_title":event_title,
            #     "event_start_time":json.loads(event_start_time),
            #     "event_end_time":json.loads(event_end_time)
            #     }
            #     print(currentContext)
            #     contextArr.append(currentContext)
            #     data.update(context=contextArr)

            
            return render(request, 'calendarapp/calendar.html', data)

            # context = {
            #     'current_user': current_user,
            #     "event" : event,
            #     "student_record" : student_record, 
            #     "form": form,
            #     "event_title":event_title,
            #     "event_start_time":event_start_time,
            #     "event_end_time":event_end_time}

            # return render(request, 'calendarapp/calendar.html', context)

    def post(self, request):        
        form2 = EventForm(request.POST or None)        
        if request.POST and form2.is_valid():
            # Event Information
            # user = request.session['user']
            current_user = request.session['user']
            confirm_user_id = Users(id_number=current_user)
            current_student = Students(StudentID=confirm_user_id)
            title = form2.cleaned_data["title"]
            description = form2.cleaned_data["description"]
            start_time = form2.cleaned_data["start_time"]
            end_time = form2.cleaned_data["end_time"]
            form2 = Event(StudentID = current_student.StudentID, title = title, description = description, start_time = start_time, end_time = end_time)
            form2.save()
            return redirect('Plan_It_Teknoy:calendar_view')
                
        else:
            print(form2.errors)
            messages.info(request, 'Form error.', extra_tags='try')
            return redirect('Plan_It_Teknoy:calendar_view')

# DashboardView
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        form = EventForm(request.POST or None)

        if 'user' in request.session:
            current_user = request.session['user']
            confirm_user_id = Users(id_number=current_user)
            current_student = Students(StudentID=confirm_user_id)
            event = Event.objects.filter(StudentID=current_student.StudentID)

            # filter [Total Events, Running Events, Completed Events]
            events = Event.objects.get_all_events(StudentID=current_student.StudentID)
            running_events = Event.objects.get_running_events(StudentID=current_student.StudentID)
            completed_events = Event.objects.get_completed_events(StudentID=current_student.StudentID)
            
            # accessing all student records in the database
            student_record = Students.objects.raw('SELECT StudentID_id, first_name, program, last_name, year_level FROM plan_it_teknoy_students WHERE StudentID_id = %s', [current_student.StudentID])
            
            context = {
                        "student_record" : student_record, "form":form, "event":event, "total_event": events,
                        "running_events": running_events,
                        "completed_events": completed_events
                        }

        return render(request, 'calendarapp/dashboard.html', context)
    
class AllEventsListView(ListView):

    # """ All event list views """

    def get(self, request):

        if 'user' in request.session:
            current_user = request.session['user']
            confirm_user_id = Users(id_number=current_user)
            current_student = Students(StudentID=confirm_user_id)
            events = Event.objects.get_all_events(StudentID=current_student.StudentID)



            student_record = Students.objects.raw('SELECT StudentID_id, first_name, program, last_name, year_level FROM plan_it_teknoy_students WHERE StudentID_id = %s', [current_student.StudentID])

            context = {"student_record" : student_record, "total_event":events,
                        "events":events,
                        }

        return render(request, 'calendarapp/events_list.html', context)
        


class RunningEventsListView(ListView):

    # """ Running events list view """
    
    def get(self, request):

           if 'user' in request.session:

            current_user = request.session['user']
            confirm_user_id = Users(id_number=current_user)
            current_student = Students(StudentID=confirm_user_id)
            running_events = Event.objects.get_running_events(StudentID=current_student.StudentID)


            student_record = Students.objects.raw('SELECT StudentID_id, first_name, program, last_name, year_level FROM plan_it_teknoy_students WHERE StudentID_id = %s', [current_student.StudentID])
            
            context = {"student_record" : student_record, "events":running_events, "running_events":running_events}

            return render(request, 'calendarapp/events_list.html', context)

class CompletedEventsListView(ListView):

    def get(self, request):

           if 'user' in request.session:

            current_user = request.session['user']
            confirm_user_id = Users(id_number=current_user)
            current_student = Students(StudentID=confirm_user_id)
            completed_events = Event.objects.get_completed_events(StudentID=current_student.StudentID)


            student_record = Students.objects.raw('SELECT StudentID_id, first_name, program, last_name, year_level FROM plan_it_teknoy_students WHERE StudentID_id = %s', [current_student.StudentID])
            
            context = {"student_record" : student_record, "events":completed_events, "completed_events":completed_events}

            return render(request, 'calendarapp/events_list.html', context)


# user_profile_settings_views
class EditProfileView(View):

    def get(self, request):

            if 'user' in request.session:
                current_user = request.session['user']
                confirm_user_id = Users(id_number=current_user)
                current_student = Students.objects.filter(StudentID=confirm_user_id)
                email_student = Users.objects.filter(id_number=confirm_user_id) 
                
                # student_events = Event.objects.filter(StudentID=current_student.StudentID, end_time__gte=datetime.now().date())
                
                return render(request, 'user_profile_settings/Personal.html', {"current_student":current_student, "email_student":email_student})

        
class EditContactView(View):
    def get(self, request):

        if 'user' in request.session:

                current_user = request.session['user']
                confirm_user_id = Users(id_number=current_user)
                current_student = Students.objects.filter(StudentID=confirm_user_id)
                email_student = Users.objects.filter(id_number=confirm_user_id) 

                return render(request, 'user_profile_settings/Contact.html', {"current_student":current_student, "email_student":email_student})

    
class EditSchoolView(View):
    def get(self, request):

        if 'user' in request.session:

                current_user = request.session['user']
                confirm_user_id = Users(id_number=current_user)
                current_student = Students.objects.filter(StudentID=confirm_user_id)
                email_student = Users.objects.filter(id_number=confirm_user_id) 

        return render(request, 'user_profile_settings/School.html', {"current_student":current_student, "email_student":email_student})

class EditPhotoView(View):
    def get(self, request):
        return render(request, 'user_profile_settings/Photo.html', {})



class EditSecurityView(View):
    def get(self, request):

            if 'user' in request.session:

                current_user = request.session['user']
                confirm_user_id = Users(id_number=current_user)
                current_student = Students.objects.filter(StudentID=confirm_user_id)
                email_student = Users.objects.filter(id_number=confirm_user_id) 


                return render(request, 'user_profile_settings/Security.html', {"current_student":current_student, "email_student":email_student})

class SProfileSettings(View):
    def get(self, request):

            if 'user' in request.session:

                current_user = request.session['user']
                confirm_user_id = Users(id_number=current_user)
                current_student = Students.objects.filter(StudentID=confirm_user_id)
                email_student = Users.objects.filter(id_number=confirm_user_id) 

                return render(request, 'account-settings.html', {"current_student":current_student, "email_student":email_student})

class TProfileSettings(View):
    def get(self, request):

            if 'user' in request.session:

                current_user = request.session['user']
                confirm_user_id = Users(id_number=current_user)
                current_teacher = Teachers.objects.filter(TeacherID=confirm_user_id)
                email_teacher = Users.objects.filter(id_number=confirm_user_id) 

                return render(request, 'account-settings.html', {"current_student":current_teacher, "email_student":email_teacher})

        

    