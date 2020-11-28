from .models import CustomUser, Posto, Precos, Denuncia
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, PostoSerializer, PrecoSerializer, GCMDeviceSerializer, DenunciaSerializer, ChangePasswordSerializer
from push_notifications.models import GCMDevice

class PostoList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Posto.objects.all()
    serializer_class = PostoSerializer

class DenunciaCreate(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Denuncia.objects.all()
    serializer_class = DenunciaSerializer    

class PostoRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostoSerializer 

    def get_queryset(self):
        id = self.kwargs['pk']
        return Posto.objects.get(id=id)  

    def retrieve(self, request, pk):
        queryset = self.get_queryset()
        serializer = PostoSerializer(queryset,)  
        return Response(serializer.data)    
    

class UserRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def retrieve(self, request, pk=None):
        if request.user and pk == 'me':
            return Response(UserSerializer(request.user).data)
        return super(UserRetrieve, self).retrieve(request, pk)

class UserCreate(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer   

class PrecoCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PrecoSerializer       
    
    def create(self, request):
        preco = PrecoSerializer(data=request.data)
        if preco.is_valid():
            posto = Posto.objects.get(user=request.user)
            precos, created = Precos.objects.update_or_create(posto=posto, defaults={
                'gasolina': preco.validated_data.get("gasolina", None),
                'aditivada': preco.validated_data.get("aditivada", None),
                'alcool': preco.validated_data.get("alcool", None),
                'diesel': preco.validated_data.get("diesel", None),
                'gnv': preco.validated_data.get("gnv", None),
                'etanol': preco.validated_data.get("etanol", None)     
            }) 
            return Response(PrecoSerializer(precos).data)

class DeviceCreate(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = GCMDevice.objects.all()
    serializer_class = GCMDeviceSerializer            
  
class PrecoRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PrecoSerializer  

    def retrieve(self, request, pk=None):
        if request.user and pk == 'me':  
            try:            
                preco = Precos.objects.get(posto__id=request.user.posto.id)              
                return Response(PrecoSerializer(preco).data) 
            except Precos.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)                         
        return super(PrecoSerializer, self).retrieve(request, pk)

class PostoUpdate(generics.UpdateAPIView):    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostoSerializer

    def update(self, request, *args, **kwargs):
        posto = Posto.objects.get(id=request.user.posto.id)
        serializer = PostoSerializer(posto, data={'nome': request.data}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class UserChangePassword(generics.UpdateAPIView):
    pagination_class = [permissions.IsAuthenticated]    
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):         
        user = CustomUser.objects.get(id=request.user.id)
        if not user.check_password(request.data["senha_atual"]):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data["senha_nova"])
        user.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Senha alterada com sucesso',
            'data': []  
        }
        return Response(response)

class UserDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        if not user.check_password(request.data):
            return Response(status=status.HTTP_400_BAD_REQUEST)        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)            



            
             
            