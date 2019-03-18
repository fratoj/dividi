from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import AuthorCreationForm


class SignUp(generic.CreateView):
    form_class = AuthorCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
