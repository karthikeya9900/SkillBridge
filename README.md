# SkillBridge

Simple modular Django MVP for student placement management.

## Current scope

- Role-based authentication for admins, students, and companies
- Student profiles with skills and resume upload
- Company profiles with admin approval flag
- Placement drives/jobs
- Student applications and company/admin status updates
- Broadcast announcements
- Admin report dashboard

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Notes

The project uses SQLite by default to keep the first version simple. The settings file reads environment variables for production-oriented values, so PostgreSQL can be introduced later without changing app code.
