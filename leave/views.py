from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO
from datetime import datetime
from .models import User, LeaveApplication
from .forms import (
    CustomUserCreationForm, 
    StaffLeaveApplicationForm, 
    HODLeaveApplicationForm, 
    LeaveReviewForm
)


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard_view(request):
    """Role-based dashboard view."""
    user = request.user
    
    # Get user's applications
    user_applications = LeaveApplication.objects.filter(user=user)
    
    context = {
        'user': user,
        'user_applications': user_applications,
    }
    
    # Add HOD-specific context
    if user.is_hod():
        # Get all pending applications from staff in same department
        pending_applications = LeaveApplication.objects.filter(
            status='pending',
            user__department=user.department
        ).exclude(user=user)
        context['pending_applications'] = pending_applications
    
    return render(request, 'dashboard.html', context)


@login_required
def apply_leave_view(request):
    """Apply for leave view - uses different forms based on user role."""
    user = request.user
    
    # Choose form based on user role
    if user.is_hod():
        form_class = HODLeaveApplicationForm
        template_name = 'hod_leave_form.html'
    else:
        form_class = StaffLeaveApplicationForm
        template_name = 'staff_leave_form.html'
    
    if request.method == 'POST':
        form = form_class(request.POST, user=user)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = user
            application.save()
            
            # Generate PDF
            pdf_file = generate_leave_pdf(application)
            if pdf_file:
                application.pdf_file.save(
                    f'leave_{application.user.username}_{application.id}.pdf',
                    ContentFile(pdf_file.getvalue()),
                    save=True
                )
            
            # Deduct leave days from user's balance
            days_requested = application.days_requested()
            user.leave_days_remaining -= days_requested
            user.save()
            
            messages.success(request, 'Leave application submitted successfully!')
            return redirect('dashboard')
    else:
        form = form_class(user=user)
    
    return render(request, template_name, {'form': form, 'user': user})


@login_required
def review_leave_view(request, application_id):
    """HOD view to review leave applications."""
    if not request.user.is_hod():
        messages.error(request, 'You do not have permission to review applications.')
        return redirect('dashboard')
    
    application = get_object_or_404(LeaveApplication, id=application_id)
    
    # Check if HOD can review this application
    if not application.can_be_reviewed_by(request.user):
        messages.error(request, 'You cannot review this application.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LeaveReviewForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.reviewed_by = request.user
            application.reviewed_date = timezone.now()
            
            # If rejected, restore leave days to user
            if application.status == 'rejected':
                days_requested = application.days_requested()
                application.user.leave_days_remaining += days_requested
                application.user.save()
            
            application.save()
            messages.success(request, f'Application {application.status} successfully!')
            return redirect('dashboard')
    else:
        form = LeaveReviewForm(instance=application)
    
    return render(request, 'review_leave.html', {
        'form': form,
        'application': application
    })


@login_required
def view_pdf(request, application_id):
    """View or download PDF of leave application."""
    application = get_object_or_404(LeaveApplication, id=application_id)
    
    # Check permissions
    if not (request.user == application.user or 
            (request.user.is_hod() and application.user.department == request.user.department)):
        raise Http404("You don't have permission to view this PDF.")
    
    if application.pdf_file:
        response = HttpResponse(application.pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="leave_application_{application.id}.pdf"'
        return response
    else:
        messages.error(request, 'PDF file not found.')
        return redirect('dashboard')


def generate_leave_pdf(application):
    """Generate PDF for leave application."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center alignment
    )
    story.append(Paragraph("LEAVE APPLICATION", title_style))
    story.append(Spacer(1, 20))
    
    # Application details table
    data = [
        ['Employee Name:', f"{application.user.first_name} {application.user.last_name}"],
        ['Department:', application.user.department],
        ['Start Date:', application.start_date.strftime('%Y-%m-%d')],
        ['End Date:', application.end_date.strftime('%Y-%m-%d')],
        ['Days Requested:', str(application.days_requested())],
        ['Reason:', application.reason],
        ['Status:', application.get_status_display()],
        ['Application Date:', application.applied_date.strftime('%Y-%m-%d %H:%M')],
    ]
    
    if application.reviewed_by:
        data.extend([
            ['Reviewed By:', f"{application.reviewed_by.first_name} {application.reviewed_by.last_name}"],
            ['Review Date:', application.reviewed_date.strftime('%Y-%m-%d %H:%M')],
        ])
    
    table = Table(data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 50))
    
    # Signature section
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10,
    )
    story.append(Paragraph("Employee Signature: _____________________", signature_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("HOD Signature: _____________________", signature_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Date: _____________________", signature_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
