from django.urls import path
from . import views


# app_name = 'Plan_It_Teknoy'

urlpatterns = [

    # Start of user pages
    path('', views.home, name="Home"),
    path("About", views.about, name="About"),
    path("Contact", views.contact, name="Contact"),
    path("Sign in", views.signin, name="Sign in"),
    path("Sign up", views.signup, name="Sign up"),

    # End of user pages

    # # icon browser tab
    # path("favicon.ico", RedirectView.as_view(
    #     url=staticfiles_storage.url("favicon.ico"))),


]
