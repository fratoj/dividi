from django.urls import path

from . import views

app_name = 'specials'

urlpatterns = [
    # path('', views.thought_list, name='list'),
    # path('<int:pk>', views.thought_detail, name='detail'),
    path('fibs/', views.FibIndexView.as_view(), name='fib_list'),
    path('fibs/new', views.FibCreateView.as_view(), name='fib_create'),
    path('fibs/<int:pk>', views.FibDetailView.as_view(), name='fib_detail'),
    path('thoughts/', views.ThoughtIndexView.as_view(), name='thought_list'),
    path('thoughts/new', views.ThoughtCreateView.as_view(), name='thought_create'),
    path('thoughts/<int:pk>', views.ThoughtDetailView.as_view(), name='thought_detail'),
]
