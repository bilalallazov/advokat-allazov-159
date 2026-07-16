from .content import DEFAULT_FAQ
from .models import FAQItem


def get_client_ip(request) -> str | None:
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def get_faq_items():
    """FAQ из БД или дефолтный контент, если записей ещё нет."""
    qs = FAQItem.objects.filter(is_published=True)
    if qs.exists():
        return qs
    return [
        type('FAQ', (), {'question': q, 'answer': a})()
        for q, a in DEFAULT_FAQ
    ]


def seed_default_faq() -> int:
    """Создаёт дефолтные FAQ, если таблица пуста. Возвращает число созданных."""
    if FAQItem.objects.exists():
        return 0
    objects = [
        FAQItem(question=q, answer=a, order=index)
        for index, (q, a) in enumerate(DEFAULT_FAQ)
    ]
    FAQItem.objects.bulk_create(objects)
    return len(objects)
