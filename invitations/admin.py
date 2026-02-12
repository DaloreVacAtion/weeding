"""
Настройка Django Admin для просмотра ответов гостей.
"""

from django.contrib import admin

from .models import GuestResponse


@admin.register(GuestResponse)
class GuestResponseAdmin(admin.ModelAdmin):
    change_list_template = 'admin/invitations/guestresponse/change_list.html'
    list_display = [
        'fio', 'fio_plus_one', 'will_attend_display',
        'overnight_stay', 'transfer_to_venue', 'transfer_home',
        'created_at'
    ]
    list_filter = ['will_attend', 'overnight_stay', 'transfer_to_venue', 'transfer_home']
    search_fields = ['fio', 'fio_plus_one', 'transfer_address']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('fio', 'fio_plus_one', 'will_attend')
        }),
        ('Напитки', {
            'fields': ('alcohol_preferences', 'custom_alcohol', 'non_alcohol_preferences', 'custom_non_alcohol')
        }),
        ('Логистика', {
            'fields': ('overnight_stay', 'transfer_to_venue', 'transfer_home', 'transfer_address')
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )

    @admin.display(boolean=True, description='Придёт')
    def will_attend_display(self, obj):
        return obj.will_attend

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        cl = self.get_changelist_instance(request)
        total_guests = 0
        for r in cl.queryset:
            if r.fio:
                total_guests += 1
            if r.fio_plus_one:
                total_guests += 1
        extra_context['total_guests_count'] = total_guests
        return super().changelist_view(request, extra_context)
