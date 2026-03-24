from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Issue

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'visit_count', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'visit_count')}),
    )

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'lab_number', 'pc_number', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('student__username', 'description', 'lab_number')
    list_editable = ('status',)
