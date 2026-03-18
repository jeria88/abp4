import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poke_appointment.settings')
django.setup()

from oak_lab.models import Creature, Schedule

def populate():
    # 1. Create Creatures
    creatures_data = [
        {
            'name': 'Charmander',
            'type': 'fuego',
            'description': 'Prefiere las cosas calientes. Dicen que cuando llueve le sale vapor de la punta de la cola.',
            'image_emoji': '🔥'
        },
        {
            'name': 'Bulbasaur',
            'type': 'planta',
            'description': 'Lleva una semilla en el lomo desde que nace. Esta crece con él.',
            'image_emoji': '🌿'
        },
        {
            'name': 'Squirtle',
            'type': 'agua',
            'description': 'Tras nacer, el lomo se le endurece y se convierte en una concha. Lanza potente espuma por la boca.',
            'image_emoji': '💧'
        }
    ]

    for data in creatures_data:
        Creature.objects.get_or_create(name=data['name'], defaults=data)
    
    print("Creatures populated.")

    # 2. Create Schedules
    days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    times = [
        ('10:00', '11:00'),
        ('14:00', '15:00'),
    ]

    for day in days:
        for start, end in times:
            Schedule.objects.get_or_create(
                day=day,
                start_time=start,
                end_time=end,
                defaults={'max_capacity': 5}
            )

    print("Schedules populated.")

if __name__ == '__main__':
    populate()
