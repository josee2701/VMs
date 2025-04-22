# your_app/views.py
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, VirtualMachine
from .permissions import IsAdminOrReadOnly
from .serializers import (MyTokenObtainPairSerializer, UserSerializer,
                          VirtualMachineSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Sólo admins pueden modificar; otros solo lectura
    
    
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class VirtualMachineViewSet(viewsets.ModelViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer
