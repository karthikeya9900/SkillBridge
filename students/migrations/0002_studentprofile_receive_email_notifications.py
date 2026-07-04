from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentprofile",
            name="receive_email_notifications",
            field=models.BooleanField(default=True),
        ),
    ]
