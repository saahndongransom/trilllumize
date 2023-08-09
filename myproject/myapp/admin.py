from django.contrib import admin
from .models import BlogPost
from .models import Category, Tag
from .models import Comment
from .models import Resource

from .models import SubscribedUsers
from django.forms.widgets import TextInput

admin.site.register(SubscribedUsers)
# myapp/admin.py
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'price')
    list_filter = ('resource_type',)
    search_fields = ('title', 'description')


class CKEditorWidget(TextInput):
    template_name = 'admin/ckeditor_widgets'






admin.site.register(BlogPost)
admin.site.register(Comment)


# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)