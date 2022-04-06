from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_message(user):
    context = {
        'text_detail': 'Спасибо за регистрацию',
        'email': user.email,
        'domain': 'http://127.0.0.1:8000/',
        'activation_code': user.activation_code,
    }
    msg_html = render_to_string('email.html', context)
    plain_message = strip_tags(msg_html)
    subject = 'Активация аккаунта'
    to_email = user.email
    mail.send_mail(subject, plain_message, 'nodirasdrv@gmail.com', [to_email, ],
                   html_message=msg_html)
