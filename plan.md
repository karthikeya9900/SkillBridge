# SkillBridge

## AI-Powered Student Placement & Skill Gap Platform

**Version:** 1.0

**Document Type:** Software Requirements Specification (SRS)

**Project Type:** Full Stack Web Application

**Backend:** Python + Django

**Frontend:** HTML + CSS + Bootstrap + JavaScript

**Database:** PostgreSQL

---

# Table of Contents

1. Project Overview
2. Vision
3. Objectives
4. Scope
5. Technology Stack
6. Development Principles
7. User Roles
8. Functional Requirements
9. Non Functional Requirements
10. Project Architecture
11. Database Design
12. Django Apps
13. User Interface
14. Development Roadmap
15. Future Enhancements

---

# 1. Project Overview

SkillBridge is a centralized placement management and student career development platform.

Unlike traditional placement portals that only allow students to apply for jobs, SkillBridge helps students organize their academic profile, manage documents, showcase technical skills, apply for opportunities, and receive placement-related announcements.

The initial version focuses on providing a clean and scalable placement management system. Artificial Intelligence features will be introduced only after the core platform is complete.

---

# 2. Vision

Create a platform that becomes the single source of truth for every student's placement journey.

The system should:

- Maintain student academic records
- Manage placement drives
- Allow companies to post jobs
- Allow students to apply
- Broadcast placement notifications
- Store resumes and academic documents
- Generate placement reports

The platform should be designed so that AI features such as Skill Gap Analysis, Resume Analyzer, Placement Prediction, and Career Recommendations can be integrated without major architectural changes.

---

# 3. Objectives

The project has the following objectives.

## Student Objectives

- Register an account
- Complete profile
- Upload documents
- Maintain skills
- Apply for jobs
- Track applications
- Receive notifications

## Company Objectives

- Register company
- Maintain company profile
- Create placement drives
- Manage applicants
- Update application status

## Admin Objectives

- Manage students
- Manage companies
- Approve company registrations
- Publish placement announcements
- Generate placement reports

---

# 4. Scope

The first version will include only the essential placement workflow.

Included:

- Authentication
- Student Management
- Company Management
- Placement Drives
- Job Applications
- Broadcast Notifications
- Reports

Excluded:

- AI Features
- Resume Parsing
- OCR
- Recommendation Engine
- Chatbot
- Machine Learning
- Mobile App

---

# 5. Technology Stack

## Backend

Python 3.13+

Django

Django REST Framework

---

## Frontend

HTML5

CSS3

Bootstrap 5

JavaScript

---

## Database

PostgreSQL

---

## Authentication

Django Authentication

Role Based Authorization

---

## Storage

Local Media Folder

Future:

AWS S3

---

# 6. Development Principles

The AI agent must strictly follow these principles.

## Principle 1

Keep the architecture modular.

Every feature must belong to its own Django app.

---

## Principle 2

Avoid duplicate code.

---

## Principle 3

Views should be lightweight.

Business logic belongs in:

- Services
- Models
- Utility functions

---

## Principle 4

Follow Django best practices.

---

## Principle 5

Every feature must be functional before adding enhancements.

---

## Principle 6

Follow PEP8 coding standards.

---

## Principle 7

The application must be responsive.

---

## Principle 8

All forms must have server-side validation.

---

## Principle 9

Use PostgreSQL relationships instead of duplicated columns.

---

## Principle 10

Write reusable templates.

---

# 7. User Roles

The platform has three user roles.

## Administrator

Responsibilities:

- Manage all users
- Approve companies
- Broadcast notifications
- View reports
- Manage placement drives

---

## Student

Responsibilities:

- Create profile
- Upload resume
- Upload documents
- Maintain skills
- Apply for jobs
- Receive notifications

---

## Company

Responsibilities:

- Maintain company profile
- Create jobs
- View applicants
- Shortlist students
- Update application status

---

# 8. Functional Requirements

## Authentication

The system shall provide:

- Login
- Logout
- Password reset
- Password change
- Session management
- Role-based dashboard

---

## Student Profile

Students shall be able to:

- Edit profile
- Upload photograph
- Upload resume
- Enter CGPA
- Enter department
- Enter branch
- Enter year
- Enter phone number
- Enter email

---

## Company

Companies shall be able to:

- Create profile
- Edit profile
- Create placement drives
- Edit placement drives
- Delete placement drives

---

## Jobs

Students shall be able to:

- View jobs
- Search jobs
- Filter jobs
- Apply
- View application status

---

## Broadcasts

Admin shall be able to:

- Create broadcast
- Edit broadcast
- Delete broadcast
- Send notifications

---

## Reports

Admin shall view:

- Number of students
- Number of companies
- Number of jobs
- Number of applications
- Placement statistics

---

# 9. Non Functional Requirements

Performance

- Page load under 2 seconds

Security

- CSRF protection
- Password hashing
- Session security

Scalability

The system must support future AI modules.

Maintainability

Each Django app should remain independent.

Availability

The application should function on desktop and mobile browsers.

---

# 10. Project Architecture

Browser

↓

Frontend

↓

Django Views

↓

Business Logic

↓

Models

↓

PostgreSQL

```

Frontend

↓

Django Templates

↓

Views

↓

Services

↓

Models

↓

Database

```

No microservices.

No Docker.

No Celery.

Keep the architecture simple.

---

# Development Philosophy

The AI agent must build the project in iterations.

Iteration 1

Working authentication

Iteration 2

Student module

Iteration 3

Company module

Iteration 4

Jobs

Iteration 5

Applications

Iteration 6

Broadcasts

Iteration 7

Reports

Only after all iterations are complete should additional features be added.
