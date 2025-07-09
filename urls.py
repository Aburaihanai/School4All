from django.views.generic import TemplateView
from django.urls import path
from schools import admin
from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import school_dashboard
from .views import dashboard


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('schools/', include('schools.urls')),
]


urlpatterns = [
    path('signup/', views.user_signup, name='user_signup'),
    path('login/', views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/manage-users/', views.admin_manage_users, name='admin_manage_users'),
    path('admin/user/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('admin/user/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('admin/fees/add/', views.admin_add_fee, name='admin_add_fee'),
    path('admin/fees/', views.admin_fee_list, name='admin_fee_list'),
    path('admin/fees/unpaid/', views.admin_unpaid_fees, name='admin_unpaid_fees'),
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('redirect/', views.redirect_after_login, name='redirect_after_login'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/enter-result/', views.enter_result, name='enter_result'),
    path('student/<int:id>/results/', views.student_results, name='student_results'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('<int:school_id>/dashboard/', school_dashboard, name='school_dashboard'),
]