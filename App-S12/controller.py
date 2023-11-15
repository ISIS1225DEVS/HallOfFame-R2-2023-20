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


def new_controller(listType):
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        'model': None
    }
    control['model'] = model.new_catalog(listType)
    return control

# Funciones para la carga de datos
def load_data(control, filesize):

    catalog = control['model']
    resultados = load_partidos(catalog, filesize)
    goles = load_goles(catalog, filesize)
    penaltis = load_penaltis(catalog, filesize)
    
    return resultados, goles, penaltis


def load_partidos(catalog, filesize="large"):
    """
    Carga los datos del reto
    """
    resultsfile = cf.data_dir + 'football/results-utf8-' + filesize + '.csv'
    input_file = csv.DictReader(open(resultsfile, encoding ="utf-8"))
    for partido in input_file:
        model.add_partido(catalog, partido)
        
    return model.partidostotales(catalog)
    
def load_goles(catalog, filesize="large"):
    resultsfile = cf.data_dir + 'football/goalscorers-utf8-' + filesize + '.csv'
    input_file = csv.DictReader(open(resultsfile, encoding ="utf-8"))
    for gol in input_file:
        model.add_goalscorers(catalog,gol)
        model.add_gol(catalog,gol)
        
    return model.golestotales(catalog) 

  
def load_penaltis(catalog, filesize="large"):
    resultsfile = cf.data_dir + 'football/shootouts-utf8-' + filesize + '.csv'
    input_file = csv.DictReader(open(resultsfile, encoding ="utf-8"))
    for penalti in input_file:
        model.add_shootouts(catalog, penalti )
        model.add_penalti(catalog,penalti)
    return model.penaltistotales(catalog)

def load_results(control):
    model.add_resultsT(control['model'])
    model.add_results_AH(control['model'])

def load_torneos(control):
    return model.add_torneos(control["model"])

def load_pais(control):
    return model.add_paises(control["model"])    
    
    
    
def load_torneosFTP(control):   
    return model.add_torneosFTP(control["model"])

# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass

def sortResults(control):
    
    return model.sortResults(control["model"])

def sortGoalScorers(control):
    
    return model.sortGoalScorers(control["model"])

def sortShootouts(control):
   
    return model.sortShootouts(control["model"])

# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control,pais,condicion):
    """
    Retorna el resultado del requerimiento 1
    """
    startTime = get_time()
    tracemalloc.start()
    startMemory = get_memory()
    partidos_ , total_teams, total_matches=model.req_1(control['model'],pais,condicion)
    stopTime = get_time()
    deltaTime = delta_time(startTime, stopTime)
    stopMemory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stopMemory, startMemory)
    return    partidos_ , total_teams, total_matches,  deltaTime, deltaMemory
    


def req_2(control,jugador):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    #iniciar tiempo
    startTime = get_time()
    tracemalloc.start()
    startMemory = get_memory()
    goles, total_scorers, total_penalties= model.req_2(control['model'],jugador)
    #finalizar tiempo
    stopTime = get_time()
    deltaTime = delta_time(startTime, stopTime)
    stopMemory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stopMemory, startMemory)
    return goles, total_scorers, total_penalties, deltaTime, deltaMemory
    


def req_3(control,pais,inicial,final):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    startTime = get_time()
    tracemalloc.start()
    startMemory = get_memory()
    filtro,tamañoC,contadorTotal,contadorAway, contadorHome= model.req_3(control['model'],pais,inicial,final)
    #finaliza tiempo
    stopTime = get_time()
    deltaTime = delta_time(startTime, stopTime)
    stopMemory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stopMemory, startMemory)
   
    return filtro,tamañoC,contadorTotal,contadorAway, contadorHome,deltaTime, deltaMemory


def req_4(control, nombre,fecha_inicial,fecha_final):
    """
    Retorna el resultado del requerimiento 4
    """
    startTime = get_time()
    tracemalloc.start()
    startMemory = get_memory()
    
    partidos_filtrados, total_torneos, total_partidos, paises, ciudades, penaltis= model.req_4(control["model"], nombre,fecha_inicial,fecha_final)
    stopTime = get_time()
    deltaTime = delta_time(startTime, stopTime)
    stopMemory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stopMemory, startMemory)
    return partidos_filtrados, total_torneos, total_partidos, paises, ciudades, penaltis,deltaTime, deltaMemory 


def req_5(control, nombre,fecha_inicial,fecha_final):
    """
    Retorna el resultado del requerimiento 5
    """
    startTime = get_time()
    tracemalloc.start()
    startMemory = get_memory()
    
    jug,size,s_penalties,s_autogoals=model.req_5(control["model"], nombre,fecha_inicial,fecha_final)
    
    stopTime = get_time()
    deltaTime = delta_time(startTime, stopTime)
    stopMemory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stopMemory, startMemory)
     
    return jug,size,s_penalties,s_autogoals,deltaTime, deltaMemory 

def req_6(control,torneo, fecha):
    startTime = get_time()
    tracemalloc.start()
    startMemory = get_memory()
    ordenados=model.req_6(control['model'], torneo, fecha)
    stopTime = get_time()
    deltaTime = delta_time(startTime, stopTime)
    stopMemory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stopMemory, startMemory)
     
    return ordenados,deltaTime, deltaMemory


def req_7(control,torneo, puntos):
    startTime = get_time()
    tracemalloc.start()
    startMemory = get_memory()
    puntos = int(puntos)
    if puntos < 0:
        print("Los puntos ingreados no tienen sentido\n")
    else:
        ordenados, torneos_con_info, total_players, total_matches, total_goals, total_penalties, total_own_goals,total_p_2points=model.req_7(control['model'],torneo, puntos)
        stopTime = get_time()
        deltaTime = delta_time(startTime, stopTime)
        stopMemory = get_memory()
        tracemalloc.stop()
        deltaMemory = delta_memory(stopMemory, startMemory)
     
        return  ordenados, torneos_con_info, total_players, total_matches, total_goals, total_penalties, total_own_goals,total_p_2points,deltaTime, deltaMemory

def req_8(control,pais, inicial,final):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    startTime = get_time()
    tracemalloc.start()
    startMemory = get_memory()
    equipos_t,tablaInicio,torneos,year,size_t,ultimo=model.req_8(control['model'],pais, inicial,final)
    stopTime = get_time()
    deltaTime = delta_time(startTime, stopTime)
    stopMemory = get_memory()
    tracemalloc.stop()
    deltaMemory = delta_memory(stopMemory, startMemory)
    return  equipos_t,tablaInicio,torneos,deltaTime, deltaMemory,year,size_t,ultimo

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
     
def load_fullresults(catalog):
     return model.conect_all_data(catalog)