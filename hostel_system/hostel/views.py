# Django Imports
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

# Local Imports
from .forms import ApplicationForm, LoginForm, UserRegistrationForm
from .models import Application, Student


# ----------------------------------------------
# Authentication Views
# ----------------------------------------------
def register(request: HttpRequest):
    """Handle user registration."""
    form = UserRegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                user = User(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                )
                user.set_password(form.cleaned_data["password"])  # Hash the password
                user.save()
                Student.objects.create(user=user)  # Create a Student profile

                messages.success(
                    request, "Registration successful! You can now log in."
                )
                return redirect("login")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "register.html", {"form": form})


def login_view(request: HttpRequest):
    """Handle user login."""
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect(
                "rector_dashboard" if user.is_staff else "student_dashboard"
            )
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html", {"form": form})


def logout_view(request: HttpRequest):
    """Handle user logout."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


# ----------------------------------------------
# Dashboard Views
# ----------------------------------------------
@login_required
def student_dashboard(request: HttpRequest):
    """Render the student dashboard."""
    return render(request, "student_dashboard.html")


@login_required
def reset_password(request: HttpRequest):
    """Render the password reset page."""
    return render(request, "password_reset.html")


@login_required
def rector_dashboard(request: HttpRequest):
    """Render the rector's dashboard with application management."""
    if request.method == "POST":
        return handle_post_request(request)

    applications = Application.objects.all()  # Fetch all applications
    context = categorize_applications(applications)
    return render(request, "rector_dashboard.html", context)


def handle_post_request(request: HttpRequest):
    """Handle POST requests for the rector dashboard."""
    action = request.POST.get("action")
    if action == "save":
        return save_applications(request)
    elif action == "cancel":
        messages.info(request, "No changes were made.")
        return redirect("rector_dashboard")

    # Handle unknown actions
    messages.warning(request, "Unknown action.")
    return redirect("rector_dashboard")


def save_applications(request: HttpRequest):
    """Save accepted or rejected applications."""
    try:
        with transaction.atomic():
            for roll_number in request.POST.keys():
                if roll_number.startswith("action_"):
                    action_value = request.POST[roll_number]
                    roll_number = roll_number.split("_")[1]
                    try:
                        application = Application.objects.get(roll_number=roll_number)
                        application.status = (
                            "accepted" if action_value == "accept" else "rejected"
                        )
                        application.save()
                    except Application.DoesNotExist:
                        messages.warning(
                            request,
                            f"Application with roll number {roll_number} does not exist.",
                        )
                        continue

            messages.success(request, "Applications have been updated.")
    except Exception as e:
        messages.error(request, f"An error occurred while updating: {str(e)}")

    return redirect("rector_dashboard")


def categorize_applications(applications):
    """Categorize applications based on their status."""
    return {
        "pending_applications": applications.filter(status="submitted"),
        "accepted_applications": applications.filter(status="accepted"),
        "rejected_applications": applications.filter(status="rejected"),
    }


# ----------------------------------------------
# Application Views
# ----------------------------------------------
@login_required
def application_create(request):
    """Handle creating a new application."""
    student = get_object_or_404(Student, user=request.user)

    # Check for an existing application (submitted or rejected)
    existing_application = Application.objects.filter(student=student).first()

    # If there is an existing application
    if existing_application:
        # If the previous application was rejected, allow editing
        if existing_application.status == "rejected":
            form = ApplicationForm(request.POST or None, instance=existing_application)
        else:
            messages.warning(
                request, "You already have an application that has not been rejected."
            )
            return redirect(
                "student_dashboard"
            )  # Redirect to student dashboard if they can't reapply
    else:
        form = ApplicationForm(request.POST or None)

    # Handle form submission
    if request.method == "POST":
        if form.is_valid():
            return save_application(
                form, request
            )  # Save the application if form is valid

    # Render the application form
    return render(
        request,
        "application_form.html",
        {
            "form": form,
            "previous_application": existing_application,
        },
    )


def save_application(form, request):
    """Save the application form data."""
    try:
        with transaction.atomic():
            application = form.save(
                commit=False
            )  # Save the form without committing to the database
            application.student = get_object_or_404(Student, user=request.user)

            # If reapplying, clear previous rejection reasons if necessary
            application.rejection_reason = ""  # Clear any rejection reason

            application.status = "submitted"  # Set the status to submitted
            application.save()  # Commit the application to the database
            messages.success(
                request, "Application submitted successfully!"
            )  # Success message
            return redirect(
                "student_dashboard"
            )  # Redirect to student dashboard after successful submission
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")  # Log the error message

    # If there's an error during saving, render the form again
    return render(request, "application_form.html", {"form": form})


@login_required
def application_view(request: HttpRequest):
    """Display applications submitted by the logged-in student."""
    applications = Application.objects.filter(student__user=request.user)
    return render(request, "application_view.html", {"applications": applications})
