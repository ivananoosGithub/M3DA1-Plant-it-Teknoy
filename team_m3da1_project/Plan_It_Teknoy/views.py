from django.shortcuts import render
from .forms import*



#################################### Start of user pages ###################################


# Home and Landing Page
def home(response):
    return render(response, "Plan_It_Teknoy/User/Home.html", {})

# About Us Page
def about(response):
    return render(response, "Plan_It_Teknoy/User/About.html", {})
    
# Contact Us page
def contact(response):
    return render(response, "Plan_It_Teknoy/User/Contact.html", {})