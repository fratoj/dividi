from django.forms import widgets


class TextareaMediumEditorWidget(widgets.Textarea):
    class Media:
        js = (
            'editor/js/medium-editor.min.js',
            # 'editor/js/me-markdown.standalone.min.js',
            'forms/widgets/medium_editor_textarea.js',
        )
        css = {
            'all': (
                'editor/css/medium-editor.css',
                'editor/css/themes/default.css',
            )
        }
    template_name = 'forms/widgets/textarea.html'


class TitleInputMediumEditorWidget(widgets.TextInput):
    class Media:
        js = (
            'editor/js/medium-editor.min.js',
            'forms/widgets/medium_editor_text.js',
        )
        css = {
            'all': (
                'editor/css/medium-editor.css',
                'editor/css/themes/default.css',
            )
        }
    template_name = 'forms/widgets/text.html'
