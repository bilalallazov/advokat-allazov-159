from django.contrib import messages
from django.urls import reverse
from django.views.generic import FormView

from .content import (
    ABOUT_DECEIT,
    ABOUT_LEAD,
    ABOUT_TRUST,
    ADVANTAGES,
    ADVICE_STEPS,
    AGGRAVATING,
    CORPUS_NOTE,
    CORPUS_SIGNS,
    DAMAGE_NOTE,
    DAMAGE_TYPES,
    FRAUD_CASES,
    INFOGRAPHIC,
    MITIGATING,
    PAGE_INTRO,
    PENALTY_CARDS,
    PROCESS_STEPS,
    REVIEWS,
    WHEN_CARDS,
)
from .forms import ConsultationForm
from .services import get_client_ip, get_faq_items


class HomeView(FormView):
    """Главная страница лендинга + приём заявок."""

    template_name = 'landing/home.html'
    form_class = ConsultationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'page_intro': PAGE_INTRO,
                'about_lead': ABOUT_LEAD,
                'about_deceit': ABOUT_DECEIT,
                'about_trust': ABOUT_TRUST,
                'fraud_cases': FRAUD_CASES,
                'corpus_signs': CORPUS_SIGNS,
                'corpus_note': CORPUS_NOTE,
                'penalty_cards': PENALTY_CARDS,
                'damage_types': DAMAGE_TYPES,
                'damage_note': DAMAGE_NOTE,
                'mitigating': MITIGATING,
                'aggravating': AGGRAVATING,
                'advice_steps': ADVICE_STEPS,
                'when_cards': WHEN_CARDS,
                'process_steps': PROCESS_STEPS,
                'infographic': INFOGRAPHIC,
                'advantages': ADVANTAGES,
                'reviews': REVIEWS,
                'faq_items': get_faq_items(),
            }
        )
        return context

    def form_valid(self, form):
        request_obj = form.save(commit=False)
        request_obj.ip_address = get_client_ip(self.request)
        request_obj.save()
        messages.success(
            self.request,
            'Заявка отправлена. Мы свяжемся с вами в ближайшее время.',
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Проверьте поля формы — есть ошибки заполнения.',
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('landing:home') + '#contacts'
