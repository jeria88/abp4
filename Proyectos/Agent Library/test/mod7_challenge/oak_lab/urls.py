from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('select-creature/', views.select_creature, name='select_creature'),
    path('select-schedule/', views.select_schedule, name='select_schedule'),
    path('confirm/', views.confirm_reservation, name='confirm_reservation'),
    path('my-reservation/', views.my_reservation, name='my_reservation'),
]
