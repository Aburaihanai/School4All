from django.db import models
from django.contrib.auth.models import User
from schools.models import School  # ✅ ADD THIS import
from django.conf import settings

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    contact_email = models.EmailField(blank=True, null=True)
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children',
        limit_choices_to={'userprofile__role': 'parent'}
    )

    def __str__(self):
        return f"{self.user.username} ({self.role}) - {self.school.name}"

class FeeRecord(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    term = models.CharField(max_length=100)
    date_recorded = models.DateField(auto_now_add=True)

    def balance(self):
        return self.amount_due - self.amount_paid

    def __str__(self):
        return f"{self.student.user.username} - {self.term}"

class Result(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    subject = models.CharField(max_length=100)
    term = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='staff_results')

    def __str__(self):
        return f"{self.student.user.username} - {self.subject} - {self.term}"

# models.py
class School(models.Model):
    name = models.CharField(max_length=100)
    ...

class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    ...

class Staff(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    ...

class Fee(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.CharField(max_length=20, choices=[
        ('1st Term', '1st Term'),
        ('2nd Term', '2nd Term'),
        ('3rd Term', '3rd Term'),
    ])

class Gallery(models.Model):
    school = models.ForeignKey(School, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='school_gallery/')
