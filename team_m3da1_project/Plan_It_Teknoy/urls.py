from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from Plan_It_Teknoy import views

app_name = 'Plan_It_Teknoy'

urlpatterns = [

    # Start of user pages
    path('', views.home, name="Home"),
    path('logout/', views.logout, name='logout'),
    path("About/", views.about, name="About"),
    path("Contact/", views.contactView.as_view(), name="contact_view"),
    path("SignIn/", views.SignInView.as_view(), name="signin_view"),
    path("StudentSignUp/", views.SignUpStudentView.as_view(), name="signupS_view"),
    path("TeacherSignUp/", views.SignUpTeacherView.as_view(), name="signupT_view"),
    # Select Role url
    path("SelectRole/", views.SelectRoleView.as_view(), name="select_view"),
    # Main Page url
    path("Calendar/", views.CalendarViewNew.as_view(), name="calendar"),
    # Dashboard url
    path("Dashboard/", views.DashboardView.as_view(), name="dashboard"),

    # End of user pages

    # # icon browser tab
    # path("favicon.ico", RedirectView.as_view(
    #     url=staticfiles_storage.url("favicon.ico"))),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
