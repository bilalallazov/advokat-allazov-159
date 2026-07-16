from django.db import models
from django.utils import timezone


class ConsultationRequest(models.Model):
    """Заявка на консультацию с лендинга."""

    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'В работе'
        DONE = 'done', 'Закрыта'

    name = models.CharField('Имя', max_length=120)
    phone = models.CharField('Телефон', max_length=32)
    email = models.EmailField('Email', blank=True)
    message = models.TextField('Ситуация', blank=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    created_at = models.DateTimeField('Создана', default=timezone.now, db_index=True)
    ip_address = models.GenericIPAddressField('IP', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка на консультацию'
        verbose_name_plural = 'Заявки на консультацию'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.name} — {self.phone}'


class FAQItem(models.Model):
    """Вопрос–ответ для блока FAQ."""

    question = models.CharField('Вопрос', max_length=255)
    answer = models.TextField('Ответ')
    order = models.PositiveIntegerField('Порядок', default=0, db_index=True)
    is_published = models.BooleanField('Опубликован', default=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order', 'id']

    def __str__(self) -> str:
        return self.question
