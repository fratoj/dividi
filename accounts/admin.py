from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AuthorChangeForm, AuthorCreationForm
from .models import Author


class AuthorAdmin(UserAdmin):
    add_form = AuthorCreationForm
    form = AuthorChangeForm
    model = Author
    list_display = ['email', 'username', ]


admin.site.register(Author, AuthorAdmin)
