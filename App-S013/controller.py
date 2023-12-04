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

csv.field_size_limit(2147483647)
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
def new_controller():
    """
    Crea una instancia del modelo
    """
    tipo_estructura = input("Ingrese el tipo de estructura (1 para CHAINING o 2 para PROBING): ")
    factor_carga = input("Ingrese el factor de carga (1, 2, 3, o 4 para CHAINING; 1, 2, 3, o 4 para PROBING): ")
    num_elementos = int(input("Ingrese la cantidad de elementos iniciales: "))

    control = {
        'model': None
    }

    control['model'] = model.new_data_structs(tipo_estructura, factor_carga, num_elementos)
    return control

def load_data(control):
    """
    Carga los datos del reto
    """
    data_structs = control['model'] 
    message = """        Ingrese 1 si quiere cargar una muestra pequeña de los datos.
        Ingrese 2 si quiere cargar el 5 porciento de los datos. 
        Ingrese 3 si quiere cargar el 10 porciento de los datos.
        Ingrese 4 si quiere cargar el 20 porciento de los datos 
        Ingrese 5 si quiere cargar el 30 porciento de los datos.
        Ingrese 6 si quiere cargar el 50 porciento de los datos 
        Ingrese 7 si quiere cargar el 80 porciento de los datos 
        Ingrese 8 si quiere cargar TODOS los datos. \n"""
    data_size = int(input(message))

    if data_size == 1:
        file = "small.csv"
    elif data_size == 2:
        file = "5pct.csv"
    elif data_size == 3:
        file = "10pct.csv"
    elif data_size == 4:
        file = "20pct.csv"
    elif data_size == 5:
        file = "30pct.csv"
    elif data_size == 6:
        file = "50pct.csv"
    elif data_size == 7:
        file = "80pct.csv"
    elif data_size == 8:
        file = "large.csv"

    matches = load_matches(data_structs, file)
    scores = load_scores(data_structs, file)
    penalties = load_penalties(data_structs, file)
    load_score_players(data_structs, file)
    load_years_tournament(data_structs, file)
    sublists = sort(control)
    return matches, scores, penalties , sublists

def load_matches(data_structs, file):

    input_file = csv.DictReader(open(cf.data_dir + f"results-utf8-{file}", encoding='utf-8'))
    for match in input_file:
        model.add_mresults(data_structs, match)
    return model.data_size(data_structs)

def load_scores(data_structs, file):

    input_file = csv.DictReader(open(cf.data_dir + f"goalscorers-utf8-{file}", encoding='utf-8'))
    for score in input_file:
        model.add_score(data_structs, score)
    return model.data_size(data_structs)

def load_penalties(data_structs, file):

    input_file = csv.DictReader(open(cf.data_dir + f"shootouts-utf8-{file}", encoding='utf-8'))
    print(cf.data_dir + f"shootouts-utf8-{file}")
    for penaltie in input_file:
        model.add_penaltie(data_structs, penaltie)
    return model.data_size(data_structs)

def load_score_players(data_structs, file):

    input_file = csv.DictReader(open(cf.data_dir + f"goalscorers-utf8-{file}", encoding='utf-8'))
    for score in input_file:
        model.add_score_player(data_structs, score)
    return model.data_size(data_structs)

def load_years_tournament(data_structs, file):
    input_file = csv.DictReader(open(cf.data_dir + f"results-utf8-{file}", encoding='utf-8'))
    for match in input_file:
        model.add_year_tournament(data_structs, match)

def sort(control):
    submatches = model.match_sort(control['model'])
    subscores = model.scores_sort(control['model'])
    penalties = model.penalties_sort(control['model'])
    return submatches, subscores, penalties

def req_1(control):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    data_structs = control['model']
    #n_matches= 15
    #t_name = 'Italy'
    #condition='Local'
    n_matches = int(input("Ingrese el número de partidos a buscar:"))
    t_name = input("Ingrese el nombre del equipo:")
    condition = input("Ingrese la condición a buscar (Local/Visitante/Indiferente):")

    start_time = get_time()
    num, elements, num_matches = model.req_1(data_structs, n_matches, t_name, condition)
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    print('Tiempo que tomó ejecutar el requerimiento:',delta)
    return num, elements, num_matches


def req_2(control,numero_goles,jugador):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    data_structure = control['model'] 
    start_time = get_time()
    rta = model.req_2(data_structure, numero_goles, jugador)
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    print('Tiempo que tomó ejecutar el requerimiento:',delta)
    return rta


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    data_structs = control

    t_name = input("Ingresa el nombre del equipo: ")
    start_d = input("Ingresa la fecha de inicio en formato YY-MM-DD, separada por '-': ")
    end_d = input("Ingresa la fecha final en formato YY-MM-DD, separada por '-': ")
    start_time = get_time()
    total_matches, matches_as_home, matches_as_away, matches_list = model.req_3(data_structs['model'], t_name, start_d, end_d)
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    print('Tiempo que tomó ejecutar el requerimiento:', delta)
    return total_matches, matches_as_home, matches_as_away, matches_list

    


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    data_structs = control
    """ t_name = 'Copa América'
    start_d = '1955-06-01'
    end_d = '2022-06-30' """
    t_name = input("Ingresa el nombre del torneo: ")
    start_d = input("Ingresa la fecha de inicio en formato YY-MM-DD, separada por '-': ")
    end_d = input("Ingresa la fecha final en formato YY-MM-DD, separada por '-': ")
    start_time = get_time()
    elements, n_matches, n_countries, n_cities = model.req_4(data_structs['model'], t_name, start_d, end_d)
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    print('Tiempo que tomó ejecutar el requerimiento:',delta)
    return elements, n_matches, n_countries, n_cities, t_name

def req_5(control,jugador,f_inicial,f_final):
    """
    Retorna el resultado del requerimiento 5
    """
    data_structure = control["model"]
    start_time = get_time()
    rta = model.req_5(data_structure,jugador,f_inicial,f_final)
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    print('Tiempo que tomó ejecutar el requerimiento:',delta)
    return rta

def req_6(control,n_equipos,torneo,anio):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    data_structs = control['model']

    start_time = get_time()
    rta = model.req_6(data_structs,n_equipos,torneo,anio)
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    print('Tiempo que tomó ejecutar el requerimiento:',delta)
    return rta


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    data_structs = control['model']
    """ n_players = 17
    start_d = '2002-03-25'
    end_d = '2021-11-23' """
    n_players = int(input("Ingrese el número de jugadores que quiere consultar:"))
    start_d=input('Ingrese la fecha inicial en el formato Y-M-D:')
    end_d= input('Ingrese la fecha final en el formato Y-M-D:')
    start_time = get_time()
    player_num, n_matches, n_tournaments, total_scores, total_penalties, total_own_goals, elements=model.req_7(data_structs, n_players, start_d, end_d)
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    print('Tiempo que tomó ejecutar el requerimiento:',delta)
    return player_num, n_matches, n_tournaments, total_scores, total_penalties, total_own_goals, elements

def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    """ team1 = 'Canada'
    team2 = 'Brazil'
    start_d ='1980-01-01'
    end_d = '2012-12-18' """
    team1 = input("Ingrese el nombre del primer equipo: ")
    team2 = input("Ingrese el nombre del segundo equipo: ")
    start_d=input('Ingrese la fecha inicial en el formato Y-M-D:')
    end_d= input('Ingrese la fecha final en el formato Y-M-D:')
    start_time = get_time()
    n_years1, n_matches1, home_matches1, away_matches1, oldest_date1, newest_match1, elements1, n_years2, n_matches2, home_matches2, away_matches2, oldest_date2, newest_match2, elements2, n_joint_matches, joint_wins1, joint_losses1, joint_wins2, joint_losses2, joint_draws, newest_joint_match, scores = model.req_8(control['model'],team1, team2, start_d, end_d)
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    print('Tiempo que tomó ejecutar el requerimiento:',delta)
    return n_years1, n_matches1, home_matches1, away_matches1, oldest_date1, newest_match1, elements1, n_years2, n_matches2, home_matches2, away_matches2, oldest_date2, newest_match2, elements2, n_joint_matches, joint_wins1, joint_losses1, joint_wins2, joint_losses2, joint_draws, newest_joint_match, scores, team1, team2


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
