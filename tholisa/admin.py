from datetime import datetime

from django.contrib import admin
from .models import Pensis


class PensisAdmin(admin.ModelAdmin):
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
        return super(PensisAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(PensisAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['pub_date'].initial = datetime.now()
        return form


admin.site.register(Pensis, PensisAdmin)

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