from django import forms

from .models import ConsultationRequest


class ConsultationForm(forms.ModelForm):
    """Форма заявки на консультацию — стилизуем через widget attrs."""

    class Meta:
        model = ConsultationRequest
        fields = ('name', 'phone', 'email', 'message')
        labels = {
            'name': 'Ваше имя',
            'phone': 'Телефон',
            'email': 'Email (необязательно)',
            'message': 'Кратко опишите ситуацию',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-field',
                    'placeholder': 'Иван Иванов',
                    'autocomplete': 'name',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-field',
                    'placeholder': '+7 (900) 000-00-00',
                    'autocomplete': 'tel',
                    'inputmode': 'tel',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-field',
                    'placeholder': 'mail@example.com',
                    'autocomplete': 'email',
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-field form-textarea',
                    'placeholder': 'Вызов на допрос, повестка, стадия дела…',
                    'rows': 4,
                }
            ),
        }

    def clean_phone(self) -> str:
        phone = self.cleaned_data['phone'].strip()
        digits = ''.join(ch for ch in phone if ch.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError('Укажите корректный номер телефона.')
        return phone

    def clean_name(self) -> str:
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise forms.ValidationError('Укажите имя.')
        return name
