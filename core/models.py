from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('it', 'IT Department'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    visit_count = models.IntegerField(default=0)

class Issue(models.Model):
    CATEGORY_CHOICES = (
        ('mouse', 'Mouse'),
        ('keyboard', 'Keyboard'),
        ('software', 'Software'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')
    lab_number = models.CharField(max_length=10)
    pc_number = models.CharField(max_length=10)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    image = models.ImageField(upload_to='issue_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.category} - {self.status}"
