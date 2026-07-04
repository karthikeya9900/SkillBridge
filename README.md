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

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Testing

Run the test suite with:

```powershell
python manage.py test
```

## Notes

The project uses SQLite by default for local development. The settings file already supports environment-based configuration, so PostgreSQL and production hardening can be introduced later without changing the application structure.
