from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import User, AbstractUser

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('E-mail', unique=True,)    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Posto(models.Model):
    user = models.OneToOneField(CustomUser,
                                      on_delete=models.CASCADE)
    nome = models.CharField(max_length=300, default="Posto")                                  
    cnpj = models.CharField(max_length=30)
    ltd = models.CharField(max_length=30)
    lgt = models.CharField(max_length=30)    

    def __str__(self):
        return f'Nome do posto: {self.user.first_name}'

class Precos(models.Model):
    gasolina = models.DecimalField(max_digits=6, decimal_places=3)
    aditivada = models.DecimalField(max_digits=6, decimal_places=3)
    alcool = models.DecimalField(max_digits=6, decimal_places=3)
    diesel = models.DecimalField(max_digits=6, decimal_places=3)
    gnv = models.DecimalField(max_digits=6, decimal_places=3)  
    etanol = models.DecimalField(max_digits=6, decimal_places=3, default=0)  

    posto = models.OneToOneField(Posto, related_name='preco', on_delete=models.CASCADE)  

    def __str__(self):
        return f'{self.id}'  

class Denuncia(models.Model):
    ESCOLHAS = (
        (1, "Preço divulgado está diferente no estabelecimento"),
        (2, "Posto não encontrado na localidade"),
        (3, "Problemas com o atendimento"),
        (4, "Outros")
    )
    denuncia = models.IntegerField(choices=ESCOLHAS)
    motivos = models.CharField(max_length=100, blank=True)
    posto = models.ForeignKey(Posto, related_name='denuncia', on_delete=models.CASCADE)  



   




