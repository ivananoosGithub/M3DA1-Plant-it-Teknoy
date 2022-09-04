from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic import View
from .forms import *
from .models import *
from passlib.hash import pbkdf2_sha256


#################################### Start of user pages ###################################


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
        return render(request, "signin.html", {})
    
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
                    return redirect('Plan_It_Teknoy:Home')
            else:
                messages.info(request, 'Incorrect ID Number and Email and Password!')
                return redirect('Plan_It_Teknoy:signin_view') 
        return redirect('Plan_It_Teknoy:Home')

# Sign up page
class SignUpView(View):
    def get(self, request):
        #  if 'user' in request.session:
        #      current_user = request.session['user']
        #      users = Users.objects.all()
        #      context = {
        #          'current_user': current_user,
        #          'users' : users,
        #      }
        #      return render(request, 'signup.html', context)
        #  else:
            return render(request, 'signup.html', {})

    def post(self, request):        
        form = UsersForm(request.POST, request.FILES)        
        if form.is_valid():
            # try:
            id_number = request.POST.get("id_number")
            password = request.POST.get("password")
            confirmpassword = request.POST.get("cpassword")
            enc_password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
            email = request.POST.get("email")
            if(confirmpassword == password):
                if Users.objects.filter(id_number=id_number).count()>0:
                    messages.info(request, 'ID Number already exists!')
                    return redirect('Plan_It_Teknoy:signup_view') 
                else:
                    form = Users(id_number = id_number, password = enc_password, email = email)
                    form.save()
                    check_user = Users.objects.filter(id_number=id_number, password=enc_password, email = email)
                    if check_user:
                        request.session['user'] = id_number
                        return redirect('Plan_It_Teknoy:signin_view')
            else:
                messages.info(request, 'Passwords do not match!', extra_tags='signin')
                return redirect('Plan_It_Teknoy:signup_view')
        else:
            print(form.errors)
            messages.info(request, 'Account already exists! Please try another unique one.', extra_tags='try')
            return redirect('Plan_It_Teknoy:signup_view')

# Select Role Page
class SignupTeacherView(View):
    def get(self, request):
        return render(request, 'signup-teacher.html', {})