from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_auth_code(domain, email, auth_code):
    login_link = f"{domain}/api/login-code/login?auth_code={auth_code}&email={email}"
    send_mail(
            "Auth Code",
            f"Your auth code is {auth_code} and your link is {login_link}",
            'example@test.com',
            [email],
        )