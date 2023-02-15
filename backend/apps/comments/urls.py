from django.urls import path

from apps.comments.views import CreateCommentstView

app_name = 'comments'

urlpatterns = [
    path('', CreateCommentstView.as_view(), name='create')
]
