from django.urls import path
from . import views


urlpatterns = [
    # Authentication
    path("", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # Student Dashboard
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/apply/", views.application_create, name="apply"),
    path("student/view/", views.application_view, name="view"),
    
    # Rector Dashboard
    path("rector/dashboard/", views.rector_dashboard, name="rector_dashboard"),
]
