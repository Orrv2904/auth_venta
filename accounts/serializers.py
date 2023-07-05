from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Publicacion, Imagen, UserAccount, Categoria
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'image_perfil')


class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = "__all__"

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = "__all__"

class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ['id', 'imagen']
class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id','first_name', 'last_name']  # Asegúrate de incluir los campos relevantes del modelo Autor

class PublicacionImagenSerializer(serializers.Serializer):
    publicacion = serializers.PrimaryKeyRelatedField(queryset=Publicacion.objects.all())
    titulo = serializers.CharField(source='publicacion.titulo', read_only=True)
    autor = AutorSerializer(source='publicacion.autor', read_only=True)
    imagenes = ImagenSerializer(many=True)

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'image_perfil']