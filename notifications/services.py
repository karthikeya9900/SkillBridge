from django.db.models import Q

from accounts.models import User
from companies.models import CompanyProfile
from students.models import StudentProfile

from .models import Notification


def create_notification(recipient, notification_type, title, message, link=""):
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link,
    )


def bulk_create_notifications(recipients, notification_type, title, message, link=""):
    unique_recipients = {recipient.pk: recipient for recipient in recipients if recipient}
    if not unique_recipients:
        return []
    notifications = [
        Notification(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link,
        )
        for recipient in unique_recipients.values()
    ]
    return Notification.objects.bulk_create(notifications)


def unread_count(user):
    return Notification.objects.filter(recipient=user, is_read=False).count()


def get_notifications_for_user(user, limit=50):
    return Notification.objects.filter(recipient=user).order_by("-created_at")[:limit]


def mark_notifications_read(user):
    Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)


def get_admin_users():
    return User.objects.filter(is_active=True).filter(
        Q(role=User.Role.ADMIN) | Q(is_staff=True)
    )


def notify_new_job(drive):
    from django.urls import reverse

    student_link = drive.get_absolute_url()
    student_title = f"New job: {drive.title}"
    student_message = f"{drive.company.name} posted a new placement drive: {drive.title}."
    students = StudentProfile.objects.select_related("user").filter(user__is_active=True)
    eligible_students = [student.user for student in students if drive.is_student_eligible(student)]
    bulk_create_notifications(
        eligible_students,
        Notification.Type.NEW_JOB,
        student_title,
        student_message,
        student_link,
    )

    admin_link = reverse("reports:drives")
    admin_title = f"New job posting from {drive.company.name}"
    admin_message = f"{drive.company.name} posted a new drive: {drive.title}."
    bulk_create_notifications(
        get_admin_users(),
        Notification.Type.NEW_JOB_ADMIN,
        admin_title,
        admin_message,
        admin_link,
    )


def notify_application_status_change(application, previous_status):
    if not previous_status or previous_status == application.status:
        return

    from django.urls import reverse

    user = application.student.user
    link = reverse("students:application_detail", kwargs={"pk": application.pk})
    title = f"Application update: {application.drive.title}"
    message = (
        f"Your application status for {application.drive.title} "
        f"is now {application.get_status_display()}."
    )
    create_notification(user, Notification.Type.APPLICATION_STATUS, title, message, link)


def notify_broadcast(broadcast):
    from django.urls import reverse

    from broadcasts.models import Broadcast

    link = reverse("broadcasts:detail", kwargs={"pk": broadcast.pk})

    if broadcast.audience in (Broadcast.Audience.ALL, Broadcast.Audience.FINAL_YEAR):
        students = StudentProfile.objects.select_related("user").filter(user__is_active=True)
        if broadcast.audience == Broadcast.Audience.FINAL_YEAR:
            students = students.filter(year=StudentProfile.Year.FINAL)
        bulk_create_notifications(
            [student.user for student in students],
            Notification.Type.BROADCAST,
            broadcast.title,
            broadcast.message,
            link,
        )

    if broadcast.audience == Broadcast.Audience.COMPANIES:
        companies = CompanyProfile.objects.select_related("user").filter(user__is_active=True)
        bulk_create_notifications(
            [company.user for company in companies],
            Notification.Type.BROADCAST,
            broadcast.title,
            broadcast.message,
            link,
        )
