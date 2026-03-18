from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Bienvenido al laboratorio, {user.username}!")
            return redirect('select_creature')
    else:
        form = UserCreationForm()
    return render(request, 'oak_lab/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Has iniciado sesión como {username}.")
                return redirect('select_creature')
            else:
                messages.error(request, "Usuario o contraseña inválidos.")
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    else:
        form = AuthenticationForm()
    return render(request, 'oak_lab/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')

from .models import Creature, Schedule, Reservation

@login_required
def select_creature(request):
    # Check if user already has a reservation
    if Reservation.objects.filter(user=request.user).exists():
        messages.warning(request, "Ya tienes una reserva activa.")
        return redirect('my_reservation')
        
    creatures = Creature.objects.all()
    return render(request, 'oak_lab/select_creature.html', {'creatures': creatures})

@login_required
def select_schedule(request):
    creature_id = request.GET.get('creature_id')
    if not creature_id:
        return redirect('select_creature')
    
    creature = Creature.objects.get(id=creature_id)
    
    # Filter schedules that have at least one slot left
    # In a real app we might want to do this more efficiently in the DB
    all_schedules = Schedule.objects.all()
    available_schedules = [s for s in all_schedules if s.remaining_slots > 0]
    
    return render(request, 'oak_lab/select_schedule.html', {
        'creature': creature,
        'schedules': available_schedules
    })

@login_required
def confirm_reservation(request):
    creature_id = request.GET.get('creature_id')
    schedule_id = request.GET.get('schedule_id')
    
    if not creature_id or not schedule_id:
        return redirect('select_creature')
    
    creature = Creature.objects.get(id=creature_id)
    schedule = Schedule.objects.get(id=schedule_id)
    
    if request.method == 'POST':
        # Final validation before saving
        if Reservation.objects.filter(user=request.user).exists():
            messages.error(request, "Error: Ya tienes una reserva.")
            return redirect('my_reservation')
            
        if schedule.remaining_slots <= 0:
            messages.error(request, "Error: Este horario se acaba de llenar.")
            return redirect('select_schedule')
            
        # Create reservation
        Reservation.objects.create(
            user=request.user,
            creature=creature,
            schedule=schedule
        )
        messages.success(request, "¡Reserva confirmada con éxito!")
        return render(request, 'oak_lab/success.html', {
            'creature': creature,
            'schedule': schedule
        })
        
    return render(request, 'oak_lab/confirm_reservation.html', {
        'creature': creature,
        'schedule': schedule
    })

@login_required
def my_reservation(request):
    try:
        # Use select_related to optimize N+1 problem
        reservation = Reservation.objects.select_related('creature', 'schedule').get(user=request.user)
    except Reservation.DoesNotExist:
        reservation = None
        
    return render(request, 'oak_lab/my_reservation.html', {'reservation': reservation})
