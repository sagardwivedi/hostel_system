from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Student: {self.user.username}"


class Rector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rector: {self.user.username}"


class Application(models.Model):
    CASTE_CHOICES = [
        ("general", "General"),
        ("obc", "Other Backward Class"),
        ("sc", "Scheduled Caste"),
        ("st", "Scheduled Tribe"),
        ("other", "Others"),
    ]

    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=100)
    cet_marks = models.DecimalField(max_digits=5, decimal_places=2)
    caste = models.CharField(max_length=10, choices=CASTE_CHOICES)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="submitted"
    )
    rejection_reason = models.TextField(blank=True, null=True)
    last_application_date = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.cet_marks < 0 or self.cet_marks > 100:
            raise ValidationError("CET marks must be between 0 and 100.")

    def __str__(self):
        return f"Application by {self.name} (Roll No: {self.roll_number}), Status: {self.status}"
