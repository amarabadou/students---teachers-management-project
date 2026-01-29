# Student & Teacher Management System

A Python-based management system for handling students, teachers, and schedules using a local MySQL database.

## Features
- Admin, Student, and Teacher login system
- Students and teachers management
- admin can add update delete students / admin can add update delete teachers
- Teachers can add lessons in PDF format
- Students can view the lessons and view the schedule
- Schedule management
- PDF generation for reports

## Technologies
- Python
- MySQL
- phpMyAdmin

## Authentication Design
- This project focuses on role-based authentication (Admin / Teacher / Student).
- User account creation (Sign-up) is intentionally excluded from the UI.
- Users are pre-created in the database by the administrator.

This design choice was made to:
- Simplify the system for educational purposes
- Focus on authentication, roles, and permissions
- Simulate a controlled academic environment

## Test Credentials
 To test the application:
1. Insert a user manually into the database (student / teacher / admin)
2. Use the inserted email and password to log in

Example:
1. Email: student@test.com
2. Password: test123
-----------------
1. username: teacher
2. password: test123
-----------------
1.username: admin
2.password: test123


## Setup
1. Clone repository
2. update your local credentials in the file **connect.p** ( DB host , DB username , DB password , DB name )
3. Import database schema
4. Install dependencies
5. Run the application (python src/main.py)


## Author

Ammar Abadou
