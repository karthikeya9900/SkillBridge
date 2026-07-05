# SkillBridge

SkillBridge is a modular Django platform for managing campus placement workflows, including student profiles, employer/company profiles, placement drives, applications, broadcasts, in-app notifications, and admin reporting.

## Current capabilities

- Role-based authentication for admins, students, and companies
- Role-specific dashboards routed from a single `/dashboard/` entry point
- Student profiles with academic details, skills, photo, resume, and email notification preferences
- Company profiles with approval workflow and notification preferences
- Placement drives/jobs with eligibility rules and active/inactive state
- Student applications with duplicate prevention and company-side status updates
- Broadcast announcements for students and companies
- In-app notifications for students, companies, and admins
- Admin dashboard with summary metrics and management pages for students, companies, drives, and applications
- Password reset by email and email notifications for broadcasts and application updates

## Notifications

SkillBridge includes a dedicated `notifications` app with an in-app inbox at `/notifications/`.

Notifications are created automatically when:

| Event | Recipients |
|-------|------------|
| Company posts a new job | Eligible students and platform admins |
| Application status changes | The student who applied |
| Admin creates a student broadcast | Students matching the audience (All / Final Year) |
| Admin creates a company broadcast | All companies |

The sidebar shows an unread count next to **Notifications** for each role. Visiting the notifications page marks items as read. Email delivery still respects each user's `receive_email_notifications` preference for broadcasts and application updates.

## Navigation by role

### Student
- Dashboard, Jobs, Profile, Applications, Notifications

### Company
- Dashboard, Jobs, Company profile, Applicants, Post Job (when approved), Notifications

### Admin
- Dashboard (admin overview), Jobs, Students, Companies, Drives, Applications, Broadcasts, Notifications, Django Admin

## Project structure

```
accounts/        # Custom user model, auth, dashboard routing
students/        # Student profiles, applications, dashboard
companies/       # Company profiles and dashboard
jobs/            # Placement drives and applications
broadcasts/      # Admin announcements
notifications/   # In-app notification inbox and delivery logic
reports/         # Admin metrics and management views
templates/       # Shared HTML templates
static/          # CSS and static assets
```

## Local setup

1. Create and activate a virtual environment.

- PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
- Command Prompt:
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Apply database migrations:
```powershell
python manage.py migrate
```

4. Create an admin user:
```powershell
python manage.py createsuperuser
```

5. Run the development server:
```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Testing

Run the full test suite with:

```powershell
python manage.py test
```

The suite includes coverage for application workflows, broadcast delivery, and notification triggers for new jobs, status changes, and broadcasts.

## Notes

- The project uses SQLite by default for local development.
- Settings support environment-based configuration, so PostgreSQL and production hardening can be introduced later without changing the application structure.
- In development, emails are written to `tmp/emails/` by default when using the file-based email backend.
