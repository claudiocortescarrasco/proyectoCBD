import requests
import json
from app.models import Estacion, Tramo

# The API endpoint
url = "https://api.tmb.cat/v1/transit"


def get_all_code_lines():
    # Get all data from the API
    app_id = "bfceaf53"
    app_key = "fa22db17bc133e3616538c432106cd78"
    # route = url + "/linies/metro?app_id=" + app_id + "&app_key=" + app_key
    route = url + "/linies/metro?app_id=" + app_id + "&app_key=" + app_key
    response = requests.get(route)
    res = response.json()
    codis_linies = []
    for line in res['features']:
        codis_linies.append(line['properties']['CODI_LINIA'])

    return codis_linies

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


def get_all_trams(codis_linies_list):
    # Get all data from the API
    app_id = "bfceaf53"
    app_key = "fa22db17bc133e3616538c432106cd78"
    list = []
    # num_linias = 11
    for l in codis_linies_list:
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
            # Obtener nombres exactos desde el tramo
            nom_estacio_ini = t["NOM_ESTACIO_INI"].strip()
            nom_estacio_fi = t["NOM_ESTACIO_FI"].strip()

            # Buscar estaciones por nombre exacto
            est_ini = Estacion.nodes.get_or_none(nom_estacio=nom_estacio_ini)
            est_fi = Estacion.nodes.get_or_none(nom_estacio=nom_estacio_fi)

            if est_ini is None or est_fi is None:
                print(f"⚠️ Estación no encontrada: {nom_estacio_ini} o {nom_estacio_fi}")
                continue

            nom_linia = t["NOM_LINIA"].strip()

            # Ahora sí verificamos adicionalmente que las estaciones contengan la línea
            if nom_linia in est_ini.linias and nom_linia in est_fi.linias:
                # Comprobamos si la relación ya existe para evitar duplicados
                if est_ini.conecta_con.relationship(est_fi) is None:
                    est_ini.conecta_con.connect(est_fi, {
                        "codi_tram_linia": t["CODI_TRAM_LINIA"],
                        "ordre_tram": t["ORDRE_TRAM"],
                        "nom_linia": nom_linia,
                        "origen_servei": t["ORIGEN_SERVEI"],
                        "desti_servei": t["DESTI_SERVEI"],
                        "longitud": t["LONGITUD"],
                        # Datos opcionales (estaciones origen/destino):
                        "nom_estacio_ini": nom_estacio_ini,
                        "nom_estacio_fi": nom_estacio_fi,
                        "codi_estacio_ini": t["CODI_ESTACIO_INI"],
                        "codi_estacio_fi": t["CODI_ESTACIO_FI"],
                    })
                else:
                    print(f"✅ Ya existe relación entre {nom_estacio_ini} y {nom_estacio_fi}")
            else:
                print(f"⚠️ No coincide línea '{nom_linia}' en estaciones {nom_estacio_ini} y {nom_estacio_fi}")

        except Exception as e:
            print(f"❌ Error al guardar tramo {nom_estacio_ini}→{nom_estacio_fi}: {e}")



def guardar_datos():
    # Guardar estaciones
    estaciones = get_all_estations()
    guardar_estaciones(estaciones)

    # Guardar tramos
    tramos = get_all_trams(get_all_code_lines())
    guardar_tramos(tramos)

# print(get_all_estations())
# print(get_all_trams())
guardar_datos()
# print(get_all_code_lines())