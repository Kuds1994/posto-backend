from .models import CustomUser, Posto, Precos, Denuncia
from rest_framework import serializers
from push_notifications.models import GCMDevice

class PrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precos
        fields = ['id', 'aditivada', 'alcool', 'diesel', 'gasolina', 'gnv', 'etanol']   

class DenunciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Denuncia
        fields = '__all__'

class PostoSerializer(serializers.ModelSerializer):
    preco = PrecoSerializer(many=False, read_only=True)

    class Meta:
        model = Posto
        fields = ['id','cnpj','nome', 'ltd', 'lgt', 'preco']                 

class UserSerializer(serializers.ModelSerializer):
    posto = PostoSerializer(many=False)    

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ['id', 'first_name', 'password', 'email', 'posto']  

    def create(self, validated_data):
        posto_data = validated_data.pop('posto')
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Posto.objects.create(user=user, **posto_data)
        return user  

class GCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GCMDevice
        fields = '__all__'        
  
class ChangePasswordSerializer(serializers.Serializer):

    senha_atual = serializers.CharField(required=True)
    senha_nova = serializers.CharField(required=True)
