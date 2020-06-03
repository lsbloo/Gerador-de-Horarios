from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class CreateUpdateModel(models.Model):

    created_at = models.DateTimeField(
        'criado em',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'atualizado em',
        auto_now=True
    )

    class Meta:
        abstract = True

# Create your models here.
class Criterion(CreateUpdateModel):
    name = models.CharField(verbose_name="nome",max_length=100,editable=True)
    description = models.CharField(verbose_name="descricao", max_length=255,editable=True)
    rate = models.IntegerField(verbose_name="peso",editable=True)
    constraint = models.CharField(verbose_name="constraint",max_length=100,editable=True)


    class Meta:
        verbose_name = "Critério"
        verbose_name_plural = "Critérios"
        ordering = ['rate']

    def __str__(self):
        return self.name

class KitKatUser(CreateUpdateModel):
    username = models.CharField(verbose_name="username",max_length=100,editable=True)
    email = models.CharField(verbose_name="email",max_length=100,editable=True)
    password = models.CharField(verbose_name="email",max_length=100,editable=True)
    is_staff = models.BooleanField(verbose_name="admin",editable=True)
    

    class Meta:
        verbose_name="Kitkat User"
        verbose_name_plural= "Kitkat Users"
        ordering = ['username']
    
    def __str__(self):
        return self.username


