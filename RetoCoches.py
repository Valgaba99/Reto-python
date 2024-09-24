import csv
import json
from collections import defaultdict
from math import radians, sin, cos, sqrt, atan2
import datetime

class Coche:
    def __init__(self, matricula, latitud, longitud, distance, pos_date):
        self.matricula = matricula
        self.latitud = float(latitud)
        self.longitud = float(longitud)
        self.distance = float(distance)
        self.pos_date = int(pos_date)

contador = 1
listamatriculas = []
listalatitudes = []
listalongitudes = []
listadistances = []
listaposdates = []

diccionario_coches = {}

# CASO 1
with open('reto.csv', 'r') as file:
    reader = csv.reader(file)

    #for row in reader:
        #print(row)

# CASO 2
with open('reto.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Saltar la cabecera

    for row in reader:
        matriculas = row[0]
        latitudes = row[1]
        longitudes = row[2]
        distances = row[3]
        pos_dates = row[4]
        listamatriculas.append(matriculas)
        listalatitudes.append(latitudes)
        listalongitudes.append(longitudes)
        listadistances.append(distances)
        listaposdates.append(pos_dates)

for matricula, latitud, longitud, distance, pos_date in zip(listamatriculas, listalatitudes, listalongitudes, listadistances, listaposdates):
    coche = Coche(matricula, latitud, longitud, distance, pos_date)
    diccionario_coches[contador] = coche
    contador = contador + 1


json_coches = {k: coche.__dict__ for k, coche in diccionario_coches.items()}

json_output = json.dumps(json_coches, indent=4)
#print(json_output)

# CASO 3
data = json.loads(json_output)

# Agrupar las distancias por matrícula
distances_por_matricula = defaultdict(float)
for coche in data.values():
    matricula = coche['matricula']
    distance = coche['distance']
    distances_por_matricula[matricula] += distance

#for matricula, total_distance in distances_por_matricula.items():
    #print(f'Matrícula: {matricula}, Distancia total: {total_distance}')

#4
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


grouped_data = {}
for key, value in data.items():
    matricula = value['matricula']
    if matricula not in grouped_data:
        grouped_data[matricula] = []
    grouped_data[matricula].append(value)

sum_distances = {}
for matricula, records in grouped_data.items():
    total_distance = 0.0
    for i in range(len(records) - 1):
        lat1, lon1 = records[i]['latitud'], records[i]['longitud']
        lat2, lon2 = records[i + 1]['latitud'], records[i + 1]['longitud']
        total_distance += haversine(lat1, lon1, lat2, lon2)
    sum_distances[matricula] = total_distance


#for matricula, total_distance in sum_distances.items():
    #print(f'Matrícula: {matricula}, Distancia total: {total_distance}' + ' km')


# CASO 5

def convertir_posix_a_fecha(posix_timestamp):
    fecha_hora = datetime.datetime.fromtimestamp(posix_timestamp / 1000)
    fecha_formateada = fecha_hora.strftime("%d/%m/%Y %H:%M:%S:%f")
    return fecha_formateada


def obtener_ultima_posicion_por_matricula(datos):
    datos_ordenados = sorted(datos, key=lambda x: x['pos_date'], reverse=True)

    ultima_posicion = {}
    for dato in datos_ordenados:
        matricula = dato['matricula']
        fecha = convertir_posix_a_fecha(dato['pos_date'])
        if matricula not in ultima_posicion or fecha > ultima_posicion[matricula]['fecha']:
            ultima_posicion[matricula] = {
                'fecha': fecha,
                'latitud': dato['latitud'],
                'longitud': dato['longitud']
            }
    return ultima_posicion

ultima_posicion = obtener_ultima_posicion_por_matricula(data.values())

def agregarRegistros(coche):
    entrada = open('ultimaposicion.txt','a', encoding='utf-8')
    entrada.write(coche)
    entrada.close()

with open('ultimaposicion.txt', 'w', encoding='utf-8'):
    pass

for matricula, info in ultima_posicion.items():
    #print(f"Matrícula: {matricula}, Fecha: {info['fecha']}, Latitud: {info['latitud']}, Longitud: {info['longitud']}")
    agregarRegistros(f"Matricula: {matricula}, Fecha: {info['fecha']}, Latitud: {info['latitud']}, Longitud: {info['longitud']}" + "\n")

#print(ultima_posicion.items())

# CASO 6
diccionario_coches_ultimas_posiciones = {}
contador = 1

with open("ultimaposicion.txt") as archivo:
    lineas = archivo.readlines()
    for linea in lineas:
        partes = linea.strip().split(", ")
        matricula = partes[0].split(": ")[1]
        fecha = partes[1].split(": ")[1]
        latitud = float(partes[2].split(": ")[1])
        longitud = float(partes[3].split(": ")[1])

        diccionario_coches_ultimas_posiciones[contador] = {
            "Matricula": matricula,
            "Fecha": fecha,
            "Latitud": latitud,
            "Longitud": longitud
        }
        contador = 1 + contador
#print(diccionario_coches_ultimas_posiciones)
json_coches_ordenados = json.dumps(diccionario_coches_ultimas_posiciones, indent=4)
#print(json_coches_ordenados)

