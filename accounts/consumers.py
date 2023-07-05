from django.contrib.auth import get_user_model
import json
from .models import Publicacion, Imagen, UserAccount
from channels.generic.websocket import AsyncWebsocketConsumer

User = get_user_model()
class MensajeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, close_code):
        pass
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data['tipo'] == 'busqueda':
            termino = data['termino']
            print(termino)
            
            # Realizar la búsqueda de usuarios por nombre o cualquier otro campo de UserAccount
            resultados = UserAccount.objects.filter(email__icontains=termino)
            
            # Serializar los resultados para enviarlos a través de WebSocket
            resultados_serializados = [{'id': resultado.id, 'nombre': resultado.nombre} for resultado in resultados]
            
            # Enviar los resultados a través de WebSocket
            await self.send(text_data=json.dumps({'resultados': resultados_serializados}))