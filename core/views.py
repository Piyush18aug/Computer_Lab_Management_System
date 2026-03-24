from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .models import Issue, User
from .forms import IssueForm

def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('student_dashboard')
        elif request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'it':
            return redirect('it_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'student':
                user.visit_count += 1
                user.save()
                return redirect('student_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'it':
                return redirect('it_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('login')
    
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.student = request.user
            issue.save()
            return redirect('student_dashboard')
    else:
        form = IssueForm()
    
    issues = Issue.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'student_dashboard.html', {'form': form, 'issues': issues})

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    issues = Issue.objects.all().order_by('-priority', '-created_at')
    total_student_visits = User.objects.filter(role='student').aggregate(Sum('visit_count'))['visit_count__sum'] or 0
    return render(request, 'admin_dashboard.html', {'issues': issues, 'total_student_visits': total_student_visits})

@login_required
def it_dashboard(request):
    if request.user.role != 'it':
        return redirect('login')
    
    issues = Issue.objects.filter(status='pending').order_by('-priority', '-created_at')
    return render(request, 'it_dashboard.html', {'issues': issues})

@login_required
def update_issue_status(request, issue_id):
    if request.user.role not in ['admin', 'it']:
        return redirect('login')
    
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'completed']:
            issue.status = new_status
            issue.save()
    
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('it_dashboard')

@login_required
def completed_issues(request):
    if request.user.role not in ['admin', 'it']:
        return redirect('login')
    
    issues = Issue.objects.filter(status='completed').order_by('-priority', '-created_at')
    return render(request, 'completed_issues.html', {'issues': issues})

@login_required
def delete_issue(request, issue_id):
    if request.user.role != 'admin':
        return redirect('login')
    
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == 'POST':
        issue.delete()
    
    return redirect('admin_dashboard')

@login_required
def analytics_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    # Aggregate data
    status_data = Issue.objects.values('status').annotate(count=Count('status'))
    priority_data = Issue.objects.values('priority').annotate(count=Count('priority'))
    category_data = Issue.objects.values('category').annotate(count=Count('category'))
    
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    
    context = {
        'status_data': json.dumps(list(status_data), cls=DjangoJSONEncoder),
        'priority_data': json.dumps(list(priority_data), cls=DjangoJSONEncoder),
        'category_data': json.dumps(list(category_data), cls=DjangoJSONEncoder),
    }
    return render(request, 'analytics.html', context)

@login_required
def reset_visit_count(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    if request.method == 'POST':
        User.objects.filter(role='student').update(visit_count=0)
    
    return redirect('admin_dashboard')
