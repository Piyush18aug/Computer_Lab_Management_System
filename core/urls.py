from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('it-dashboard/', views.it_dashboard, name='it_dashboard'),
    path('update-status/<int:issue_id>/', views.update_issue_status, name='update_issue_status'),
    path('completed-issues/', views.completed_issues, name='completed_issues'),
    path('delete-issue/<int:issue_id>/', views.delete_issue, name='delete_issue'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('reset-visit-count/', views.reset_visit_count, name='reset_visit_count'),
]
