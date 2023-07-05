from django.urls import path
from .views import CreatePublicacion, CategoriaListAPIView, UploadImageView, ImagenListView, ObtenerImagenesView, ImagenesPublicacionAPI

urlpatterns = [
    #path('publicaciones/', PublicacionListCreateView.as_view(), name='publicacion-list-create'),
    path('p/create/', CreatePublicacion.as_view(), name='post_create'),
    path('imagenes/', ImagenListView.as_view(), name='imagen-list'),
    path('obtener-imagenes/', ObtenerImagenesView.as_view(), name='obtener_imagenes'),
    path('api/imagenes-publicacion/', ImagenesPublicacionAPI.as_view(), name='imagenes-publicacion'),
    path('api/upload-image/', UploadImageView.as_view(), name='upload_image'),
    path('api/categorias/', CategoriaListAPIView.as_view(), name='categoria-list'),
]

