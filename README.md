# 🚀 MICDE Leave Application Web App Setup Prompt

# I want to build a Django web application with the following features:
# 1. Custom user model with 2 roles: 'staff' and 'hod'
# 2. Each user should have department info and leave_days_remaining field
# 3. Staff and HOD can both apply for leave but using different forms
# 4. Leave applications should be saved in the database with start_date, end_date, reason, status
# 5. HOD users should also be able to view and approve/reject leave requests submitted by staff
# 6. After submitting, a PDF should be generated using a template and saved in the filesystem
# 7. Use Django built-in auth, SQLite for the database, and a clean project/app structure
# 8. Include a simple login page, and role-based dashboards
# 9. Leave forms should autofill user data like name, department, remaining leave days
# 10. Set up everything using `venv`, and include a requirements.txt file

# 🛠 Use Django best practices, and create one main app called `leave`
# ✅ After scaffolding, generate models, forms, views, and sample templates for:
# - staff_leave_form.html
# - hod_leave_form.html
# - leave_pdf_template.html
