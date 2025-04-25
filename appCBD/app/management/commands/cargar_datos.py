from django.core.management.base import BaseCommand
from app.endpoints import get_all_code_lines, get_all_estations, get_all_trams, guardar_estaciones, guardar_tramos


class Command(BaseCommand):
    help = 'Carga estaciones y tramos desde la API de TMB'

    def handle(self, *args, **kwargs):
        print("Obteniendo estaciones...")
        estaciones = get_all_estations()
        guardar_estaciones(estaciones)

        print("Obteniendo tramos...")
        tramos = get_all_trams(get_all_code_lines())
        guardar_tramos(tramos)

        self.stdout.write(self.style.SUCCESS('Datos cargados correctamente.'))