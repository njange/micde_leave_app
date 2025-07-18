# 🚀 MICDE Leave Application Web App

A comprehensive Django web application for managing employee leave requests with role-based access control and PDF generation.

## ✨ Features

✅ **Custom User Model** - Two roles: 'staff' and 'hod' (Head of Department)
✅ **Department Management** - Users assigned to departments with leave days tracking
✅ **Role-Based Forms** - Different forms for staff and HOD leave applications
✅ **Leave Request Management** - Save applications with start_date, end_date, reason, and status
✅ **Approval Workflow** - HOD users can view and approve/reject staff leave requests
✅ **PDF Generation** - Automatic PDF generation using ReportLab for each application
✅ **Authentication System** - Django built-in auth with custom login/registration
✅ **Role-Based Dashboards** - Different dashboards for staff and HOD users
✅ **Auto-Fill Forms** - Forms pre-populate with user data (name, department, leave days)
✅ **SQLite Database** - Lightweight database for development
✅ **Bootstrap UI** - Clean and responsive user interface

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite
- **PDF Generation**: ReportLab
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Authentication**: Django built-in auth system
- **Environment**: Python Virtual Environment

## 📋 Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Clone and Setup
```bash
cd /home/njange/Projects/micde_leave_app
```

### 3. Activate Virtual Environment
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Create Sample Data (Optional)
```bash
python manage.py shell < create_sample_data.py
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 👥 Sample User Accounts

The following test accounts are available (password: `password123`):

### Staff Users
- **Username**: `john_staff` (Engineering Department)
- **Username**: `bob_staff` (Marketing Department)

### HOD Users
- **Username**: `jane_hod` (Engineering Department)
- **Username**: `alice_hod` (Marketing Department)

## 🎯 Usage Guide

### For Staff Users:
1. **Login** with staff credentials
2. **View Dashboard** to see leave balance and submitted applications
3. **Apply for Leave** using the staff leave form
4. **View PDF** of submitted applications
5. **Track Status** of applications (Pending/Approved/Rejected)

### For HOD Users:
1. **Login** with HOD credentials
2. **View Dashboard** to see personal applications and pending staff requests
3. **Apply for Leave** using the HOD leave form (with additional coverage checklist)
4. **Review Applications** from staff in their department
5. **Approve/Reject** leave requests
6. **View PDFs** of all applications

### Admin Users:
1. **Access Django Admin** at `/admin/`
2. **Manage Users** - Create, edit, and delete user accounts
3. **Manage Leave Applications** - View and modify all leave requests
4. **Department Management** - Organize users by departments

## 📁 Project Structure

```
micde_leave_app/
├── manage.py
├── requirements.txt
├── README.md
├── create_sample_data.py
├── db.sqlite3
├── micde_leave_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── leave/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── migrations/
│   └── tests.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── staff_leave_form.html
│   ├── hod_leave_form.html
│   ├── review_leave.html
│   └── registration/
│       ├── login.html
│       └── register.html
├── static/
│   └── css/
│       └── style.css
└── media/
    └── leave_pdfs/
```

## 🔧 Key Features Explained

### Role-Based Access Control
- **Staff**: Can apply for leave and view their own applications
- **HOD**: Can apply for leave AND review/approve staff applications in their department

### PDF Generation
- Automatic PDF generation using ReportLab
- Professional template with application details
- Stored in filesystem under `media/leave_pdfs/`

### Leave Days Management
- Each user starts with 21 leave days
- Days are deducted when application is submitted
- Days are restored if application is rejected
- Real-time balance tracking

### Form Validation
- Start date cannot be in the past
- End date must be after start date
- Cannot request more days than available balance
- Different validation rules for staff and HOD

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Bootstrap 5**: Modern and clean interface
- **Font Awesome Icons**: Intuitive iconography
- **Color-coded Status**: Visual indication of application status
- **Interactive Forms**: Client-side validation and date pickers
- **Dashboard Cards**: Information at a glance

## 🔒 Security Features

- **CSRF Protection**: All forms protected against CSRF attacks
- **User Authentication**: Required for all application pages
- **Role-based Views**: Users can only access appropriate content
- **File Access Control**: PDF files only accessible to authorized users

## 📊 Database Models

### User Model
- Extends Django's AbstractUser
- Additional fields: role, department, leave_days_remaining

### LeaveApplication Model
- Tracks all leave requests
- Status workflow: pending → approved/rejected
- Automatic PDF generation and storage

## 🚀 Future Enhancements

- [ ] Email notifications for application status changes
- [ ] Calendar integration for leave visualization
- [ ] Advanced reporting and analytics
- [ ] Multiple approval levels
- [ ] Leave types (sick, vacation, personal)
- [ ] Bulk operations for HOD users
- [ ] API endpoints for mobile app integration

## 🐛 Troubleshooting

### Common Issues:
1. **Migration Errors**: Run `python manage.py migrate` after model changes
2. **Static Files**: Run `python manage.py collectstatic` for production
3. **PDF Generation**: Ensure ReportLab is installed correctly
4. **Permission Errors**: Check media directory permissions

### Development Tips:
- Use `python manage.py check` to validate configuration
- Set `DEBUG=True` in settings.py for development
- Use Django Admin for quick data management
- Check terminal output for detailed error messages

## 📝 License

This project is developed for educational purposes as part of the MICDE Leave Application system.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Happy Coding!** 🎉
