from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="companyprofile",
            name="receive_email_notifications",
            field=models.BooleanField(default=True),
        ),
    ]
