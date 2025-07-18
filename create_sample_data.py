#!/usr/bin/env python
"""
Sample data creation script for MICDE Leave Application
Run this with: python manage.py shell < create_sample_data.py
"""

from leave.models import User

# Create sample users
users_data = [
    {
        'username': 'john_staff',
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'role': 'staff',
        'department': 'Engineering',
        'password': 'password123'
    },
    {
        'username': 'jane_hod',
        'email': 'jane@example.com',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'role': 'hod',
        'department': 'Engineering',
        'password': 'password123'
    },
    {
        'username': 'bob_staff',
        'email': 'bob@example.com',
        'first_name': 'Bob',
        'last_name': 'Johnson',
        'role': 'staff',
        'department': 'Marketing',
        'password': 'password123'
    },
    {
        'username': 'alice_hod',
        'email': 'alice@example.com',
        'first_name': 'Alice',
        'last_name': 'Brown',
        'role': 'hod',
        'department': 'Marketing',
        'password': 'password123'
    }
]

print("Creating sample users...")
for user_data in users_data:
    password = user_data.pop('password')
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults=user_data
    )
    if created:
        user.set_password(password)
        user.save()
        print(f"Created user: {user.username} ({user.get_role_display()})")
    else:
        print(f"User already exists: {user.username}")

print("Sample data creation completed!")
