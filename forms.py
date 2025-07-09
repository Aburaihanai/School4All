from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from schools.models import School
from .models import Result


class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    school = forms.ModelChoiceField(queryset=School.objects.all())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
class AdminCreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    parent = forms.ModelChoiceField(
        queryset=User.objects.filter(userprofile__role='parent'),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'password']

class AdminEditUserForm(forms.ModelForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username']

from .models import FeeRecord

class FeeRecordForm(forms.ModelForm):
    class Meta:
        model = FeeRecord
        fields = ['student', 'amount_due', 'amount_paid', 'term']

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'term', 'score']
