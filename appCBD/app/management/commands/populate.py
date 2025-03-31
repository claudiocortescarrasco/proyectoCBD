from django.core.management.base import BaseCommand
from app.models import Estacion

class Command(BaseCommand):
    help = "Popula la base de datos con datos iniciales del Metro de Madrid"

    def handle(self, *args, **options):
        self.stdout.write("Limpiando la base de datos...")

        # Eliminar todas las estaciones existentes para evitar duplicados
        for estacion in Estacion.nodes:
            estacion.delete()

        self.stdout.write("Poblando la base de datos...")

        # Crear dos estaciones de ejemplo
        atochas = Estacion(
            nombre="Atocha",
            linea="Línea 1",
            direccion="Avenida de la Paz, Madrid"
        ).save()

        sol = Estacion(
            nombre="Sol",
            linea="Línea 1",
            direccion="Plaza del Sol, Madrid"
        ).save()

        # Conectar Atocha con Sol, indicando que el viaje dura 3 minutos
        atochas.conexiones.connect(sol, {'tiempo': 3})

        self.stdout.write(self.style.SUCCESS("Base de datos poblada exitosamente."))
