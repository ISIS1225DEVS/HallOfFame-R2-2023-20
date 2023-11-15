"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import time
import csv
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller(tipo, factorcarga):
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos

    control = {
        model:None
    }
    control = model.new_data_structs(tipo, factorcarga)
    

    return control
        

def load_goleadores_m(control, tamanho,):
    """
    Carga los datos del reto
    """

    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()

#logica

    file =  cf.data_dir+"/football/goalscorers-utf8-" + tamanho + ".csv"
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for goalscorer in input_file:
        info = model.add_goleadores_m(control,goalscorer)
        

#fin logica
    stop_time = get_time()
    delta_time_2 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_2=delta_memory(stop_memory, start_memory)
    return info, delta_time_2, delta__memory_2

def load_torneo(control, tamanho,):
    """
    Carga los datos del reto
    """

    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()

#logica

    file =  cf.data_dir+"/football/results-utf8-" + tamanho + ".csv"
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for goalscorer in input_file:
        info = model.add_torneo(control,goalscorer)
        

#fin logica
    stop_time = get_time()
    delta_time_3 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_3=delta_memory(stop_memory, start_memory)
    return info, delta_time_3, delta__memory_3


def load_hometeam(control, tamanho,):
    """
    Carga los datos del reto
    """

    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()

#logica

    file =  cf.data_dir+"/football/results-utf8-" + tamanho + ".csv"
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for goalscorer in input_file:
        info = model.add_hometeam(control,goalscorer)
        

#fin logica
    stop_time = get_time()
    delta_time_4 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_4=delta_memory(stop_memory, start_memory)
    return info, delta_time_4, delta__memory_4

def load_awayteam(control, tamanho,):
    """
    Carga los datos del reto
    """

    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()

#logica

    file =  cf.data_dir+"/football/results-utf8-" + tamanho + ".csv"
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for goalscorer in input_file:
        info = model.add_awayteam(control,goalscorer)
        

#fin logica
    stop_time = get_time()
    delta_time_5 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_5=delta_memory(stop_memory, start_memory)
    return info, delta_time_5, delta__memory_5



def load_data_shoootouts(control,tamanho):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()
    
    #logica
         
    fila = 0
    Shootouts_file = cf.data_dir+"/football/shootouts-utf8-" + tamanho + ".csv"
    input_file = csv.DictReader(open(Shootouts_file, encoding="utf8"))
    for shootout in input_file:
        info = model.add_shotouts(control,shootout)
        fila += 1

    #fin logica

    stop_time = get_time()
    delta_time_6 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_6=delta_memory(stop_memory, start_memory)

    return info, fila,delta_time_6,delta__memory_6

def load_data_results(control,tamanho):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()
    
    #logica
    fila = 0
    Results_file = cf.data_dir+"/football/results-utf8-" + tamanho + ".csv"
    input_file = csv.DictReader(open(Results_file, encoding="utf8"))
    for result in input_file:
        info = model.add_results(control,result)
        fila += 1
        
    #fin logica

    stop_time = get_time()
    delta_time_7 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_7=delta_memory(stop_memory, start_memory)
    return info, fila,delta_time_7,delta__memory_7

def load_data_goalscorers(control,tamanho):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    memflag=True
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory =get_memory()
    fila = 0
    Goalscorers_file = cf.data_dir+"/football/goalscorers-utf8-" + tamanho + ".csv"
    input_file = csv.DictReader(open(Goalscorers_file, encoding="utf8"))
    for goalscorer in input_file:
        info = model.add_goalscorers(control,goalscorer)
        fila += 1
        
    #fin logica

    stop_time = get_time()
    delta_time_8 = stop_time- start_time
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        delta__memory_8=delta_memory(stop_memory, start_memory)
    return info, fila,delta_time_8,delta__memory_8


# Funciones de ordenamiento

def sort(control,s):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    return model.sort(control,s)


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, numero_partidos,nombre_equipo,condicion_equipo):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1    
    start_time=get_time()
    lista = model.req_1(control, numero_partidos,nombre_equipo,condicion_equipo)
    stop_time=get_time()
    delta_time_r=delta_time(start_time,stop_time)
    for i in lista['elements']:
        del i['neutral']
    return lista['elements'], delta_time_r

def req_2(control,goles,goleador):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time=get_time()
    lista=model.req_2(control,goles,goleador)
    stop_time=get_time()
    delta_time_r=delta_time(start_time,stop_time)
    return lista["elements"],delta_time_r


def req_3(control, nombre_equipo, fecha_inicial, fecha_final):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()

    lista, num_partidos, num_partidos_equipo, num_home, num_away= model.req_3(control, nombre_equipo, fecha_inicial, fecha_final)
    for i in lista['elements']:
        del i['neutral']

    stop_time = get_time()
    delta_time = stop_time- start_time

    return lista['elements'], num_partidos, num_partidos_equipo, num_home, num_away, delta_time
    


def req_4(control, nombre_torneo,fecha_i,fecha_f):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    start_time=get_time()
    r = model.req_4(control, nombre_torneo,fecha_i,fecha_f)
    stop_time=get_time()
    delta_time_r=delta_time(start_time,stop_time)
    return r,delta_time_r




def req_5(control,nombre_jugador,fecha_inicial,fecha_final):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    start_time=get_time()
    lista = model.req_5(control,nombre_jugador,fecha_inicial,fecha_final)
    stop_time=get_time()
    delta_time_r=delta_time(start_time,stop_time)
    torneos = 0
    lista_torneo = []
    penaltis = 0
    autogoles = 0
    for i in lista:

        if i['tournament'] not in lista_torneo:
            lista_torneo.append(i['tournament'])
            torneos += 1
        if i['penalty']:
            penaltis +=1
        if i['own_goal']:
            autogoles +=1
    return lista,torneos,penaltis,autogoles,delta_time_r

def req_6(control, nombre_torneo, anio, num_equipos: int):
    """
    Retorna el resultado del requerimiento 6
    """    

    # TODO: Modificar el requerimiento 6

    start_time=get_time()

    respuesta_general, lista  = model.req_6(control, nombre_torneo, anio)

    end_time=get_time()
    diferencia_t=delta_time(start_time,end_time)
    clave = 'Puntos totales'

    lista_ordenada = sorted(lista, key=lambda x:x[clave], reverse = True)

    mejores = lista_ordenada[:num_equipos]


    return mejores, respuesta_general, diferencia_t


def req_7(control, torneo, puntos):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    start_time=get_time()
    lista = model.req_7(control, torneo, puntos)
    end_time=get_time()
    diferencia_t=delta_time(start_time,end_time)
    r = []
    clave_orden = 'puntos'

    lista_ordenada = sorted(lista, key=lambda x:x[clave_orden], reverse = True)

    
    total_goles = 0
    total_penaltis = 0
    total_autogoles = 0
    for i in lista_ordenada:

        del i['fecha']
        del i['team']
        total_goles += i['goles_totales']
        total_penaltis += i['goles_penal']
        total_autogoles += i['auto_goles']
        del i['último_gol']['fecha']

        if i['puntos'] == puntos:
            r.append(i)


    total_jugadores = len(r)


    return r,total_goles,total_penaltis,total_autogoles,total_jugadores,diferencia_t


def req_8(control, pais, anio_i, anio_f):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    start_time=get_time()
    lista = model.req_8(control, pais, anio_i, anio_f)
    end_time=get_time()
    diferencia_t=delta_time(start_time,end_time)

    return lista,diferencia_t


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
