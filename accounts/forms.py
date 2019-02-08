from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Ibutho


class IbuthoCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Ibutho
        fields = ('username', 'email')


class IbuthoChangeForm(UserChangeForm):

    class Meta:
        model = Ibutho
        fields = ('username', 'email', 'profile')
