from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, LeaveApplication
from datetime import date


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with Bootstrap styling."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with role and department fields."""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'department')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['department'].required = True
        
        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
        # Add specific placeholders
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter email address'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter last name'})
        self.fields['department'].widget.attrs.update({'placeholder': 'Enter department'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})


class BaseLeaveApplicationForm(forms.ModelForm):
    """Base form for leave applications."""
    
    class Meta:
        model = LeaveApplication
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Set minimum date to today
        self.fields['start_date'].widget.attrs['min'] = date.today().strftime('%Y-%m-%d')
        self.fields['end_date'].widget.attrs['min'] = date.today().strftime('%Y-%m-%d')
    
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < date.today():
            raise ValidationError("Start date cannot be in the past.")
        return start_date
    
    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date and end_date < date.today():
            raise ValidationError("End date cannot be in the past.")
        return end_date
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date < start_date:
                raise ValidationError("End date must be after start date.")
            
            # Check if user has enough leave days
            if self.user:
                days_requested = (end_date - start_date).days + 1
                if days_requested > self.user.leave_days_remaining:
                    raise ValidationError(
                        f"You only have {self.user.leave_days_remaining} leave days remaining. "
                        f"You requested {days_requested} days."
                    )
        
        return cleaned_data


class StaffLeaveApplicationForm(BaseLeaveApplicationForm):
    """Form for staff members to apply for leave."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason'].help_text = "Please provide a detailed reason for your leave request."


class HODLeaveApplicationForm(BaseLeaveApplicationForm):
    """Form for HOD members to apply for leave."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason'].help_text = "As HOD, please provide reason for your leave request."


class LeaveReviewForm(forms.ModelForm):
    """Form for HOD to review leave applications."""
    
    class Meta:
        model = LeaveApplication
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove 'pending' from choices as it's the default state
        self.fields['status'].choices = [
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ]
