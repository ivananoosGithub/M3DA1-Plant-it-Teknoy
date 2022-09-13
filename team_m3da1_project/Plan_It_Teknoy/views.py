from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic import View
from .forms import *
from .models import *
from passlib.hash import pbkdf2_sha256
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

# Select Role Page
class SelectRoleView(View):
    def get(self, request):
        return render(request, 'signup-role.html', {})

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
            id_number = request.POST.get('id_number')
            email = request.POST.get("email")
            password = request.POST.get('password')
            check_password = pbkdf2_sha256.hash(password, rounds=20000, salt_size=16)
            dec_password = pbkdf2_sha256.verify(password, check_password)
            check_id = Users.objects.filter(id_number=id_number)
            check_email = Users.objects.filter(email=email)
            if check_id and dec_password and check_email:
                request.session['user'] = id_number
                if Users.objects.filter(id_number=id_number).count()>0:
                    return redirect('Plan_It_Teknoy:dashboard_view')
            else:
                messages.info(request, 'Incorrect ID Number and Email and Password!')
                return redirect('Plan_It_Teknoy:signin_view') 
        return redirect('Plan_It_Teknoy:Home')

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
            event = Event.objects.filter(StudentID = current_student.StudentID)
            
            #accessing all student records in the database
            student_record = Students.objects.raw('SELECT StudentID_id, first_name, program, last_name, year_level FROM plan_it_teknoy_students WHERE StudentID_id = %s', [current_student.StudentID])
            
            context = {
                'current_user': current_user,
                "event" : event,
                "student_record" : student_record, 
                "form": form,}
            return render(request, 'calendarapp/calendar.html', context)

    def post(self, request):        
        form2 = EventForm(request.POST or None)        
        if request.POST and form2.is_valid():
            # Event Information
            user = request.session['user']
            title = form2.cleaned_data["title"]
            description = form2.cleaned_data["description"]
            start_time = form2.cleaned_data["start_time"]
            end_time = form2.cleaned_data["end_time"]
            form2 = Event(StudentID = user, title = title, description = description, start_time = start_time, end_time = end_time)
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

            # filter [Total Events, Running Events,]
            events = Event.objects.get_all_events(StudentID=current_student.StudentID)
            running_events = Event.objects.get_running_events(StudentID=current_student.StudentID)
            completed_events = Event.objects.get_completed_events(StudentID=current_student.StudentID)
            
            # accessing all student records in the database
            student_record = Students.objects.raw('SELECT StudentID_id, first_name, program, last_name, year_level FROM plan_it_teknoy_students WHERE StudentID_id = %s', [current_student.StudentID])
            
            context = {
                        "student_record" : student_record, "form":form, "event":event, "total_event": events.count(),
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
            all_events = Event.objects.get_all_events(StudentID=current_student.StudentID)

        return render(request, 'calendarapp/events_list.html', {"all_events":all_events})
        


class RunningEventsListView(ListView):

    # """ Running events list view """
    
    def get(self, request):

           if 'user' in request.session:

            current_user = request.session['user']
            confirm_user_id = Users(id_number=current_user)
            current_student = Students(StudentID=confirm_user_id)
            all_events = Event.objects.get_running_events(StudentID=current_student.StudentID)

            return render(request, 'calendarapp/events_list.html', {"all_events":all_events})

class CompletedEventsListView(ListView):

    def get(self, request):

           if 'user' in request.session:

            current_user = request.session['user']
            confirm_user_id = Users(id_number=current_user)
            current_student = Students(StudentID=confirm_user_id)
            all_events = Event.objects.get_completed_events(StudentID=current_student.StudentID)

            return render(request, 'calendarapp/events_list.html', {"all_events":all_events})



        

    