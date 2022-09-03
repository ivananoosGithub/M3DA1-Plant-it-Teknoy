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
    
# Contact Us page
def contact(response):
    return render(response, "Contact.html", {})

# Sign in page
def signin(response):
    return render(response, "SignIn.html", {})

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
                        return redirect('Plan_It_Teknoy:Home')
            else:
                messages.info(request, 'Passwords do not match!', extra_tags='signin')
                return redirect('Plan_It_Teknoy:signup_view')
        else:
            print(form.errors)
            messages.info(request, 'Account already exists! Please try another unique one.', extra_tags='try')
            return redirect('Plan_It_Teknoy:signup_view')