from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, LeaveApplication


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin for User model."""
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'department', 'leave_days_remaining'),
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'department', 'leave_days_remaining'),
        }),
    )
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'leave_days_remaining')
    list_filter = ('role', 'department', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'department')


@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    """Admin for LeaveApplication model."""
    
    list_display = ('user', 'start_date', 'end_date', 'days_requested', 'status', 'applied_date', 'reviewed_by')
    list_filter = ('status', 'start_date', 'end_date', 'applied_date', 'user__department')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'reason')
    readonly_fields = ('applied_date', 'reviewed_date', 'days_requested')
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('user',)
        }),
        ('Leave Details', {
            'fields': ('start_date', 'end_date', 'reason', 'status')
        }),
        ('Review Information', {
            'fields': ('reviewed_by', 'reviewed_date'),
            'classes': ('collapse',)
        }),
        ('File', {
            'fields': ('pdf_file',)
        }),
        ('Timestamps', {
            'fields': ('applied_date',),
            'classes': ('collapse',)
        }),
    )
    
    def days_requested(self, obj):
        return obj.days_requested()
    days_requested.short_description = 'Days Requested'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'reviewed_by')
