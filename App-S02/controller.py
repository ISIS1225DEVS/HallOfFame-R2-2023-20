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
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller(size, map_type, loadFactor):
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la funcixón del modelo que crea las estructuras de datos
    control = {
        'model': None
    }
    control['model'] = model.newCatalog(size, map_type, loadFactor)
    return control

# Funciones para la carga de datos

  
def load_data(catalog, filesize, memflag=True):
    """
    Carga los datos del reto en cada archivo.
    """
    
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    
    
    partido= load_files(me.getValue(mp.get(catalog['model']['partidos'], 'partidos')), filesize, 'partidos')

    goleadores= merg.sort(load_files(me.getValue(mp.get(catalog['model']['partidos'], 'goleadores')), filesize, 'goleadores'), model.compare_dates_ind )

    penales= merg.sort(load_files(me.getValue(mp.get(catalog['model']['partidos'], 'penales')), filesize, 'penales'), model.compare_dates_ind)

    
    partido_1 = load_partidos_1(catalog['model'], filesize)
    
    goleadores_1 = load_golea_map(catalog['model'])
    
    
    catalog['model']['individuales'] = (goleadores, penales)
    
    respuesta, totales = load_partidos(catalog, partido, goleadores, penales)
    load_otros(catalog)
    
    

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return (delta_time, delta_memory), totales

    else:
        # respuesta sin medir memoria
        return delta_time, totales
    
def load_files(catalog, filesize, filename): 
    """
    Utiliza la función del modelo para cargar los 3 primeros archivos a la estructura.
    """
    if filename == 'partidos': 
        csv_file = 'results'
    elif filename == 'goleadores':
        csv_file = 'goalscorers'
    elif filename == 'penales': 
        csv_file = 'shootouts'
    fileLoad = cf.data_dir + f'football/{csv_file}-utf8-{filesize}.csv'
    input_file = csv.DictReader(open(fileLoad, encoding='utf-8'))
    for element in input_file:
        model.add_element(catalog, element, filename)
    return catalog

def load_partidos(catalog, partidos, goleadores, penales):
    """
    Carga los datos del reto
    """
    tot_p = lt.size(partidos)
    tot_g = lt.size(goleadores)
    tot_i = lt.size(penales)
    
    merge= model.mergeFiles(catalog['model'], partidos, goleadores, penales)

    catalog['model']['partidos'] = merge
    return catalog , (tot_p, tot_g, tot_i)




def load_otros(catalog): 
    return model.load_otros(catalog)



    
def load_partidos_1(catalog, filesize):
    """
    Carga los datos del reto
    """
    
    partidos_load = cf.data_dir + f'football/results-utf8-{filesize}.csv'
    input_file = csv.DictReader(open(partidos_load, encoding='utf-8'))
    for element in input_file:
        model.add_partidos_1(catalog, element)
    
    goleadores_load = cf.data_dir + f'football/goalscorers-utf8-{filesize}.csv'
    ginput_file = csv.DictReader(open(goleadores_load, encoding='utf-8'))
    
    goleadores= model.load_goleadores_penales(ginput_file)
    
    merge= model.mergeFiles2(catalog['partidos_1'], goleadores)

    catalog['Merge_part_jug'] = merge
    
    return catalog


def load_golea_map(catalog): 
    """
    Utiliza la función del modelo para cargar los 3 primeros archivos a la estructura.
    """
    return model.load_equ_tor(catalog)


#############3333333333

# Funciones de ordenamiento


def sortData(catalog, size,  filename): 
    return model.sortData(catalog['model'], size,  filename)

# Funciones de consulta sobre el catálogo


def req_1(catalog, n, equipo, condicion, memflag=True):
    """
    Retorna el resultado del requerimiento 1
    """
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    lista_n, totales= model.req_1(catalog['model'], n, equipo, condicion)
    
    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return (delta_time, delta_memory), lista_n, totales

    else:
        # respuesta sin medir memoria
        return delta_time, lista_n, totales


def req_2(catalog, goleador, n, memflag=True):
    """
    Retorna el resultado del requerimiento 1
    """
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    resultado, suma, total, penal = model.req_2(catalog['model'], goleador,n)
    
    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return (delta_time, delta_memory), resultado, suma, total, penal

    else:
        # respuesta sin medir memoria
        return delta_time, resultado, suma, total, penal    


def req_3(catalog, equipo, fi, ff, memflag=True):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = getTime()
    
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    
    final, numero_par, home, away, numero_equipos= model.req_3(catalog['model'], equipo, fi, ff)
    stop_time= getTime()
    
    delta_time= deltaTime(stop_time, start_time)
    
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory= deltaMemory(stop_memory, start_memory)
        return (delta_time, delta_memory), final, numero_par, home, away,numero_equipos
    else:
        return delta_time, final, numero_par, home, away, numero_equipos


def req_4(catalog, torneo, fecha_i, fecha_f, memflag=True ):
    """
    Retorna el resultado del requerimiento 4
    """
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    lista_n, totales= model.req_4(catalog['model'], torneo, fecha_i, fecha_f)
    
    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return (delta_time, delta_memory), lista_n, totales

    else:
        # respuesta sin medir memoria
        return delta_time, lista_n, totales


def req_5(catalog, goleador, fecha_i, fecha_f, memflag):

    """
    Retorna el resultado del requerimiento 5
    """
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
        
    resultado, suma, total, tot_torneos, penalty, auto = model.req_5(catalog['model'], goleador, fecha_i, fecha_f)

    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return (delta_time, delta_memory), resultado, suma, total, tot_torneos, penalty, auto

    else:
        # respuesta sin medir memoria
        return delta_time, resultado, suma, total, tot_torneos, penalty, auto

def req_6(catalog, n, torneo, year, memflag=True):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    (totales_de_equipos, totales_generales)= model.req_6(catalog['model'], n , torneo, year)
    
    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return (delta_time, delta_memory), (totales_de_equipos, totales_generales)

    else:
        # respuesta sin medir memoria
        return delta_time, (totales_de_equipos, totales_generales)


def req_7(catalog, torneo, n, memflag=True):
    """
    Retorna el resultado del requerimiento 1
    """
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    lista_jugadores, totales = model.req_7(catalog['model'], torneo, n)
    
    # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return (delta_time, delta_memory), lista_jugadores, totales

    else:
        # respuesta sin medir memoria
        return delta_time, lista_jugadores, totales


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para medir la memoria utilizada


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
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