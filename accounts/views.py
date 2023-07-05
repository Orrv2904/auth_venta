from django.shortcuts import render
from rest_framework import generics
from .models import Publicacion, Imagen
from .serializers import PublicacionSerializer, CategoriaSerializer, ImageSerializer, PublicacionImagenSerializer, UserAccountSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import JSONParser
from django.core.files.storage import default_storage
import random
from django.http import JsonResponse
from .models import Imagen, Categoria
from django.http import HttpResponse



from django.core.serializers.json import DjangoJSONEncoder
import json

class ImageFieldFileEncoder(DjangoJSONEncoder):
    def default(self, o):
        from django.db.models.fields.files import ImageFieldFile
        if isinstance(o, ImageFieldFile):
            return str(o.url)
        return super().default(o)

class ObtenerImagenesView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        publicaciones = Publicacion.objects.order_by('?')[:10]
        registros_random = []

        for publicacion in publicaciones:
            imagenes_publicacion = Imagen.objects.filter(publicacion=publicacion)

            if imagenes_publicacion.exists():
                imagenes_urls = [imagen.imagen for imagen in imagenes_publicacion]
                registros_random.append({
                    'id_publicacion': publicacion.id,
                    'publicacion_titulo': publicacion.titulo,
                    'autor_nombre': publicacion.autor.first_name,
                    'autor_apellido': publicacion.autor.last_name,
                    'perfil': publicacion.autor.image_perfil.url,
                    'imagenes_urls': imagenes_urls
                })

        response_data = {'publicaciones': registros_random}
        response_json = json.dumps(response_data, cls=ImageFieldFileEncoder)

        return HttpResponse(response_json, content_type='application/json')

class ImagenListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        imagenes = Imagen.objects.all()
        publicaciones = {}

        for imagen in imagenes:
            publicacion_id = imagen.publicacion.id
            if publicacion_id in publicaciones:
                publicaciones[publicacion_id]['imagenes'].append(imagen)
            else:
                publicaciones[publicacion_id] = {
                    'publicacion': imagen.publicacion,
                    'imagenes': [imagen],
                }
        
        serializer = PublicacionImagenSerializer(publicaciones.values(), many=True)
        return Response(serializer.data)

class CreatePublicacion(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        post_data = request.data.get('titulo')
        print(request.data)
        images = []

        post = Publicacion.objects.create(titulo=post_data, autor=request.user)
        for key, file_list in request.FILES.items():
            if key.startswith('image') and file_list.content_type.startswith('image'):
                imagen = Imagen.objects.create(publicacion=post, imagen=file_list)
                serializer_imagen = ImageSerializer(imagen)
                images.append(serializer_imagen.data)

        serializer_publicacion = PublicacionSerializer(post)
        
        return Response([serializer_publicacion.data ], status=status.HTTP_201_CREATED)



class ImagenesPublicacionAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        usuario = request.user
        publicaciones = Publicacion.objects.filter(autor=usuario)
        data = []
        for publicacion in publicaciones:
            imagenes = publicacion.imagenes.all()
            imagen_urls = [imagen.imagen.url for imagen in imagenes]
            data.append({
                'publicacion_id': publicacion.id,
                'titulo': publicacion.titulo,
                'imagenes': imagen_urls
            })
        return Response(data)

class UploadImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, format=None):
        user = request.user
        image_file = request.data['image_perfil']
        user.image_perfil = image_file
        user.save()
        serializer = UserAccountSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriaListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
# class PublicacionListCreateView(generics.ListCreateAPIView):
#     permission_classes = [AllowAny]
#     queryset = Publicacion.objects.all()
#     serializer_class = PublicacionSerializer

