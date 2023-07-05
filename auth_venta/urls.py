from django.contrib import admin
from django.urls import path, include
from accounts.consumers import MensajeConsumer
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include("accounts.urls")),

    #Websocket
    path('ws/mensajes/', MensajeConsumer.as_asgi()),
   
]
