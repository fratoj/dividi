from django.urls import path

from . import views

app_name = 'tholisa'

urlpatterns = [
    path('', views.pensis_list, name='list'),
    path('<int:pk>', views.pensis_detail, name='detail'),
]
