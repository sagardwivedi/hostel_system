from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import ApplicationForm, LoginForm, UserRegistrationForm
from .models import Application, Student


def register(request: HttpRequest):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = form.cleaned_data["username"]

            # Create a new user with the email as the username
            user = User(username=username, email=email)
            user.set_password(password)  # Hash the password
            user.save()

            # Create a Student profile for the new user
            Student.objects.create(user=user)
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})


def login_view(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(request.POST)
        print(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(
                    request, "Login successful!"
                )  # Optional success message
                if user.is_staff:
                    return redirect("rector_dashboard")
                else:
                    return redirect("student_dashboard")
            else:
                form.add_error(None, "Invalid credentials")  # Add non-field error
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("login")


@login_required
def student_dashboard(request: HttpRequest):
    return render(request, "student_dashboard.html")


@login_required
def rector_dashboard(request: HttpRequest):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "save":
            for application in Application.objects.all():
                print(request.POST)
                accept_checkbox = request.POST.get(f"accept_{application.roll_number}")
                reject_checkbox = request.POST.get(f"reject_{application.roll_number}")
                print("Accept", accept_checkbox)
                print("Reject", reject_checkbox)
                if accept_checkbox and not reject_checkbox:
                    application.status = "Accepted"
                    application.save()
                elif reject_checkbox and not accept_checkbox:
                    application.status = "Rejected"
                    application.save()

            messages.success(request, "Applications have been updated.")
        elif action == "cancel":
            messages.info(request, "No changes were made.")

        return redirect("rector_dashboard")

    else:
        applications = Application.objects.all()  # Fetch all applications
        return render(request, "rector_dashboard.html", {"applications": applications})


@login_required
def application_create(request: HttpRequest):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = Student.objects.get(
                user=request.user
            )  # Link to the logged-in student
            application.save()  # Save the application data to the database
            messages.success(request, "Application submitted successfully!")
            return redirect("student_dashboard")
    else:
        form = ApplicationForm()
    return render(request, "application_form.html", {"form": form})


@login_required
def application_view(request):
    # Assuming you want to display the applications for the logged-in student
    applications = Application.objects.filter(student__user=request.user)
    return render(request, "application_view.html", {"applications": applications})
