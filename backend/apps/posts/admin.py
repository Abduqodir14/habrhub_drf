from django.contrib import admin
from django import forms

from ckeditor.widgets import CKEditorWidget
from django.template.defaultfilters import truncatechars

from apps.posts.models import Post, Vote


class PostAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    form = PostAdminForm
    list_display = ('id', 'title', 'get_description', 'author', 'views', 'rating')
    list_display_links = ('id', 'title')
    readonly_fields = ('views', 'rating')

    def get_description(self, obj):
        return obj.description[:100]

    get_description.short_description = "description"


admin.site.register(Vote)

