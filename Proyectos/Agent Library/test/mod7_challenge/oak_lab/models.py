from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Creature(models.Model):
    TYPE_CHOICES = [
        ('fuego', 'Fuego'),
        ('planta', 'Planta'),
        ('agua', 'Agua'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='creatures/', null=True, blank=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_capacity = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"{self.day} {self.start_time} - {self.end_time}"

    @property
    def remaining_slots(self):
        return self.max_capacity - self.reservation_set.count()

class Reservation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creature = models.ForeignKey(Creature, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.schedule.remaining_slots <= 0:
            raise ValidationError("Este horario ya no tiene cupos disponibles.")

    def __str__(self):
        return f"Reserva de {self.user.username} - {self.creature.name}"
