# myapp/models.py
from django.db import models

class Camioneta(models.Model):
    patente = models.CharField(max_length=10, primary_key=True)
    estado = models.IntegerField(choices=[(0, 'Disponible'), (1, 'En arriendo'), (2, 'En mantenimiento')])

    def __str__(self):
        return self.patente
