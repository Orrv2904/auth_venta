from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import UserManager

class UserAccountManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image_perfil = models.ImageField(upload_to='images/muapp/profile/', blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
    


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Publicacion(models.Model):
    autor = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField(null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.titulo} {self.fecha_publicacion}"

class Imagen(models.Model):
    publicacion = models.ForeignKey(Publicacion, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='images/muapp/', blank=True, null=True)

class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')
    autor_coment = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comentario de {self.autor.username} en "{self.publicacion.titulo}"'
    
class Mensaje(models.Model):
    emisor = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)


