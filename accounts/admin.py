from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import IbuthoCreationForm, IbuthoChangeForm
from .models import Ibutho


class IbuthoAdmin(UserAdmin):
    add_form = IbuthoCreationForm
    form = IbuthoChangeForm
    model = Ibutho
    list_display = ['email', 'username', ]


admin.site.register(Ibutho, IbuthoAdmin)
