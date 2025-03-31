from neomodel import StructuredNode, StructuredRel, StringProperty, FloatProperty, RelationshipTo

# Esta clase representa la relación entre dos estaciones y permite agregar propiedades a la conexión
class Conexion(StructuredRel):
    tiempo = FloatProperty(required=True)  # Tiempo de viaje entre estaciones en minutos

# Este nodo representa una estación del metro
class Estacion(StructuredNode):
    nombre = StringProperty(unique_index=True, required=True)
    linea = StringProperty(required=True)
    direccion = StringProperty()  # Dirección o ubicación textual de la estación

    # Conexión a otras estaciones usando el tipo de relación "CONECTA" y el modelo Conexion
    conexiones = RelationshipTo("Estacion", "CONECTA", model=Conexion)
