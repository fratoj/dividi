from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from accounts.models import Author
from specials import tomd
from specials.forms import FibForm, ThoughtForm
from .models import Thought, Fib


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class FibCreateView(LoginRequiredMixin, CreateView):
    form_class = FibForm
    model = Fib

    def get_success_url(self):
        return reverse('specials:fib_list')

    def form_valid(self, form):
        fib = form.save(commit=False)
        fib.content = tomd.convert(fib.content)
        loggedin_user = Author.objects.get(id=self.request.user.id)
        fib.user = loggedin_user
        fib.save()
        return HttpResponseRedirect(self.get_success_url())


class FibIndexView(ListView):
    model = Fib
    fields = ('title', 'content', 'user', )
    ordering = ['-create_date']


class FibDetailView(DetailView):
    model = Fib


class ThoughtCreateView(LoginRequiredMixin, CreateView):
    form_class = ThoughtForm
    model = Thought

    def get_success_url(self):
        return reverse('specials:thought_list')

    def form_valid(self, form):
        fib = form.save(commit=False)
        fib.content = tomd.convert(fib.content)
        loggedin_user = Author.objects.get(id=self.request.user.id)
        fib.user = loggedin_user
        fib.save()
        return HttpResponseRedirect(self.get_success_url())


class ThoughtIndexView(ListView):
    model = Thought
    fields = ('title', 'content', 'user', )
    ordering = ['-create_date']


class ThoughtDetailView(DetailView):
    model = Thought
