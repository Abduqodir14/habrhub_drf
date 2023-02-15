from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import Route, DynamicRoute, SimpleRouter

from apps.users.views import CreateUserView, ManageUserView

app_name = 'users'

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet, basename='users')


# class CustomReadOnlyRouter(SimpleRouter):
#     """
#     A router for read-only APIs, which doesn't use trailing slashes.
#     """
#     routes = [
#         Route(
#             url=r'^{prefix}$',
#             mapping={'get': 'list'},
#             name='{basename}-list',
#             detail=False,
#             initkwargs={'suffix': 'List'}
#         ),
#         Route(
#             url=r'^{prefix}/account$',
#             mapping={'get': 'retrieve', 'patch': 'update'},
#             name='{basename}-detail',
#             detail=True,
#             initkwargs={'suffix': 'Detail'}
#         )
#     ]


# router = CustomReadOnlyRouter()
# router.register('users', UserViewSet)

urlpatterns = [
    path('', CreateUserView.as_view(), name='create'),
    path('account/', ManageUserView.as_view(), name='account')
]
