from django.contrib import admin
from .models import Creature, Schedule, Reservation

@admin.register(Creature)
class CreatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'max_capacity', 'get_remaining_slots')
    list_filter = ('day',)

    def get_remaining_slots(self, obj):
        return obj.remaining_slots
    get_remaining_slots.short_description = 'Cupos Restantes'

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'creature', 'schedule', 'created_at')
    list_filter = ('creature', 'schedule__day')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'creature', 'schedule')
