from django.urls import path

from . import views

app_name = 'specials'

urlpatterns = [
    path('', views.thought_list, name='list'),
    path('<int:pk>', views.thought_detail, name='detail'),
    path('fibs/', views.FibIndexView.as_view(), name='fib_list'),
]
