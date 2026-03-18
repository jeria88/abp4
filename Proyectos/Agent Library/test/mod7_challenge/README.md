# 🧪 Laboratorio del Profesor Oak - Sistema de Citas

Este es un sistema web temático desarrollado como parte de un desafío técnico para un puesto de Desarrollador Fullstack Junior. Permite a los nuevos entrenadores registrarse, elegir su criatura inicial y agendar una cita en el laboratorio.

## 🚀 Características

- **Registro e Inicio de Sesión**: Sistema de autenticación para entrenadores.
- **Flujo de reserva en 3 pasos**:
    1. **Elección de Criatura**: Charmander, Bulbasaur o Squirtle con animaciones interactivas.
    2. **Elección de Horario**: Calendario semanal con control de cupos en tiempo real.
    3. **Confirmación**: Resumen detallado antes de finalizar la reserva.
- **Mi Reserva**: Vista optimizada para consultar los detalles de la cita agendada.
- **Admin de Django**: Gestión completa de criaturas, horarios y reservas para el Profesor Oak.
- **Diseño Premium**: Interfaz temática, responsiva y con micro-animaciones (Glassmorphism, transiciones suaves).

## 🛠️ Tecnologías

- **Backend**: Django 6.0 (Python 3)
- **Base de Datos**: SQLite3
- **Frontend**: HTML5, Vanilla CSS3 (sin frameworks externos)
- **Tipografía**: Google Fonts (Outfit)

## 📦 Instalación y Ejecución

1. **Clonar el repositorio** (o acceder a la carpeta del proyecto).
2. **Activar el entorno virtual**:
   ```bash
   source venv/bin/activate
   ```
3. **Instalar dependencias** (si no están instaladas):
   ```bash
   pip install django
   ```
4. **Ejecutar migraciones y poblar datos**:
   ```bash
   python manage.py migrate
   python populate_data.py
   ```
5. **Crear un superusuario** (para el Profesor Oak):
   ```bash
   python manage.py createsuperuser
   ```
6. **Iniciar el servidor**:
   ```bash
   python manage.py runserver
   ```
7. **Acceder a la aplicación**:
   - Frontend: `http://127.0.0.1:8000/oak-lab/login/`
   - Admin: `http://127.0.0.1:8000/admin/`

## 🧪 Decisiones Técnicas

- **Modelos**: Uso de `OneToOneField` en `Reservation` para garantizar que un entrenador solo tenga una reserva.
- **Validaciones**: Implementación de lógica en el modelo (`clean`) y en las vistas para respetar los cupos máximos de los horarios.
- **Optimización**: Uso de `select_related` en la consulta de reservas para evitar el problema de consultas N+1.
- **UI/UX**: Uso de variables CSS para una paleta de colores consistente y animaciones basadas en estados (hover, active) para mejorar la interactividad.

---
Desarrollado con ❤️ para el Desafío Fullstack.
