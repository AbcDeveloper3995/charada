from django.contrib.auth.models import AbstractUser
from django.db import models
from charada.settings import MEDIA_URL, STATIC_URL

class Usuario(AbstractUser):
    fechaCaducidad = models.DateField(verbose_name='Fecha de caducidad', blank=True, null=True)

    class Meta:
        db_table = 'Usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        else:
            query = Usuario.objects.get(pk=self.pk)
            if query.password != self.password:
                self.set_password(self.password)
        super().save(*args, **kwargs)