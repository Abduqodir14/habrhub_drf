from rest_framework import permissions, mixins, viewsets, generics

from apps.users.serializers import UserSerializer
from core.viewsets import MixedPermission
from apps.users.models import User


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# class UserViewSet(mixins.CreateModelMixin,
#                   mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   MixedPermission,
#                   viewsets.GenericViewSet):
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes_by_action = {
#         'create': (permissions.AllowAny, ),
#         'retrieve': (permissions.IsAuthenticated,),
#         'update': (permissions.IsAuthenticated,)
#     }
#
#     def get_object(self):
#         return self.request.user

