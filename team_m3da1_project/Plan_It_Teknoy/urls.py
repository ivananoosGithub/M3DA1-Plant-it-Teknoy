from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from Plan_It_Teknoy import views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy


app_name = 'Plan_It_Teknoy'

urlpatterns = [

    # Start of user pages
    path('', views.home, name="Home"),
    # for login microsoft
    path('microsoft_authentication/', include('microsoft_authentication.urls')),
    path('index/', views.IndexView.as_view(), name="index_view"),
    
    path('logout/', views.microsoft_logout, name="Logout"),
    # end of addition
    # path('logout/', views.logout, name='logout'),
    path("About/", views.about, name="About"),
    path("Contact/", views.contactView.as_view(), name="contact_view"),
    path("SignIn/", views.SignInView.as_view(), name="signin_view"),
    path("StudentSignUp/", views.SignUpStudentView.as_view(), name="signupS_view"),
    path("TeacherSignUp/", views.SignUpTeacherView.as_view(), name="signupT_view"),
    # Select Role url
    path("SelectRole/", views.SelectRoleView.as_view(), name="select_view"),
    # Main Page url
    path("Calendar/", views.CalendarViewNew.as_view(), name="calendar_view"),
    # Dashboard url
    path("Dashboard/", views.DashboardView.as_view(), name="dashboard_view"),

    # End of user pages

    # icon browser tab
    path("favicon.ico", RedirectView.as_view(
        url=staticfiles_storage.url("favicon.ico"))),

    path("All Events/", views.AllEventsListView.as_view(), name="all_events"),
    path(
        "Running Events/",
        views.RunningEventsListView.as_view(),
        name="running_events",
    ),
    path("Completed Events/", views.CompletedEventsListView.as_view(), name="completed_events"),

    # student profile settings try
    path("student-profile/", views.SProfileSettings.as_view(), name="sprofile-settings_view"),
    # teacher profile settings try
    path("teacher-profile/", views.TProfileSettings.as_view(), name="tprofile-settings_view"),

        # Forgot Password url
    path("ForgotPassword/", views.ForgotPasswordView.as_view(), name="fp_view"),
    path("ForgotPassword/<code>/", views.ChangePasswordSentView.as_view(), name="fpt_view"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
