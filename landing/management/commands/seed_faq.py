from django.core.management.base import BaseCommand

from landing.content import DEFAULT_FAQ
from landing.models import FAQItem
from landing.services import seed_default_faq


class Command(BaseCommand):
    help = 'Заполняет или обновляет FAQ из content.DEFAULT_FAQ'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Удалить существующие FAQ и создать заново',
        )

    def handle(self, *args, **options):
        if options['force']:
            deleted, _ = FAQItem.objects.all().delete()
            self.stdout.write(f'Удалено FAQ: {deleted}')
            created = seed_default_faq()
            self.stdout.write(self.style.SUCCESS(f'Создано FAQ: {created}'))
            return

        created = seed_default_faq()
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создано FAQ: {created}'))
        else:
            # Обновляем тексты по порядку, если количество совпадает
            items = list(FAQItem.objects.order_by('order', 'id'))
            if len(items) == len(DEFAULT_FAQ):
                for obj, (question, answer) in zip(items, DEFAULT_FAQ):
                    obj.question = question
                    obj.answer = answer
                    obj.is_published = True
                FAQItem.objects.bulk_update(items, ['question', 'answer', 'is_published'])
                self.stdout.write(self.style.SUCCESS(f'Обновлено FAQ: {len(items)}'))
            else:
                self.stdout.write(
                    'FAQ уже есть в другом составе. Запустите с --force для полной перезаписи.'
                )
