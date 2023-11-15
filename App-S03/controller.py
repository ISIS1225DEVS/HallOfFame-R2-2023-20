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


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }
    control['model'] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control,filepartidos,filegoleadores,filepenales,memflag=True):
    """
    Carga los datos del reto
    """
    # toma el tiempo al inicio del proceso
    start_time = get_time()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = get_memory()
    
    
    data_structs = control['model']
    partidos = load_partidos(data_structs,filepartidos)
    goleadores = load_goleadores(data_structs,filegoleadores)
    penales = load_penales(data_structs,filepenales)
    scorer= load_scorer(data_structs,filegoleadores)
    Top_scorer=load_top(data_structs,filegoleadores,filepartidos)
    torneo=load_torneo(data_structs,filepartidos)
    team=load_team(data_structs,filepartidos)
    goleadores_team=load_goleador_team(data_structs,filegoleadores)
    penales_team=load_penal_team(data_structs,filepenales)
    year=load_year(data_structs,filepartidos)

    # toma el tiempo al final del proceso
    stop_time = get_time()
    # calculando la diferencia en tiempo
    delta_Time = delta_time(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_Memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return partidos, goleadores, penales,scorer,Top_scorer, delta_Time, delta_Memory, torneo, team, goleadores_team,penales_team, year

    else:
        # respuesta sin medir memoria
        return partidos, goleadores, penales,scorer,Top_scorer, delta_Time, torneo, team, goleadores_team,penales_team, year 


def load_partidos(data_structs,file):
    """
    Carga los partidos
    """
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for partido in input_file:
        model.add_partidos(data_structs, partido)
    
    return data_structs["partidos"]


def load_goleadores(data_structs,file):
    """
    Carga los Goleadores
    """
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for goleador in input_file:
        model.add_goleadores(data_structs, goleador)
    
    return data_structs["goleadores"]


def load_scorer(data_structs,file):
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for goleador in input_file:
        model.addbyscorer(data_structs["scorer"], goleador)
    
    return data_structs["scorer"]
    
    
def load_torneo(data_structs,file):
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for partido in input_file:
        model.addbytorneo(data_structs, partido)
    
    return data_structs["torneos"]

def load_penales(data_structs,file):
    """
    Carga los Penales
    """
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for penales in input_file:
        model.add_penales(data_structs, penales)
    
    return data_structs["penales"]


def load_top(data_structs,goleadores,results):
    input_file1 = csv.DictReader(open(goleadores, encoding='utf-8'))
    input_file2 = csv.DictReader(open(results, encoding='utf-8'))
    
    for goleador in input_file1:
        model.addBytopscorer(data_structs,goleador)
    
    for result in input_file2:
        model.top_scorer2(data_structs,result)
    model.ToPpro(data_structs)
    
    return data_structs['Top']
    

def load_team(data_structs,file):
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for partido in input_file:
        model.addbyteam(data_structs["team"], partido)
    
    return data_structs["team"]
    

def load_goleador_team (data_structs,file):
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for goleador in input_file:
        model.addbyteam(data_structs["Goleador Team"], goleador)

    return data_structs["Goleador Team"]

def load_penal_team (data_structs, file):
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for penal in input_file:
        model.addbyteam(data_structs["Penales Team"], penal)

    return data_structs["Penales Team"]

def load_year (data_structs,file):
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for partido in input_file:
        model.addbyYear(data_structs["Year"], partido)
    
    return data_structs["Year"]

# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


def sort_date(data_structs):
    sorted_list = model.sort_date(data_structs)
    return sorted_list


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(teams,NPartidos,equipo,condicion):
    """
    Retorna el resultado del requerimiento 1
    """
    return model.req_1(teams,NPartidos,equipo,condicion)



def req_2(goleadores,Ngoles,jugador):
    """
    Retorna el resultado del requerimiento 2
    """
    return model.req_2(goleadores,Ngoles,jugador)


def req_3(teams,goleadores_team,equipo,inicio,final):
    """
    Retorna el resultado del requerimiento 3
    """
    return model.req_3(teams,goleadores_team,equipo,inicio,final)



def req_4(torneos,penales_team,torneo,inicio,final):
    """
    Retorna el resultado del requerimiento 4
    """
    return model.req_4(torneos,penales_team,torneo,inicio,final)


def req_5(Top,jugador,fecha_ini,fecha_fin):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    return model.req_5(Top,jugador,fecha_ini,fecha_fin)

def req_6(torneos,years,goleadores_team,Nequipos,torneo,year):
    """
    Retorna el resultado del requerimiento 6
    """
    return model.req_6(torneos,years,goleadores_team,Nequipos,torneo,year)



def req_7(torneos,goleadores_team,torneo, NPuntos):
    """
    Retorna el resultado del requerimiento 7
    """
    return model.req_7(torneos,goleadores_team,torneo, NPuntos)



def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


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
