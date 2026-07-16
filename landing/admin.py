from django.contrib import admin

from .models import ConsultationRequest, FAQItem


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at', 'ip_address')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    search_fields = ('question', 'answer')
    ordering = ('order', 'id')


admin.site.site_header = 'Ст. 159 УК РФ — админка'
admin.site.site_title = 'Ст. 159'
admin.site.index_title = 'Управление лендингом'
