from django.contrib import admin
from django import forms

from ckeditor.widgets import CKEditorWidget

from apps.posts.models import Post, Vote


class PostAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ("id", "title", 'description', "author", "views", "rating")
    list_display_links = ("id", "title")


admin.site.register(Vote)

