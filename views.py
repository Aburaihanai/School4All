from pyexpat.errors import messages
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from schools import models
from .forms import AdminEditUserForm, FeeRecordForm, ResultForm, UserSignupForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import AdminCreateUserForm
from django.shortcuts import get_object_or_404
from .models import FeeRecord
from django.db.models import Q
from .models import UserProfile, FeeRecord
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Result
from django.shortcuts import render, get_object_or_404
from .models import School, Student, Staff, Fee
from django.db.models import Sum

def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            profile = UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                school=form.cleaned_data['school']
            )
            login(request, user)
            return redirect('dashboard')  # You’ll define this later
    else:
        form = UserSignupForm()
    return render(request, 'users/signup.html', {'form': form})
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = user.userprofile.role
            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'staff':
                return redirect('staff_dashboard')
            elif role == 'student':
                return redirect('student_dashboard')
            elif role == 'parent':
                return redirect('parent_dashboard')
            return redirect('dashboard')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'users/login.html')

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html', {'user': request.user})
@login_required
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')

@login_required
def staff_dashboard(request):
    return render(request, 'users/staff_dashboard.html')

@login_required
def student_dashboard(request):
    return render(request, 'users/student_dashboard.html')

@login_required
def parent_dashboard(request):
    return render(request, 'users/parent_dashboard.html')

@login_required
def admin_create_user(request):
      if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("You are not allowed here.")

@login_required
def admin_create_user(request):
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("You are not allowed here.")

@login_required
def admin_manage_users(request):
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("Access denied.")

    school = request.user.userprofile.school
    users = UserProfile.objects.filter(school=school)

    return render(request, 'users/admin_manage_users.html', {'users': users})

@login_required
def admin_edit_user(request, user_id):
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("Access denied.")

    user = get_object_or_404(User, id=user_id)
    profile = user.userprofile

    # Ensure same school
    if profile.school != request.user.userprofile.school:
        return HttpResponseForbidden("You can't edit users from another school.")

    if request.method == 'POST':
        form = AdminEditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            profile.role = form.cleaned_data['role']
            profile.save()
            return redirect('admin_manage_users')
    else:
        form = AdminEditUserForm(instance=user, initial={'role': profile.role})

    return render(request, 'users/admin_edit_user.html', {'form': form, 'user_id': user.id})

@login_required
def admin_delete_user(request, user_id):
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("Access denied.")

    user = get_object_or_404(User, id=user_id)
    profile = user.userprofile

    if profile.school != request.user.userprofile.school:
        return HttpResponseForbidden("You can't delete users from another school.")

    user.delete()
    return redirect('admin_manage_users')

@login_required
def admin_add_fee(request):
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("Access denied.")

    school = request.user.userprofile.school
    form = FeeRecordForm()
    form.fields['student'].queryset = UserProfile.objects.filter(role='student', school=school)

    if request.method == 'POST':
        form = FeeRecordForm(request.POST)
        form.fields['student'].queryset = UserProfile.objects.filter(role='student', school=school)
        if form.is_valid():
            form.save()
            return redirect('admin_fee_list')

    return render(request, 'users/admin_add_fee.html', {'form': form})

@login_required
def admin_fee_list(request):
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("Access denied.")

    school = request.user.userprofile.school
    fees = FeeRecord.objects.filter(student__school=school)

    return render(request, 'users/admin_fee_list.html', {'fees': fees})

@login_required
def admin_unpaid_fees(request):
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("Access denied.")

    school = request.user.userprofile.school
    # Get fee records with balance > 0
    unpaid_fees = FeeRecord.objects.filter(
        student__school=school
    ).filter(amount_paid__lt=models.F('amount_due'))

    return render(request, 'users/admin_unpaid_fees.html', {'fees': unpaid_fees})

@login_required
def admin_create_user(request):
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden("You are not allowed here.")
    
    school = request.user.userprofile.school

    if request.method == 'POST':
        form = AdminCreateUserForm(request.POST)
        form.fields['parent'].queryset = User.objects.filter(userprofile__role='parent', userprofile__school=school)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                school=school,
                parent=form.cleaned_data.get('parent')
            )
            return render(request, 'users/create_user_success.html')
    else:
        form = AdminCreateUserForm()
        form.fields['parent'].queryset = User.objects.filter(userprofile__role='parent', userprofile__school=school)

    return render(request, 'users/admin_create_user.html', {'form': form})

@login_required
def parent_dashboard(request):
    if request.user.userprofile.role != 'parent':
        return HttpResponseForbidden("Access denied.")

    children_profiles = UserProfile.objects.filter(parent=request.user)
    fees = FeeRecord.objects.filter(student__in=children_profiles)

    return render(request, 'users/parent_dashboard.html', {
        'children': children_profiles,
        'fees': fees,
    })

@login_required
def redirect_after_login(request):
    role = request.user.userprofile.role
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'parent':
        return redirect('parent_dashboard')
    elif role == 'staff':
        return redirect('staff_dashboard')  # create this later
    else:
        return redirect('student_dashboard')  # create this later

@login_required
def staff_dashboard(request):
    if request.user.userprofile.role != 'staff':
        return HttpResponseForbidden("Access denied.")

    return render(request, 'users/staff_dashboard.html')

@login_required
def enter_result(request):
    if request.user.userprofile.role != 'staff':
        return HttpResponseForbidden("Access denied.")

    school = request.user.userprofile.school
    form = ResultForm()
    form.fields['student'].queryset = UserProfile.objects.filter(school=school, role='student')

    if request.method == 'POST':
        form = ResultForm(request.POST)
        form.fields['student'].queryset = UserProfile.objects.filter(school=school, role='student')
        if form.is_valid():
            result = form.save(commit=False)
            result.added_by = request.user
            result.save()
            return redirect('staff_dashboard')

    return render(request, 'users/enter_result.html', {'form': form})

@login_required
def redirect_after_login(request):
    role = request.user.userprofile.role
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'parent':
        return redirect('parent_dashboard')
    elif role == 'staff':
        return redirect('staff_dashboard')
    else:
        return redirect('student_dashboard')


@login_required(login_url='/')  # ✅ Redirect to homepage instead
def student_results(request, id):
    student_name = "Ahmad Sulaiman"
    results = {
        "Math": 85,
        "English": 72,
        "Islamic Studies": 95,
    }
    return render(request, 'users/student_results.html', {
        'student_name': student_name,
        'results': results,
    })


@login_required(login_url='/')
def school_dashboard(request, school_id):
    school = get_object_or_404(School, id=school_id)

    total_students = Student.objects.filter(school=school).count()
    total_staff = Staff.objects.filter(school=school).count()
    total_fees_collected = Fee.objects.filter(school=school).aggregate(total=Sum('amount'))['total'] or 0

    gallery_images = school.gallery_images.all()

    # ✅ Fee totals per term
    fee_by_term = Fee.objects.filter(school=school).values('term').annotate(total=Sum('amount'))

    chart_labels = []
    chart_data = []

    for item in fee_by_term:
        chart_labels.append(item['term'])
        chart_data.append(float(item['total']))

    context = {
        'school': school,
        'total_students': total_students,
        'total_staff': total_staff,
        'total_fees_collected': total_fees_collected,
        'gallery_images': gallery_images,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }

    return render(request, 'schools/school_dashboard.html', context)

def school_dashboard(request, school_id):
    school = get_object_or_404(School, id=school_id)
    return render(request, 'schools/dashboard.html', {'school': school})
