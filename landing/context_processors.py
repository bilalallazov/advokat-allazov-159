from django.conf import settings


def site_contacts(request):
    """Контакты и данные адвоката для всех шаблонов."""
    return {
        'site': {
            'phone': settings.SITE_PHONE,
            'phone_raw': settings.SITE_PHONE_RAW,
            'whatsapp': settings.SITE_WHATSAPP,
            'telegram': settings.SITE_TELEGRAM,
            'email': settings.SITE_EMAIL,
            'lawyer_name': settings.SITE_LAWYER_NAME,
            'lawyer_title': settings.SITE_LAWYER_TITLE,
        }
    }
