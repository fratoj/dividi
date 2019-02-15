from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from tholisa.views import PensisView, FibView, SingleFibView

app_name = 'tholisa.api'

urlpatterns = [
    path('pensis/', PensisView.as_view()),
    path('pensis/<int:pk>', PensisView.as_view()),
    path('fib/', FibView.as_view()),
    path('fib/<int:pk>', SingleFibView.as_view()),
    path('token-auth/', obtain_auth_token, name='token_auth'),
]
