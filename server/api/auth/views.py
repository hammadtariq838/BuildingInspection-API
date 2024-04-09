from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import User

class CreateUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  queryset = User.objects.all()
  permission_classes = [AllowAny] # Only allow unauthenticated users to register

  @classmethod
  def get_extra_actions(cls):
    return []

  def get_queryset(self):
    return self.queryset
  
  def post(self, request, *args, **kwargs):
    print(request.data)
    return self.create(request, *args, **kwargs)