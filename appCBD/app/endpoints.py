import requests
import json
from app.models import Estacion, Tramo

# The API endpoint
url = "https://api.tmb.cat/v1/transit"


def get_all_estations():
    # Get all data from the API
    app_id = "bfceaf53"
    app_key = "fa22db17bc133e3616538c432106cd78"
    # route = url + "/linies/metro?app_id=" + app_id + "&app_key=" + app_key
    route = url + "/estacions?app_id=" + app_id + "&app_key=" + app_key
    response = requests.get(route)
    res = response.json()
    del res['type'], res['numberMatched'], res['numberReturned'], res['timeStamp'], res['totalFeatures'], res['crs']
    list = []
    for estacio in res['features']:
        element = {}
        element['ID_ESTACIO'] = estacio['properties']['ID_ESTACIO']
        element['NOM_ESTACIO'] = estacio['properties']['NOM_ESTACIO']
        element['CODI_LINIAS'] = estacio['properties']['PICTO'] # Puede contener más de una linea
        list.append(estacio)
    # return json.dumps(res, indent=4, sort_keys=True, ensure_ascii=False)
    return list


def get_all_trams():
    # Get all data from the API
    app_id = "bfceaf53"
    app_key = "fa22db17bc133e3616538c432106cd78"
    list = []
    num_linias = 11
    for l in range(num_linias + 1):
        route = url + "/linies/metro/" + str(l) + "/trams?app_id=" + app_id + "&app_key=" + app_key
        response = requests.get(route)
        res = response.json()
        del res['type'], res['numberMatched'], res['numberReturned'], res['timeStamp'], res['totalFeatures'], res['crs']
        for tram in res['features']:
            element = {}
            element['CODI_TRAM_LINIA'] = tram['properties']['CODI_TRAM_LINIA']
            element['CODI_ESTACIO_INI'] = tram['properties']['CODI_ESTACIO_INI']
            element['NOM_ESTACIO_INI'] = tram['properties']['NOM_ESTACIO_INI']
            element['CODI_ESTACIO_FI'] = tram['properties']['CODI_ESTACIO_FI']
            element['NOM_ESTACIO_FI'] = tram['properties']['NOM_ESTACIO_FI']
            element['ORDRE_TRAM'] = tram['properties']['ORDRE_TRAM']
            element['NOM_LINIA'] = tram['properties']['NOM_LINIA']
            element['ORIGEN_SERVEI'] = tram['properties']['ORIGEN_SERVEI']
            element['DESTI_SERVEI'] = tram['properties']['DESTI_SERVEI']
            element['LONGITUD'] = tram['properties']['LONGITUD']
            list.append(element)
    # return json.dumps(res, indent=4, sort_keys=True, ensure_ascii=False)
    return list

def guardar_estaciones(estaciones):
    for est in estaciones:
        codi = est['properties']['ID_ESTACIO']
        nom = est['properties']['NOM_ESTACIO']
        linias = est['properties']['PICTO']  

        if Estacion.nodes.get_or_none(codi_estacio=codi) is None:
            Estacion(
                codi_estacio=codi,
                nom_estacio=nom,
                linias=linias
            ).save()

def guardar_tramos(tramos):
    for t in tramos:
        try:
            est_ini = Estacion.nodes.get(codi_estacio=str(t["CODI_ESTACIO_INI"]))
            est_fi = Estacion.nodes.get(codi_estacio=str(t["CODI_ESTACIO_FI"]))

            # Verificamos si ya existe la relación
            if est_ini.conecta_con.relationship(est_fi) is None:
                est_ini.conecta_con.connect(est_fi, {
                    "codi_tram_linia": t["CODI_TRAM_LINIA"],
                    "codi_estacio_ini": t["CODI_ESTACIO_INI"],
                    "nom_estacio_ini": t["NOM_ESTACIO_INI"],
                    "codi_estacio_fi": t["CODI_ESTACIO_FI"],
                    "nom_estacio_fi": t["NOM_ESTACIO_FI"],
                    "ordre_tram": t["ORDRE_TRAM"],
                    "nom_linia": t["NOM_LINIA"],
                    "origen_servei": t["ORIGEN_SERVEI"],
                    "desti_servei": t["DESTI_SERVEI"],
                    "longitud": t["LONGITUD"]
                })
        except Estacion.DoesNotExist:
            print(f"Estación no encontrada: {t['CODI_ESTACIO_INI']} o {t['CODI_ESTACIO_FI']}")


def guardar_datos():
    # Guardar estaciones
    estaciones = get_all_estations()
    guardar_estaciones(estaciones)

    # Guardar tramos
    tramos = get_all_trams()
    guardar_tramos(tramos)

# print(get_all_estations())
# print(get_all_trams())
guardar_datos()