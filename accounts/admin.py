from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Publicacion)
admin.site.register(Imagen)
admin.site.register(Categoria)