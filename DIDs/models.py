from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class DID(models.Model):
    numero = models.CharField(max_length=15)
    pais = models.CharField(max_length=30)
    empresa = models.CharField(max_length=30)
    minutos_uso = models.IntegerField()

    def __str__(self): 
        
        return f"DID: {self.numero}, País: {self.pais}, Empresa: {self.empresa}"

class Tarifa(models.Model):
    trafico_entrante = models.DecimalField(max_digits=6, decimal_places=4)
    trafico_saliente = models.DecimalField(max_digits=6, decimal_places=4)
    precio_por_numero = models.DecimalField(max_digits=6, decimal_places=4)
    pais = models.CharField(max_length=30)

    def __str__(self): 
        
        return f"Tarifa para {self.pais}: Entrante {self.trafico_entrante}, Saliente {self.trafico_saliente}, Precio por Número {self.precio_por_numero}"

class Compania(models.Model):
    direccion = models.CharField(max_length=60)
    codigo_postal = models.IntegerField()
    nombre = models.CharField(max_length=60)
    persona_contacto = models.CharField(max_length=60)
    NOCemail = models.EmailField()

    def __str__(self): 
        
        return f"Compañía: {self.nombre}, Dirección: {self.direccion}, Contacto: {self.persona_contacto}"
    


User = get_user_model()

class TroubleTicket(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    ticket = models.ForeignKey(TroubleTicket, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.ticket}'
