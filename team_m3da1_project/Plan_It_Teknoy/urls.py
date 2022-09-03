from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from Plan_It_Teknoy import views

app_name = 'Plan_It_Teknoy'

urlpatterns = [

    # Start of user pages
    path('', views.home, name="Home"),
    path("About/", views.about, name="About"),
    path("Contact/", views.contact, name="Contact"),
    path("SignIn/", views.signin, name="signin"),
    path("SignUp/", views.SignUpView.as_view(), name="signup_view"),
    # End of user pages

    # # icon browser tab
    # path("favicon.ico", RedirectView.as_view(
    #     url=staticfiles_storage.url("favicon.ico"))),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
