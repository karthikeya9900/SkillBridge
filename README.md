# SkillBridge

SkillBridge is a modular Django platform for managing campus placement workflows, including student profiles, employer/company profiles, placement drives, applications, broadcasts, and admin reporting.

## Current capabilities

- Role-based authentication for admins, students, and companies
- Student profiles with academic details, skills, photo, resume, and email notification preferences
- Company profiles with approval workflow and notification preferences
- Placement drives/jobs with eligibility rules and active/inactive state
- Student applications with duplicate prevention and company-side status updates
- Broadcast announcements for students and companies
- Admin dashboards for monitoring students, companies, drives, applications, and offers
- Password reset by email and basic email notifications for broadcasts and application updates

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

Run the test suite with:

```powershell
python manage.py test
```

## Notes

The project uses SQLite by default for local development. The settings file already supports environment-based configuration, so PostgreSQL and production hardening can be introduced later without changing the application structure.
