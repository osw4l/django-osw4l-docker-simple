from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


def send(**kwargs):
    from_email = 'mail@domain.com'
    subject = kwargs.get('subject')
    to_email = kwargs.get('to_email')
    template = kwargs.get('template')
    context = kwargs.get('context')

    template = get_template(template)
    html_template = template.render(context)
    msg = EmailMultiAlternatives(subject, subject, from_email, to=[to_email])
    msg.attach_alternative(html_template, "text/html")
    msg.send()

    return kwargs
