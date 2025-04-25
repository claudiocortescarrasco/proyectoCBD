from neomodel import StructuredNode, StructuredRel, StringProperty, IntegerProperty, FloatProperty, RelationshipTo

class Tramo(StructuredRel):
    # Esta clase representa la relación entre dos estaciones y permite agregar propiedades a la conexión
    codi_tram_linia = StringProperty(unique_index=True, required=True)  # id del tramo
    codi_estacio_ini = IntegerProperty(required=True)  # código de la estación inicial
    nom_estacio_ini = StringProperty(required=True)  # nombre de la estación inicial
    codi_estacio_fi = IntegerProperty(required=True)  # código de la estación final
    nom_estacio_fi = StringProperty(required=True)  # nombre de la estación final
    ordre_tram = IntegerProperty(required=True)  # orden del tramo en la línea
    nom_linia = StringProperty(required=True)  # nombre de la línea
    origen_servei = StringProperty(required=True)  # estacion origen de la linea a la que pertenece esta estacion
    desti_servei = StringProperty(required=True)  # estacion destino de la linea a la que pertenece esta estacion
    longitud = FloatProperty()  # Distancia entre estaciones en metros
    # num_total_trams_linia = IntegerProperty(required=True)  # Número total de tramos en la línea (atrib totalFeatures del JSON de respuesta)



class Estacion(StructuredNode):
    codi_estacio = StringProperty(unique_index=True, required=True)  # código de estación
    nom_estacio = StringProperty(required=True) # nombre de la estacion
    linias = StringProperty(required=True)  # líneas a las que pertenece la estación

    # Relación con otras estaciones
    conecta_con = RelationshipTo('Estacion', 'TRAMO', model=Tramo)

