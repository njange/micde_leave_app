from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """Custom user model with role-based permissions."""
    
    ROLE_CHOICES = [
        ('staff', 'Staff'),
        ('hod', 'Head of Department'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')
    department = models.CharField(max_length=100, blank=True)
    leave_days_remaining = models.PositiveIntegerField(
        default=21,
        validators=[MinValueValidator(0)]
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_hod(self):
        return self.role == 'hod'
    
    def is_staff_member(self):
        return self.role == 'staff'


class LeaveApplication(models.Model):
    """Model for leave applications."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_applications')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    reviewed_date = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )
    pdf_file = models.FileField(upload_to='leave_pdfs/', blank=True, null=True)
    
    class Meta:
        ordering = ['-applied_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.start_date} to {self.end_date}"
    
    def days_requested(self):
        """Calculate number of days requested."""
        return (self.end_date - self.start_date).days + 1
    
    def can_be_reviewed_by(self, user):
        """Check if a user can review this application."""
        return user.is_hod() and user != self.user
