from datetime import datetime
from django.utils import formats
from django.contrib import admin
from django.utils.text import slugify

from .models import Thought, Fib


class ThoughtAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'headline', 'content')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('user', 'slug', 'pub_date')
        })
    )

    prepopulated_fields = {
        'slug': ('title',),
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
        return super(ThoughtAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ThoughtAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['pub_date'].initial = datetime.now()
        return form


class FibAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'content',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('user', 'slug')
        })
    )
    prepopulated_fields = {
        'slug': ('title',),
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
        return super(FibAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(FibAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title'].initial = slugify(formats.date_format(datetime.now(), "Y-m-d"))
        return form


admin.site.register(Thought, ThoughtAdmin)
admin.site.register(Fib, FibAdmin)

"""

--==--
You can limit the choices of a related model to the objects involved in that relation using RelatedOnlyFieldListFilter:

class BookAdmin(admin.ModelAdmin):
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
    )
Assuming author is a ForeignKey to a User model, this will limit the list_filter choices to the users who have written
a book instead of listing all users.
--==--

--==--
Disallowing a user from changing another post
def has_change_permission(self, request, obj=None):
    has_class_permission = super(PostAdmin, self).has_change_permission(request, obj)

    if not has_class_permission:
        return False

    if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
        return False
--==--

--==--
Only let the user view their own posts
Another measure to limit the possibilities of the user can be to let the user only view their own posts. To do this we just change the queryset to filter posts where the author is themselves. We still want superusers to see all posts, so only filter it for normal users.

def queryset(self, request):
    if request.user.is_superuser:
        return Post.objects.all()
    return Post.objects.filter(author=request.user)
--==--
"""