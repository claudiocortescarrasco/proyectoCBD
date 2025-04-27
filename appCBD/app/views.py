from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from app.endpoints import guardar_datos
from django.contrib import messages
from app.models import Estacion
import re
from neomodel import db


# Create your views here.
def home(request):
    return render(request, "home.html")


@require_POST
def load_stations(request):
    try:
        guardar_datos()
        messages.success(request, "Datos cargados correctamente desde la API.")
    except Exception as e:
        messages.error(request, f"Error al cargar los datos: {str(e)}")
    return redirect("home")


def lines_list(request):
    lineas = {}

    # Recorrer todas las estaciones
    for estacion in Estacion.nodes.all():
        for est_fi in estacion.conecta_con:
            rel = estacion.conecta_con.relationship(
                est_fi
            )

            nombre_linea = rel.nom_linia
            orden_tramo = rel.ordre_tram

            if nombre_linea not in lineas:
                lineas[nombre_linea] = []

            lineas[nombre_linea].append(
                (orden_tramo, rel.nom_estacio_ini, rel.nom_estacio_fi)
            )

    resultado_final = {}

    for linea, tramos in lineas.items():
        tramos_ordenados = sorted(tramos, key=lambda x: x[0])

        estaciones = []
        for orden, est_ini, est_fi in tramos_ordenados:
            if not estaciones:
                estaciones.append(est_ini)
            if est_fi not in estaciones:
                estaciones.append(est_fi)

        resultado_final[linea] = estaciones

    return render(request, "lines_list.html", {"lineas": resultado_final})


def line_form(request):
    lineas_set = set()

    for estacion in Estacion.nodes.all():
        lineas_encontradas = re.findall(r"(?:L\d{1,2}(?:N|S)?|FM)", estacion.linias)
        lineas_set.update(lineas_encontradas)

    lineas = sorted(lineas_set)
    return render(request, "line_form.html", {"lineas": lineas})


def line_stations(request):
    if request.method == "POST":
        linea_seleccionada = request.POST.get("linea")
        estaciones = []

        for estacion in Estacion.nodes.all():
            lineas_encontradas = re.findall(r"(?:L\d{1,2}(?:N|S)?|FM)", estacion.linias)
            if linea_seleccionada in lineas_encontradas:
                estaciones.append(estacion.nom_estacio)

        estaciones = sorted(estaciones)

        lineas_set = set()
        for estacion in Estacion.nodes.all():
            lineas_encontradas = re.findall(r"(?:L\d{1,2}(?:N|S)?|FM)", estacion.linias)
            lineas_set.update(lineas_encontradas)

        lineas = sorted(lineas_set)

        return render(
            request,
            "line_form.html",
            {
                "lineas": lineas,
                "estaciones": estaciones,
                "linea_seleccionada": linea_seleccionada,
            },
        )
    else:
        return redirect("line_form")


def line_stations_by_pk(request, pk):
    return redirect("home")


def station_form(request):
    estaciones = Estacion.nodes.all()
    nombre_estaciones = sorted([e.nom_estacio for e in estaciones])

    if request.method == "POST":
        nombre_estacion = request.POST.get("estacion")
        estacion = Estacion.nodes.get_or_none(nom_estacio=nombre_estacion)

        if estacion:
            lineas_separadas = re.findall(r"(?:L\d{1,2}(?:N|S)?|FM)", estacion.linias)

            lineas_formateadas = " ".join(f"[{linea}]" for linea in lineas_separadas)

            cantidad_lineas = len(lineas_separadas)

            return render(
                request,
                "station_form.html",
                {
                    "estaciones": nombre_estaciones,
                    "lineas_formateadas": lineas_formateadas,
                    "estacion_seleccionada": nombre_estacion,
                    "cantidad_lineas": cantidad_lineas,
                },
            )
        else:
            return render(
                request,
                "station_form.html",
                {"estaciones": nombre_estaciones, "error": "Estación no encontrada"},
            )

    return render(request, "station_form.html", {"estaciones": nombre_estaciones})


def station_line(request, pk):
    try:
        estacion = Estacion.nodes.get(codi_estacio=str(pk))

        lineas_crudas = estacion.linias
        lineas = [lineas_crudas[i : i + 3] for i in range(0, len(lineas_crudas), 3)]

        if len(lineas) == 1:
            lineas_formateadas = lineas[0]
        else:
            lineas_formateadas = ", ".join(lineas[:-1]) + " y " + lineas[-1]

        return render(
            request,
            "station_line.html",
            {"estacion": estacion.nom_estacio, "lineas": lineas_formateadas},
        )

    except Estacion.DoesNotExist:
        return render(
            request, "station_line.html", {"error": "Estación no encontrada."}
        )


def route_form(request):
    estaciones = Estacion.nodes.all()
    nombre_estaciones = sorted([e.nom_estacio for e in estaciones])

    return render(request, "route_form.html", {"estaciones": nombre_estaciones})


def route_stations(request):
    if request.method == "POST":
        origen = request.POST.get("origen")
        destino = request.POST.get("destino")

        if origen and destino:
            query = """
            MATCH (start:Estacion {nom_estacio: $origen}), (end:Estacion {nom_estacio: $destino})
            MATCH path = shortestPath((start)-[:TRAMO*]-(end))
            RETURN [n IN nodes(path) | {nombre: n.nom_estacio, lineas: n.linias}] AS estaciones
            """

            results, _ = db.cypher_query(query, {"origen": origen, "destino": destino})
            if results and results[0]:
                estaciones = results[0][0]  
                
                for estacion in estaciones:
                    lineas_raw = estacion["lineas"] if estacion["lineas"] else ""
                    estacion["lineas"] = re.findall(r"L\d{1,2}(?:N|S)?|FM", lineas_raw)

            else:
                estaciones = []

            return render(
                request,
                "route_stations.html",
                {"origen": origen, "destino": destino, "estaciones": estaciones},
            )

    return redirect("route_form")
