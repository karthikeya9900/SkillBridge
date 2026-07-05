from datetime import date, timedelta

from django.core import mail
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import User
from accounts.services import create_profile_for_user
from broadcasts.models import Broadcast
from companies.models import CompanyProfile
from jobs.models import Application, PlacementDrive
from notifications.models import Notification


class SkillBridgeFlowTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin = user_model.objects.create_user(
            username="admin",
            password="TestPass123!",
            role=User.Role.ADMIN,
            is_staff=True,
        )
        self.student_user = user_model.objects.create_user(
            username="student",
            password="TestPass123!",
            first_name="Student",
            last_name="User",
            role=User.Role.STUDENT,
        )
        create_profile_for_user(self.student_user)
        self.student = self.student_user.student_profile
        self.student.branch = "CSE"
        self.student.year = self.student.Year.FINAL
        self.student.cgpa = "8.25"
        self.student.save()

        self.company_user = user_model.objects.create_user(
            username="company",
            password="TestPass123!",
            role=User.Role.COMPANY,
        )
        create_profile_for_user(self.company_user)
        self.company = self.company_user.company_profile
        self.company.name = "Acme"
        self.company.is_approved = True
        self.company.save()

        self.drive = PlacementDrive.objects.create(
            company=self.company,
            title="Developer Intern",
            description="Build products",
            requirements="Python",
            min_cgpa="7.00",
            eligible_branches="CSE, IT",
            deadline=date.today() + timedelta(days=10),
            created_by=self.company_user,
        )

    def test_student_can_apply_and_company_can_update_status(self):
        self.client.login(username="student", password="TestPass123!")
        response = self.client.post(reverse("jobs:apply", args=[self.drive.pk]), follow=True)

        self.assertContains(response, "Application submitted.")
        application = Application.objects.get(student=self.student, drive=self.drive)
        self.assertEqual(application.status, Application.Status.APPLIED)

        self.client.login(username="company", password="TestPass123!")
        response = self.client.post(
            reverse("jobs:update_application", args=[application.pk]),
            {"status": Application.Status.SHORTLISTED, "note": "Proceed"},
            follow=True,
        )

        self.assertContains(response, "Application status updated.")
        application.refresh_from_db()
        self.assertEqual(application.status, Application.Status.SHORTLISTED)
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.student_user,
                notification_type=Notification.Type.APPLICATION_STATUS,
            ).exists()
        )

    def test_unapproved_company_cannot_create_drive(self):
        self.company.is_approved = False
        self.company.save()
        self.client.login(username="company", password="TestPass123!")

        response = self.client.get(reverse("jobs:create"), follow=True)

        self.assertContains(response, "must be approved")
        self.assertEqual(PlacementDrive.objects.count(), 1)

    def test_admin_can_create_broadcast(self):
        self.client.login(username="admin", password="TestPass123!")

        response = self.client.post(
            reverse("broadcasts:create"),
            {
                "title": "Campus Update",
                "message": "Placement drive tomorrow.",
                "audience": Broadcast.Audience.ALL,
                "publish_at": "2026-07-04T09:30",
                "is_active": "on",
            },
            follow=True,
        )

        self.assertContains(response, "Broadcast saved.")
        self.assertTrue(Broadcast.objects.filter(title="Campus Update").exists())

    def test_authenticated_login_redirects_to_dashboard(self):
        self.client.login(username="student", password="TestPass123!")

        response = self.client.get(reverse("login"), follow=True)

        self.assertRedirects(response, reverse("students:dashboard"))

    def test_logout_get_is_not_a_browser_error(self):
        self.client.login(username="student", password="TestPass123!")

        response = self.client.get(reverse("logout"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Use the logout button")

    def test_student_applications_and_notifications_pages_render(self):
        self.client.login(username="admin", password="TestPass123!")
        self.client.post(
            reverse("broadcasts:create"),
            {
                "title": "Final Year Update",
                "message": "Prepare for the drive.",
                "audience": Broadcast.Audience.FINAL_YEAR,
                "publish_at": "2026-07-04T09:30",
                "is_active": "on",
            },
        )
        Application.objects.create(student=self.student, drive=self.drive)
        self.client.login(username="student", password="TestPass123!")

        applications_response = self.client.get(reverse("students:applications"))
        notifications_response = self.client.get(reverse("notifications:list"))

        self.assertContains(applications_response, "Developer Intern")
        self.assertContains(notifications_response, "Final Year Update")

    def test_company_all_applicants_page_renders(self):
        Application.objects.create(student=self.student, drive=self.drive)
        self.client.login(username="company", password="TestPass123!")

        response = self.client.get(reverse("companies:applicants"))

        self.assertContains(response, "Student User")
        self.assertContains(response, "Developer Intern")

    def test_company_can_close_and_delete_drive(self):
        self.client.login(username="company", password="TestPass123!")

        close_response = self.client.post(reverse("jobs:close", args=[self.drive.pk]), follow=True)
        self.drive.refresh_from_db()
        self.assertContains(close_response, "was closed")
        self.assertFalse(self.drive.is_active)

        delete_response = self.client.post(reverse("jobs:delete", args=[self.drive.pk]), follow=True)
        self.assertContains(delete_response, "was deleted")
        self.assertFalse(PlacementDrive.objects.filter(pk=self.drive.pk).exists())

    def test_admin_management_actions(self):
        self.client.login(username="admin", password="TestPass123!")

        student_response = self.client.post(reverse("reports:toggle_student", args=[self.student.pk]), follow=True)
        company_response = self.client.post(reverse("reports:toggle_company", args=[self.company.pk]), follow=True)
        drive_response = self.client.post(reverse("reports:toggle_drive", args=[self.drive.pk]), follow=True)

        self.student.refresh_from_db()
        self.company.refresh_from_db()
        self.drive.refresh_from_db()
        self.assertContains(student_response, "verification was updated")
        self.assertContains(company_response, "approval was updated")
        self.assertContains(drive_response, "active state was updated")
        self.assertTrue(self.student.is_verified)
        self.assertFalse(self.company.is_approved)
        self.assertFalse(self.drive.is_active)

    def test_admin_can_delete_broadcast(self):
        broadcast = Broadcast.objects.create(
            title="Remove Me",
            message="Old update",
            audience=Broadcast.Audience.ALL,
            created_by=self.admin,
        )
        self.client.login(username="admin", password="TestPass123!")

        response = self.client.post(reverse("broadcasts:delete", args=[broadcast.pk]), follow=True)

        self.assertContains(response, "was deleted")
        self.assertFalse(Broadcast.objects.filter(pk=broadcast.pk).exists())

    def test_job_filters_by_branch_and_cgpa(self):
        self.client.login(username="student", password="TestPass123!")

        response = self.client.get(reverse("jobs:list"), {"branch": "CSE", "min_cgpa": "8.25"})

        self.assertContains(response, "Developer Intern")

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_sends_email(self):
        self.student_user.email = "student@example.com"
        self.student_user.save(update_fields=["email"])

        response = self.client.post(reverse("password_reset"), {"email": self.student_user.email}, follow=True)

        self.assertContains(response, "We’ve emailed you")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.student_user.email, mail.outbox[0].to)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_broadcast_creation_sends_notification_to_enabled_students(self):
        self.student_user.email = "student@example.com"
        self.student_user.save(update_fields=["email"])
        self.student.receive_email_notifications = True
        self.student.save(update_fields=["receive_email_notifications"])

        self.client.login(username="admin", password="TestPass123!")
        response = self.client.post(
            reverse("broadcasts:create"),
            {
                "title": "Drive Alert",
                "message": "A new placement drive is live.",
                "audience": Broadcast.Audience.ALL,
                "publish_at": "2026-07-04T09:30",
                "is_active": "on",
            },
            follow=True,
        )

        self.assertContains(response, "Broadcast saved.")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.student_user.email, mail.outbox[0].to)
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.student_user,
                notification_type=Notification.Type.BROADCAST,
                title="Drive Alert",
            ).exists()
        )

    def test_new_job_notifies_eligible_students_and_admins(self):
        self.client.login(username="company", password="TestPass123!")
        response = self.client.post(
            reverse("jobs:create"),
            {
                "title": "Backend Engineer",
                "description": "Build APIs",
                "requirements": "Python",
                "location": "Remote",
                "package_lpa": "12.00",
                "min_cgpa": "7.00",
                "eligible_branches": "CSE",
                "deadline": (date.today() + timedelta(days=14)).isoformat(),
                "is_active": "on",
            },
            follow=True,
        )

        self.assertContains(response, "Placement drive created.")
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.student_user,
                notification_type=Notification.Type.NEW_JOB,
                title__icontains="Backend Engineer",
            ).exists()
        )
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.admin,
                notification_type=Notification.Type.NEW_JOB_ADMIN,
            ).exists()
        )

    def test_company_broadcast_creates_in_app_notification(self):
        self.client.login(username="admin", password="TestPass123!")
        self.client.post(
            reverse("broadcasts:create"),
            {
                "title": "Company Notice",
                "message": "Please review the updated policy.",
                "audience": Broadcast.Audience.COMPANIES,
                "publish_at": "2026-07-04T09:30",
                "is_active": "on",
            },
        )

        self.assertTrue(
            Notification.objects.filter(
                recipient=self.company_user,
                notification_type=Notification.Type.BROADCAST,
                title="Company Notice",
            ).exists()
        )
