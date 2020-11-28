from django.core.management.base import BaseCommand, CommandError
from push_notifications.models import GCMDevice
from ...models import Precos

class Command(BaseCommand):
    help = 'Envia mensagem para o aplicativo'

    def handle(self, *args, **options):

        precos = Precos.objects.all()
        soma = 0

        for preco in precos:
            soma = soma + preco.gasolina         

        devices = GCMDevice.objects.all()
        
        devices.send_message("O preço da gasolina está em média: " + "R${:,.2f}".format(soma/len(precos)))
        
