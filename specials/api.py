from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from specials.views import ThoughtView, FibView, SingleFibView

app_name = 'specials.api'

urlpatterns = [
    path('thought/', ThoughtView.as_view()),
    path('thought/<int:pk>', ThoughtView.as_view()),
    path('fib/', FibView.as_view()),
    path('fib/<int:pk>', SingleFibView.as_view()),
    path('token-auth/', obtain_auth_token, name='token_auth'),
]
