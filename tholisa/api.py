from django.urls import path

from tholisa.views import PensisView

app_name = 'tholisa.api'

urlpatterns = [
    path('pensis/', PensisView.as_view()),
    path('pensis/<int:pk>', PensisView.as_view()),
]
