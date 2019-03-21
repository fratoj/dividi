from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from specials.models import Fib, Thought
from specials.widgets import TitleInputMediumEditorWidget, TextareaMediumEditorWidget


class FibForm(forms.ModelForm):
    title = forms.CharField(widget=TitleInputMediumEditorWidget(
        attrs={'class': 'ui top editable thought__title header'}
    ))
    content = forms.Field(widget=TextareaMediumEditorWidget(
        attrs={'class': 'ui top editable thought__content header'}
    ))

    class Meta:
        model = Fib
        exclude = ('slug', 'user',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'title', 'content',
        )

        super(FibForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = False
        self.fields['content'].label = False
        self.fields['title'].required = True
        self.fields['content'].required = True

    def clean(self):
        self.cleaned_data['content'] = self.cleaned_data['content'].strip()
        return super(FibForm, self).clean()


class ThoughtForm(forms.ModelForm):
    title = forms.CharField(widget=TitleInputMediumEditorWidget(
        attrs={'class': 'ui top editable thought__title header'}
    ))
    content = forms.Field(widget=TextareaMediumEditorWidget(
        attrs={'class': 'ui top editable thought__content header'}
    ))

    class Meta:
        model = Thought
        exclude = ('slug', 'user',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'title', 'content',
        )

        super(ThoughtForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = False
        self.fields['content'].label = False
        self.fields['title'].required = True
        self.fields['content'].required = True

    def clean(self):
        self.cleaned_data['content'] = self.cleaned_data['content'].strip()
        return super(ThoughtForm, self).clean()

