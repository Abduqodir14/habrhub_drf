from django.urls import path, include

from apps.followers.views import ListFollowerView, FollowerView

app_name = 'followers'

urlpatterns = [
    path('', ListFollowerView.as_view() , name='followers-list'),
    path('<uuid:pk>/', FollowerView.as_view() , name='followers-detail')
]
