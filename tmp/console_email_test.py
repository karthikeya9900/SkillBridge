import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillbridge.settings')
django.setup()

from django.core.mail import send_mail

result = send_mail(
    'Test',
    'Body',
    'SkillBridge <ksaisaran643@gmail.com>',
    ['ksaisaran643@gmail.com'],
    fail_silently=False,
)
print('send_mail result:', result)
