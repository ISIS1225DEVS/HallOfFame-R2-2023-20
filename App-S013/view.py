"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

default_limit = 1000
sys.setrecursionlimit(default_limit*10)
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
    Se crea una instancia del controlador
    """
    control = controller.new_controller()
    return control

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    results = controller.load_data(control)
    return results

def print_data(control):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    print("Cargando información de los archivos ....\n")
    data = control

    print(f'{"-"*10}\n'
            f'Numero de partidos: {data[0][0]}\n'
            f'Numero de goles marcados: {data[1][1]}\n'
            f'Numero de penalties: {data[2][2]}\n'
        f'{"-"*10}\n')
    print(f'Resultados de partidos cargados: {data[0][0]}')

    dic_partidos = {"Fecha":[],
                "Local":[],
                "Visitante":[],
                "Marcador final":[],
                "Liga":[],
                "Locación":[]}
    for partidos in lt.iterator(data[3][0]):
        dic_partidos["Fecha"].append(partidos["date"])
        dic_partidos["Local"].append(partidos["home_team"])
        dic_partidos["Visitante"].append(partidos["away_team"])
        dic_partidos["Marcador final"].append(partidos["home_score"]+"-"+partidos["away_score"])
        dic_partidos["Liga"].append(partidos["tournament"])
        dic_partidos["Locación"].append(partidos["city"]+", "+partidos["country"])
    print(f'Primeros y últimos tres partidos:\n {tabulate(dic_partidos, headers="keys",tablefmt="grid")}')

    dict_scorers = {"Fecha":[],
                    "Local":[],
                    "Visitante":[],
                    "Nombre del jugador que marco":[],
                    "Equipo":[],
                    "Minuto":[],
                    "Penal":[],
                    "Autogol":[]
    }

    for goles in lt.iterator(data[3][1]):
        dict_scorers["Fecha"].append(goles["date"])
        dict_scorers["Local"].append(goles["home_team"])
        dict_scorers["Visitante"].append(goles["away_team"])
        dict_scorers["Nombre del jugador que marco"].append(goles["scorer"])
        dict_scorers["Equipo"].append(goles["team"])
        dict_scorers["Minuto"].append(goles["minute"])
        dict_scorers["Penal"].append(goles["penalty"])
        dict_scorers["Autogol"].append(goles["own_goal"])
    print(f'Primeros y últimos tres goles: \n {tabulate(dict_scorers,headers="keys",tablefmt="grid")}')

    dict_penalties = {"Fecha":[],
                    "Local":[],
                    "Visitante":[],
                    "Ganador":[]}
    
    for penalties in lt.iterator(data[3][2]):
        dict_penalties["Fecha"].append(penalties["date"])
        dict_penalties["Local"].append(penalties["home_team"])
        dict_penalties["Visitante"].append(penalties["away_team"])
        dict_penalties["Ganador"].append(penalties["winner"])
    print(f'Primeros y últimos tres penalties:\n{tabulate(dict_penalties,headers="keys", tablefmt="grid")}')

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    num, elements, num_matches = controller.req_1(control)
    print(f'{"-"*5}Partidos encontrados: {num}{"-"*50}')
    print(f'{"-"*5}Seleccionando {num_matches} partidos...{"-"*50}')
    print(f'{tabulate(elements, headers="keys",tablefmt="grid")}')


def  print_req_2(control,numero_goles,jugador):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    if numero_goles == "": 
        numero_goles = 7
    if jugador == "":
        jugador = "Michael Ballack"

    
    rta = controller.req_2(control,int(numero_goles),jugador)
    print("""======================================== Resultados REQ 2 ======================================== \n""")
    print(f"Total de jugadores con goles: {rta[3]}")
    print(f"Total de goles de '{jugador}': {rta[1]}")
    print(f"Total de penalties de '{jugador}': {rta[2]}")
    dict_aux =  {"Fecha":[],
                "Local":[],
                "Visitante":[],
                "Equipo":[],
                "Minuto":[],
                "Penal":[],
                "Autogol":[]
    }
    for gol in lt.iterator(rta[0]):
        dict_aux["Fecha"].append(gol["date"])
        dict_aux["Local"].append(gol["home_team"])
        dict_aux["Visitante"].append(gol["away_team"])
        dict_aux["Equipo"].append(gol["team"])
        dict_aux["Minuto"].append(gol["minute"])
        dict_aux["Penal"].append(gol["penalty"])
        dict_aux["Autogol"].append(gol["own_goal"])

    print(tabulate(dict_aux,headers="keys",tablefmt="grid"))

def print_req_3(control):
    """
    Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    matches_list, total_matches, matches_as_home, matches_as_away = controller.req_3(control)
    print(f'{"-"*5} juegos totales: {total_matches}{"-"*50}')
    print(f'{"-"*5}Juegos como local: {matches_as_home}{"-"*50}')
    print(f'{"-"*5}Juegos como visitante: {matches_as_away}{"-"*50}')
    print(f'{tabulate(lt.iterator(matches_list), headers="keys",tablefmt="grid")}')


def print_req_4(control,data_structs, t_name, start_d, end_d):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """

    rta = controller.req_4(control,data_structs,t_name,start_d,end_d)
    print(rta)
    goles = rta[0]
    torneos = rta[6]
    
    elements, n_matches, n_countries, n_cities, t_name = controller.req_4(control)
    print(f'{"-"*5}{t_name} partidos totales: {n_matches}{"-"*50}')
    print(f'{"-"*5}{t_name} países totales: {n_countries}{"-"*50}')
    print(f'{"-"*5}{t_name} ciudades totales: {n_cities}{"-"*50}')
    print(f'{tabulate(elements, headers="keys",tablefmt="grid")}')

    dict_aux =  {"Fecha":[],
                "Pais":[],
                "Ciudad":[],
                "Local":[],
                "Visitante":[],
                "Equipo":[],
                "Goles Visitante":[],
                "Goles Local":[],
                "Penalty":[],
                "Equipo Ganador":[]
    }

    for gol in lt.iterator(goles):
        dict_aux["Fecha"].append(gol["date"])
        dict_aux["Pais"].append(gol["home_team"])
        dict_aux["Ciudad"].append(gol["city"])
        dict_aux["Local"].append(gol["home_team"])
        dict_aux["Visitante"].append(gol["away_team"])
        dict_aux["Equipo"].append(gol["team"])
        dict_aux["Penalty"].append(gol["penalty"])
        dict_aux["Equipo Ganador"].append(gol["winner"])

    for torneo in lt.iterator(torneos):
        dict_aux["Torneo"].append(torneo["tournament"])
        dict_aux["Goles local"].append(torneo["home_score"])
        dict_aux["Goles Visitante"].append(torneo["away_score"])

    print(tabulate(dict_aux,headers="keys",tablefmt="grid"))


def print_req_5(control,jugador,f_inicial,f_final):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    if jugador == "":
        jugador = "Ali Daei"
    if f_inicial == "":
        f_inicial = "1999-03-25"
    if f_final == "":
        f_final = "2021-11-23"
    rta = controller.req_5(control,jugador,f_inicial,f_final)

    goles = rta[0]
    total_goles = rta[1]
    total_torneos = rta[2]
    jugadores_con_goles = rta[3]
    penalties = rta[4]
    autogoles = rta[5]
    torneos = rta[6]
    
    print("""======================================== Resultados REQ 5 ======================================== \n""")
    print(f"Total de jugadores con goles: {jugadores_con_goles}")
    print(f"Total de goles de '{jugador}': {total_goles}")
    print(f"Total de penalties de torneos de '{jugador}': {total_torneos}")
    print(f"Total de penalties de penalties de '{jugador}': {penalties}")
    print(f"Total de penalties de autogoles de '{jugador}': {autogoles}")

    dict_aux =  {"Fecha":[],
                "Minuto":[],
                "Local":[],
                "Visitante":[],
                "Equipo":[],
                "Goles local":[],
                "Goles Visitante":[],
                "Torneo":[],
                "Penalty":[],
                "Autogol":[]
    }

    for gol in lt.iterator(goles):
        dict_aux["Fecha"].append(gol["date"])
        dict_aux["Minuto"].append(gol["minute"])
        dict_aux["Local"].append(gol["home_team"])
        dict_aux["Visitante"].append(gol["away_team"])
        dict_aux["Equipo"].append(gol["team"])
        dict_aux["Penalty"].append(gol["penalty"])
        dict_aux["Autogol"].append(gol["own_goal"])

    for torneo in lt.iterator(torneos):
        dict_aux["Torneo"].append(torneo["tournament"])
        dict_aux["Goles local"].append(torneo["home_score"])
        dict_aux["Goles Visitante"].append(torneo["away_score"])

    print(tabulate(dict_aux,headers="keys",tablefmt="grid"))



def print_req_6(control,n_equipos,torneo,anio):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    if n_equipos == "":
        n_equipos = 11
    if torneo == "":
        torneo = "FIFA World Cup qualification"
    if anio == "":
        anio = 2021

    rta = controller.req_6(control,int(n_equipos),torneo,str(anio))
    print(rta)
    print("""======================================== Resultados REQ 6 ======================================== \n""")
    print(f"Total de años disponibles :{rta[0]}")
    print(f"Total de torneos disputados en el año:{rta[1]}")
    print(f"Total de equipos que participaron en el torneo:{rta[2]}")
    print(f"Total de partidos disputados en el torneo:{rta[3]}")
    print(f"Total de paises que participaron en el torneo:{rta[4]}")
    print(f"Total de ciudades que participaron en el torneo:{rta[5]}")
    print(f"Ciudad que mas se frecuentó :{rta[6]}")

    dict_aux =  {"Equipo":[],
                "Puntos":[],
                "Diferencia de gol":[],
                "Penalties":[],
                "Partidos":[],
                "Autogoles":[],
                "Victorias":[],
                "Derrotas":[],
                "Empates":[],
                "Goles a favor":[],
                "Goles en contra":[],
                "Goleador":[],}
    
    for equipo in lt.iterator(rta[7]):
        dict_aux["Equipo"].append(equipo["equipo"])
        dict_aux["Puntos"].append(equipo["puntos"])
        dict_aux["Diferencia de gol"].append(equipo["goles_favor"]-equipo["goles_contra"])
        dict_aux["Penalties"].append(equipo["penalties"])
        dict_aux["Partidos"].append(equipo["partidos"])
        dict_aux["Autogoles"].append(equipo["autogoles"])
        dict_aux["Victorias"].append(equipo["victorias"])
        dict_aux["Derrotas"].append(equipo["derrotas"])
        dict_aux["Empates"].append(equipo["empates"])
        dict_aux["Goles a favor"].append(equipo["goles_favor"])
        dict_aux["Goles en contra"].append(equipo["goles_contra"])
        dict_aux["Goleador"].append(tabulate([equipo["jugador_mas_goles"]],headers="keys",tablefmt="grid"))

    print(tabulate(dict_aux,headers="keys",tablefmt="grid"))



def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    player_num, n_matches, n_tournaments, total_scores, total_penalties, total_own_goals, elements = controller.req_7(control)
    print(f'{"-"*5}Número de torneos oficiales: {n_tournaments}{"-"*50}')
    print(f'{"-"*5}Número de jugadores en torneos oficiales: {player_num}{"-"*50}')
    print(f'{"-"*5}Partidos totales en torneos oficiales: {n_matches}{"-"*50}')
    print(f'{"-"*5}Goles totales en torneos oficiales: {total_scores}{"-"*50}')
    print(f'{"-"*5}Penales totales en torneos oficiales: {total_penalties}{"-"*50}')
    print(f'{"-"*5}Autogoles en torneos oficiales: {total_own_goals}{"-"*50}')
    for element in elements:
        element['last_goal']=tabulate([element['last_goal']], headers="keys", tablefmt="grid")
    print(f'{tabulate(elements, headers="keys", tablefmt="grid")}')

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    n_years1, n_matches1, home_matches1, away_matches1, oldest_date1, newest_match1, elements1, n_years2, n_matches2, home_matches2, away_matches2, oldest_date2, newest_match2, elements2, n_joint_matches, joint_wins1, joint_losses1, joint_wins2, joint_losses2, joint_draws, newest_joint_match, scores, team1, team2 =controller.req_8(control)
    for element in elements1:
        if type(element['top_scorer'])==dict:
            element['top_scorer']=tabulate([element['top_scorer']], headers="keys", tablefmt="grid")
    for element in elements2:
        if type(element['top_scorer'])==dict:
            element['top_scorer']=tabulate([element['top_scorer']], headers="keys", tablefmt="grid")
    print(f'{"-"*5}{team1} Statistics{"-"*50}')
    print(f'{"-"*5}Years: {n_years1}{"-"*50}')
    print(f'{"-"*5}Total matches: {n_matches1}{"-"*50}')
    print(f'{"-"*5}Total home matches: {home_matches1}{"-"*50}')
    print(f'{"-"*5}Total away matches: {away_matches1}{"-"*50}')
    print(f'{"-"*5}Oldest match date: {oldest_date1}{"-"*50}')
    print(f'{"-"*5} Newest match data {"-"*50}')
    print(f'{tabulate([newest_match1], headers="keys", tablefmt="grid")}')
    print(f'{"-"*5} Yearly statistics {"-"*50}')
    print(f'{tabulate(elements1, headers="keys", tablefmt="grid")}')

    print(f'{"-"*5}{team2} Statistics{"-"*50}')
    print(f'{"-"*5}Years: {n_years2}{"-"*50}')
    print(f'{"-"*5}Total matches: {n_matches2}{"-"*50}')
    print(f'{"-"*5}Total home matches: {home_matches2}{"-"*50}')
    print(f'{"-"*5}Total away matches: {away_matches2}{"-"*50}')
    print(f'{"-"*5}Oldest match date: {oldest_date2}{"-"*50}')
    print(f'{"-"*5} Newest match data {"-"*50}')
    print(f'{tabulate([newest_match2], headers="keys", tablefmt="grid")}')
    print(f'{"-"*5} Yearly statistics {"-"*50}')
    print(f'{tabulate(elements2, headers="keys", tablefmt="grid")}')

    print(f'{"-"*5}{team1} vs {team2} Statistics{"-"*50}')
    print(f'{"-"*5}Total matches: {n_joint_matches}{"-"*50}')
    print(f'{"-"*5}Total wins for {team1}: {joint_wins1}{"-"*50}')
    print(f'{"-"*5}Total losses for {team1}: {joint_losses1}{"-"*50}')
    print(f'{"-"*5}Total wins for {team2}: {joint_wins2}{"-"*50}')
    print(f'{"-"*5}Total losses for {team2}: {joint_losses2}{"-"*50}')
    print(f'{"-"*5}Total draws: {joint_draws}{"-"*50}')
    print(f'{"-"*5} Newest match data {"-"*50}')
    print(f'{tabulate([newest_joint_match], headers="keys", tablefmt="grid")}')
    print(f'{"-"*5} Match scores {"-"*50}')
    print(f'{tabulate(scores, headers="keys", tablefmt="grid")}')


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
            print_data(data)

        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            numero_goles = input("Ingrese el número de goles que desea consultar: ")
            jugador = input("Ingrese el nombre del jugador que desea consultar: ")
            print_req_2(control,numero_goles,jugador)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            jugador = input("Ingrese el nombre del jugador que desea consultar: ")
            f_inicial = input("Ingrese la fecha inicial en formato YYYY-MM-DD: ")
            f_final = input("Ingrese la fecha final en formato YYYY-MM-DD: ")
            print_req_5(control,jugador,f_inicial,f_final)

        elif int(inputs) == 7:
            n_equipos = input("Ingrese el numero de equipos que desea clasificar: ")
            torneo = input("Ingrese el nombre del torneo que desea consultar: ")
            anio = input("Ingrese el año que desea buscar: ")
            print_req_6(control,n_equipos,torneo,anio)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
