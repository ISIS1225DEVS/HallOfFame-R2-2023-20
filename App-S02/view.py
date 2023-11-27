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
import model
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
from datetime import datetime

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
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control

def print_menu():
    print("Bienvenido :D")
    print("1- Cargar datos")
    print("2- Equipos según su condición ")
    print("3- Goles de jugador")
    print("4- Partidos de un equipo en periodo de tiempo ")
    print("5- Partidos de torneo en periodo de tiempo ")
    print("6- Anotaciones de jugador en un periodo de tiempo ")
    print("7- Mejores equipos de un torneo en periodo de tiempo  ")
    print("8- Mejores anotadores en partidos oficiales en periodo de tiempo")
    print("9- Desempeño historico de selecciones en torneo oficial ")
    print("10- Ordenar los datos")
    print("0- Salir")

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False
    
def printLoadDataAnswer(answer):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    if isinstance(answer, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "||",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer:.3f}")

def print_files(partidos, filename, sample = 3):
    
    if filename == 'partidos': 
        size = lt.size(partidos)
        tabla =[]
        if size <= sample*2:
            for partido in lt.iterator(partidos):
                tabla.append([partido['date'] , partido['home_team'] , partido['away_team'] , 
                            partido['home_score'], partido['away_score'], partido['country'], 
                            partido['city'], partido['tournament']])
        else:
            
            i = 1
            while i <= sample:
                partido = lt.getElement(partidos, i)
                tabla.append([partido['date'] , partido['home_team'] , partido['away_team'] , 
                            partido['home_score'], partido['away_score'], partido['country'], 
                            partido['city'], partido['tournament']])
                i += 1
            i = size - sample + 1
            while i <= size:
                partido = lt.getElement(partidos, i)
                tabla.append([partido['date'] , partido['home_team'] , partido['away_team'] , 
                            partido['home_score'], partido['away_score'], partido['country'], 
                            partido['city'], partido['tournament']])
                i += 1
            if tabla:
                headers = ["date", "home_team", "away_team", "home_score", "away_score", "country", "city", "tournament"]
                print(tabulate(tabla, headers=headers, tablefmt="grid"))
                
    elif filename == 'goleadores': 
        tabla = []
        size = lt.size(partidos)
        
        if size <= sample*2:
            for goleador in lt.iterator(partidos):
                tabla.append([ goleador['date'] , goleador['home_team'] , goleador['away_team'], 
                    goleador['team'] , goleador['scorer'] , float(goleador['minute'] ),
                    goleador['own_goal'], goleador['penalty']])
        else:
            
            i = 1
            while i <= sample:
                goleador = lt.getElement(partidos, i)
                tabla.append([ goleador['date'] , goleador['home_team'] , goleador['away_team'], 
                    goleador['team'] , goleador['scorer'] , float(goleador['minute']) ,
                    goleador['own_goal'], goleador['penalty']])
                i += 1
            i = size - sample + 1
            while i <= size:
                goleador = lt.getElement(partidos, i)
                tabla.append([ goleador['date'], goleador['home_team'] , goleador['away_team'], 
                    goleador['team'] , goleador['scorer'] , float(goleador['minute']) ,
                    goleador['own_goal'], goleador['penalty']])
                i += 1
        if tabla:
            headers = ["date", "home_team", "away_team", "team", "scorer", "minute", "own_goal", "penalty"]
            print(tabulate(tabla, headers=headers, tablefmt="grid"))
            
    elif filename == 'penales': 
        tabla = []
        size = lt.size(partidos)
        if size <= sample*2:
            
            for penal in lt.iterator(partidos):
                tabla.append([ penal['date'] , penal['home_team'] , penal['away_team'] 
                    ,penal['winner']])

        else:
            
            i = 1
            while i <= sample:
                penal = lt.getElement(partidos, i)
                tabla.append([ penal['date'] , penal['home_team'] , penal['away_team'] 
                    ,penal['winner']])
                i += 1
            
            i = size - sample + 1
            while i <= size:
                penal = lt.getElement(partidos, i)
                tabla.append([ penal['date'], penal['home_team'] , penal['away_team'] 
                    ,penal['winner']])
                i += 1
            if tabla:
                headers = ["date", "home_team", "away_team", "winner"]
                print(tabulate(tabla, headers=headers, tablefmt="grid"))

        
    
def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(partidos_n, sample= 3):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    size = lt.size(partidos_n)
    tabla =[]
    if size <= sample * 2:
        print("Los", size, "son:")
        for partido in lt.iterator(partidos_n):
            tabla.append([partido['date'], partido['home_team'], partido['away_team'], 
                          partido['home_score'], partido['away_score'], partido['country'], 
                          partido['city'], partido['tournament']])
    else:
        print(f"Los {sample} primeros y últimos partidos ordenados son:")
        i = 1
        while i <= sample:
            partido = lt.getElement(partidos_n, i)
            tabla.append([partido['date'], partido['home_team'], partido['away_team'], 
                          partido['home_score'], partido['away_score'], partido['country'], 
                          partido['city'], partido['tournament']])
            i += 1

        i = size - sample + 1
        while i <= size:
            partido = lt.getElement(partidos_n, i)
            tabla.append([partido['date'], partido['home_team'], partido['away_team'], 
                          partido['home_score'], partido['away_score'], partido['country'], 
                          partido['city'], partido['tournament']])
            i += 1

    if tabla:
        headers = ["date", "home_team", "away_team", "home_score", "away_score", "country", "city", "tournament"]
        print(tabulate(tabla, headers=headers, tablefmt="grid"))



def print_req_2(goleadores_ordenados, sample=3): 
    """
    Imprime los goleadores ordenados con tabulate
    """
    tabla = []
    size = lt.size(goleadores_ordenados)
    
    if size <= sample*2:
        for goleador in lt.iterator(goleadores_ordenados):
            tabla.append([ goleador['date'] , goleador['home_team'] , goleador['away_team'], 
                 goleador['team'] , goleador['scorer'] , goleador['minute'] ,
                 goleador['own_goal'], goleador['penalty']])
    else:
        
        i = 1
        while i <= sample:
            goleador = lt.getElement(goleadores_ordenados, i)
            tabla.append([ goleador['date'] , goleador['home_team'] , goleador['away_team'], 
                 goleador['team'] , goleador['scorer'] , goleador['minute'] ,
                 goleador['own_goal'], goleador['penalty']])
            i += 1
        i = size - sample + 1
        while i <= size:
            goleador = lt.getElement(goleadores_ordenados, i)
            tabla.append([ goleador['date'] , goleador['home_team'] , goleador['away_team'], 
                 goleador['team'] , goleador['scorer'] , goleador['minute'] ,
                 goleador['own_goal'], goleador['penalty']])
            i += 1
    if tabla:
        headers = ["date", "home_team", "away_team", "team", "scorer", "minute", "own_goal", "penalty"]
        print(tabulate(tabla, headers=headers, tablefmt="grid"))


def print_req_3(partidos, sample = 3):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    size = lt.size(partidos)
    tabla = []
    
    if size <= sample * 2:
        print("Los", size, "son:")
        for partido in lt.iterator(partidos):
            tabla.append([partido['date'], partido['home_score'], partido['away_score'], partido['home_team'], 
                          partido['away_team'], partido['country'], partido['city'], 
                          partido['tournament'], partido['penalty'], partido['own_goal']])
    else:
        print(f"Los {sample} primeros y últimos partidos ordenados son:")
        i = 1
        while i <= sample:
            partido = lt.getElement(partidos, i)
            tabla.append([partido['date'], partido['home_score'], partido['away_score'], partido['home_team'], 
                          partido['away_team'], partido['country'], partido['city'], 
                          partido['tournament'], partido['penalty'], partido['own_goal']])
            i += 1

        i = size - sample + 1
        while i <= size:
            partido = lt.getElement(partidos, i)
            tabla.append([partido['date'], partido['home_score'], partido['away_score'], partido['home_team'], 
                          partido['away_team'], partido['country'], partido['city'], 
                          partido['tournament'], partido['penalty'], partido['own_goal']])
            i += 1

    if tabla:
        tabla.reverse()
        headers = ['date', 'home_score', 'away_score', 'home_team', 'away_team', 'country', 'city', 'tournament', 'penalty', 'own_goal']
        print(tabulate(tabla, headers=headers, tablefmt="grid"))


def print_req_4(partidos_torneo_frame, sample= 3):
    """
    Imprime el requerimiento 4 ordenado con tabulate
    """
    # TODO: Imprimir el resultado del requerimiento 4

    size = lt.size(partidos_torneo_frame)
    tabla = []

    if size <= sample * 2:
        print("Los", size, "son:")
        for partido in lt.iterator(partidos_torneo_frame):
            tabla.append([partido['date'], partido['tournament'], partido['country'], partido['city'], 
                          partido['home_team'], partido['away_team'], partido['home_score'], 
                          partido['away_score'], partido['winner']])
    else:
        print(f"Los {sample} primeros y últimos partidos ordenados son:")
        i = 1
        while i <= sample:
            partido = lt.getElement(partidos_torneo_frame, i)
            tabla.append([partido['date'],partido['tournament'], partido['country'], partido['city'], 
                          partido['home_team'], partido['away_team'], partido['home_score'], 
                          partido['away_score'], partido['winner']])
            i += 1

        i = size - sample + 1
        while i <= size:
            partido = lt.getElement(partidos_torneo_frame, i)
            tabla.append([partido['date'],partido['tournament'], partido['country'], partido['city'], 
                          partido['home_team'], partido['away_team'], partido['home_score'], 
                          partido['away_score'], partido['winner']])
            i += 1

    if tabla:
        headers = ['date', 'tournament', 'country', 'city', 'home_team', 'away_team', 'home_score', 'away_score', 'winner']
        print(tabulate(tabla, headers=headers, tablefmt="grid"))


def print_req_5(anotaciones, sample=3):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    size = lt.size(anotaciones)
    tabla = []
    

    if size <= sample * 2:
        print("Las", size, "anotaciones son:")
        for partido in lt.iterator(anotaciones):
            tabla.append([partido['date'], partido['minute'], partido['home_team'], partido['away_team'], partido['team'], 
                          partido['home_score'], partido['away_score'], partido['tournament'], 
                          partido['penalty'], partido['own_goal']])
    else:
        print(f"Las {sample} primeras y últimas anotaciones ordenados son:")
        i = 1
        while i <= sample:
            partido = lt.getElement(anotaciones, i)
            tabla.append([partido['date'], partido['minute'], partido['home_team'], partido['away_team'], partido['team'], 
                          partido['home_score'], partido['away_score'], partido['tournament'], 
                          partido['penalty'], partido['own_goal']])
            i += 1

        i = size - sample + 1
        while i <= size:
            partido = lt.getElement(anotaciones, i)
            tabla.append([partido['date'], partido['minute'], partido['home_team'], partido['away_team'], partido['team'], 
                          partido['home_score'], partido['away_score'], partido['tournament'], 
                          partido['penalty'], partido['own_goal']])
            i += 1

    if tabla:
        headers = ['date', 'minute', 'home_team', 'away_team', 'team', 'home_score', 'away_score', 'tournament', 'penalty', 'own_goal' ]
        print(tabulate(tabla, headers=headers, tablefmt="grid"))


def print_req_6(resultados, sample= 3):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    size = lt.size(resultados)
    tabla = []
    
    if size <= sample * 2:
        print("Los", size, "equipos son:")
        for t_partido in lt.iterator(resultados):
            goleador = me.getValue(mp.get(t_partido, 'mejor_jugador'))
            if goleador['partidos'] != 0:
                goleador['partidos'] = len(goleador['partidos'])
            inner = tabulate([goleador], headers="keys", tablefmt="grid")
            tabla.append([me.getValue(mp.get(t_partido, 'equipo')), me.getValue(mp.get(t_partido, 'total_puntos_obtenidos')),
                          me.getValue(mp.get(t_partido, 'diferencia_goles')),me.getValue(mp.get(t_partido, 'total_linea_penal')), 
                          me.getValue(mp.get(t_partido, 'total_partidos')), me.getValue(mp.get(t_partido, 'total_autogol')), 
                          me.getValue(mp.get(t_partido, 'total_victorias')), me.getValue(mp.get(t_partido, 'total_empates')),
                          me.getValue(mp.get(t_partido, 'total_derrotas')), me.getValue(mp.get(t_partido, 'total_goles')),
                          me.getValue(mp.get(t_partido, 'total_goles_recibidos')), inner])
    else:
        print(f"Las {sample} primeras y últimas anotaciones ordenados son:")
        i = 1
        
        while i <= sample:
                
            t_partido = lt.getElement(resultados, i)
            goleador = me.getValue(mp.get(t_partido, 'mejor_jugador'))
            if goleador['partidos'] != 0:
                goleador['partidos'] = len(goleador['partidos'])
            inner = tabulate([goleador], headers="keys", tablefmt="grid")       
            tabla.append([me.getValue(mp.get(t_partido, 'equipo')), me.getValue(mp.get(t_partido, 'total_puntos_obtenidos')),
                          me.getValue(mp.get(t_partido, 'diferencia_goles')),me.getValue(mp.get(t_partido, 'total_linea_penal')), 
                          me.getValue(mp.get(t_partido, 'total_partidos')), me.getValue(mp.get(t_partido, 'total_autogol')), 
                          me.getValue(mp.get(t_partido, 'total_victorias')), me.getValue(mp.get(t_partido, 'total_empates')),
                          me.getValue(mp.get(t_partido, 'total_derrotas')), me.getValue(mp.get(t_partido, 'total_goles')),
                          me.getValue(mp.get(t_partido, 'total_goles_recibidos')), inner])
            i += 1

        i = size - sample + 1
        while i <= size:
            
            t_partido = lt.getElement(resultados, i)
            goleador = me.getValue(mp.get(t_partido, 'mejor_jugador'))
            if goleador['partidos'] != 0:
                goleador['partidos'] = len(goleador['partidos'])
            inner = tabulate([goleador], headers="keys", tablefmt="grid")
            tabla.append([me.getValue(mp.get(t_partido, 'equipo')), me.getValue(mp.get(t_partido, 'total_puntos_obtenidos')),
                          me.getValue(mp.get(t_partido, 'diferencia_goles')),me.getValue(mp.get(t_partido, 'total_linea_penal')), 
                          me.getValue(mp.get(t_partido, 'total_partidos')), me.getValue(mp.get(t_partido, 'total_autogol')), 
                          me.getValue(mp.get(t_partido, 'total_victorias')), me.getValue(mp.get(t_partido, 'total_empates')),
                          me.getValue(mp.get(t_partido, 'total_derrotas')), me.getValue(mp.get(t_partido, 'total_goles')),
                          me.getValue(mp.get(t_partido, 'total_goles_recibidos')), inner])
            i += 1

    if tabla:
        headers = ['team', 'total_points', 'goal_difference', 'penalty_points', 'total_teams', 'own_goals_points', 'wins','draws', 'losses', 'goals_for', 'goals_against', 'top_scorer' ]
        print(tabulate(tabla, headers=headers, tablefmt="grid"))
        
    
    
    


def print_req_7(resultados, sample= 3):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    size = lt.size(resultados)
    tabla = []
    
    if size <= sample * 2:
        print("Los", size, "equipos son:")
        for t_partido in lt.iterator(resultados):
            last_partido = me.getValue(mp.get(t_partido, 'last_goal'))
            last_partido['date'] = last_partido['date']
            headers_mini = ['date', 'tournament', 'home_team', 'away_team', 'home_score', 'away_score', 'minute', 'penalty', 'own_goal']
            tabla_mini = [[last_partido['date'], last_partido['tournament'], last_partido['home_team'], last_partido['away_team'], last_partido['home_score'],
                          last_partido['away_score'], last_partido['minute'], last_partido['penalty'], last_partido['own_goal']]]
            
            inner = tabulate(tabla_mini, headers=headers_mini, tablefmt="grid")

            tabla.append([me.getValue(mp.get(t_partido, 'jugador')), me.getValue(mp.get(t_partido, 'total_points')),
                          me.getValue(mp.get(t_partido, 'total_goals')),me.getValue(mp.get(t_partido, 'penalty_goals')), 
                          me.getValue(mp.get(t_partido, 'own_goals')), me.getValue(mp.get(t_partido, 'avg_time')), 
                          me.getValue(mp.get(t_partido, 'scored_in_wins')), me.getValue(mp.get(t_partido, 'scored_in_loses')),
                          me.getValue(mp.get(t_partido, 'scored_in_draws')), inner ])
    else:
        print(f"Las {sample} primeras y últimas anotaciones ordenados son:")
        i = 1
        
        while i <= sample:
                
            t_partido = lt.getElement(resultados, i)
            last_partido = me.getValue(mp.get(t_partido, 'last_goal'))
            last_partido['date'] = last_partido['date']
            headers_mini = ['date', 'tournament', 'home_team', 'away_team', 'home_score', 'away_score', 'minute', 'penalty', 'own_goal']
            tabla_mini = [[last_partido['date'], last_partido['tournament'], last_partido['home_team'], last_partido['away_team'], last_partido['home_score'],
                          last_partido['away_score'], last_partido['minute'], last_partido['penalty'], last_partido['own_goal']]]
            inner = tabulate(tabla_mini, headers=headers_mini, tablefmt="grid", numalign="right")
            tabla.append([me.getValue(mp.get(t_partido, 'jugador')), me.getValue(mp.get(t_partido, 'total_points')),
                          me.getValue(mp.get(t_partido, 'total_goals')),me.getValue(mp.get(t_partido, 'penalty_goals')), 
                          me.getValue(mp.get(t_partido, 'own_goals')), me.getValue(mp.get(t_partido, 'avg_time')), 
                          me.getValue(mp.get(t_partido, 'scored_in_wins')), me.getValue(mp.get(t_partido, 'scored_in_loses')),
                          me.getValue(mp.get(t_partido, 'scored_in_draws')), inner])
            i += 1

        i = size - sample + 1
        while i <= size:
            
            t_partido = lt.getElement(resultados, i)
            last_partido = me.getValue(mp.get(t_partido, 'last_goal'))
            last_partido['date'] = last_partido['date']
            headers_mini = ['date', 'tournament', 'home_team', 'away_team', 'home_score', 'away_score', 'minute', 'penalty', 'own_goal']
            tabla_mini = [[last_partido['date'], last_partido['tournament'], last_partido['home_team'], last_partido['away_team'], last_partido['home_score'],
                          last_partido['away_score'], last_partido['minute'], last_partido['penalty'], last_partido['own_goal']]]
            inner = tabulate(tabla_mini, headers=headers_mini, tablefmt="grid", numalign="right")
            tabla.append([me.getValue(mp.get(t_partido, 'jugador')), me.getValue(mp.get(t_partido, 'total_points')),
                          me.getValue(mp.get(t_partido, 'total_goals')),me.getValue(mp.get(t_partido, 'penalty_goals')), 
                          me.getValue(mp.get(t_partido, 'own_goals')), me.getValue(mp.get(t_partido, 'avg_time')), 
                          me.getValue(mp.get(t_partido, 'scored_in_wins')), me.getValue(mp.get(t_partido, 'scored_in_loses')),
                          me.getValue(mp.get(t_partido, 'scored_in_draws')), inner])
            i += 1

    if tabla:
        headers = ['jugador', 'total_points', 'total_goals', 'penalty_goals', 'own_goals', 'avg_time','scored_in_wins', 'scored_in_loses', 'scored_in_draws', 'last_goal']
        print(tabulate(tabla, headers=headers, tablefmt="grid"))
        


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
catalog = None
map_type = 'PROBING'
loadFactor = 0.7

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
            
            filesize = input('Indique el tamaño de la muestra que desea analizar (small, ...pct, large): ')
            
            if filesize == 'small': 
                size = 727
            elif filesize == '10pct':
                size =  3467
            elif filesize == '20pct': 
                size = 6659
            elif filesize == '30pct':
                size = 17487
            elif filesize == '50pct':
                size=  26342
            elif filesize == '80pct':
                size = 37714
            else: 
                size = 45001
            
            change = input('¿Deseas cambiar el mecanismo de colisiones, factor de carga y el número de elementos? (True/False): ')
            change = castBoolean(change)
            
            if change: 
                mapType = input('Indique que manejo de colisiones prefiere utilizar para los mapas implementados (PROBING/CHAINING): ')
                loadFactor = float(input('Indique el factor de carga que quieres para los mapas implementados: '))
                size = int(input('Indique el número de elementos que desea agregar: '))
            if catalog == None: 
                catalog = controller.new_controller(size, map_type, loadFactor)
            
            
            mem = castBoolean(input('¿Quieres medir la memoria utilizada? (True/False): '))
            deltas, totales = controller.load_data(catalog, filesize, memflag=mem)
            
            print('\nLoading data... \n')
            print('-'*50)
            print('\nResultados de partidos contados: '+ str(totales[0]))
            print('Goles de jugadores contados: ' + str(totales[1]))
            print('Definición de tiros penales: ' + str(totales[2]) )
            printLoadDataAnswer(deltas)
            print('\n'+'-'*50 ,'\n')
            
            print('='*50)
            print('='*16, 'REGISTRO FIFA :D', '='*16)
            print('='*50, '\n')
            
            print('-'*9, 'Resultados de partidos contados:', '-'*9)
            print('Total de partido: ' + str(totales[0]) + '\n')
            
            partidos = controller.sortData(catalog, totales[0], 'partidos')
            print_files(partidos, 'partidos')
            
            print('\n', '-'*8, 'Resultados de los goles contados:', '-'*9)
            print('Total de goleadores: ' + str(totales[1]) + '\n')
            
            print_files(catalog['model']['individuales'][0], 'goleadores')
            
            print('\n','-'*9, 'Resultados de penales contados:', '-'*9)
            print('Total de penales: ' + str(totales[2]) + '\n')
            
            
            print_files(catalog['model']['individuales'][1], 'penales')
            

        elif int(inputs) == 2:
            equipo = input('Inserte el equipo del cual quiere los partidos:  ')
            condicion = int(input("Seleccione la condición de la cual quiere los partidos de este equipo: \n 1. Local \n 2. Visitante \n 3. Indiferente: "))
           
            if condicion == 1: 
                condicion = 'home'

            elif condicion == 2:
                condicion = 'away' 

            else: 
                condicion = 'ind'
            n = int(input('¿Cúantos partidos de '+ str(equipo) + ' siendo ' + str(condicion)+ ' quieres tomar? '))
            mem = castBoolean(input('¿Quieres medir la memoria utilizada? (True o False) '))
            

            deltas, lista_n, totales = controller.req_1(catalog,n, equipo, condicion, memflag=mem)

            equipos= totales[0]
            partidos = totales[1]
            home = totales[2]
            if partidos == 0: 
                print('No se encontro informacion de goles realizados por este jugador')
            else:
                print("\n" + "-" *20 + "PARÁMETROS"+ "-" *20 )
                print("\nEquipo: " + equipo)
                print("Condición: " + condicion)
                print("Número de partidos a revisar: " + str(n))

                print("\n" + "=" *20 + " LOS PARTIDOS RESULTANTES "+ "=" *20 )
                print("\nTotal de equipos encontrados:  " + str(equipos))
                print("Total de partidos en los que participo encontrados:  " + str(partidos))
                print("Total de partidos en los que jugó como home:  " + str(home))
                
                printLoadDataAnswer(deltas)
                if int(n) <= 6:   
                    print('\nLa estructura tiene 6 o menos resultados')
                
                print_req_1(lista_n)
            

        elif int(inputs) == 3:

            goleador = input('Escriba el nombre de un jugador: ')
            n = int(input('Seleccione cuántos goles desea obtener del jugador: '))
            mem = castBoolean(input('¿Quieres medir la memoria utilizada? (True o False) '))
            deltas, resultado, suma, total, penal  = controller.req_2(catalog, goleador, n, mem)
            
            print("\n" + "-" *20 + "PARÁMETROS"+ "-" *20 )
            print("Número de goles solicitados: " + str(n) )
            print("Nombre del jugador: " + '"' + goleador  + '"' )
            
            print("\n" + "=" *20 + " LOS PARTIDOS RESULTANTES "+ "=" *20 )
            print('El total de goleadores es: ' + str(suma))
            print('El total de anotaciones obtenidas por el jugador son: ' + str(total))
            print('El total de penalties del jugador son: ' + str(penal))
            
            printLoadDataAnswer(deltas)
            
        
            if n <= 6: 
                if   total < n:
                        print('Selecting ' + '"' + str(total)  + '"' + " records")
                else: 
                    print('Selecting ' + '"' + str(n)  + '"' + " records")
                print('\nStruct has less than or equal to 6 results')
            else: 
                if total < n:
                    print('Selecting ' + str(total) + " records")
                else:   
                    print('Selecting ' + '6' + " records")
                print('\nStruct has less than or equal to 6 results')
                
            print_req_2(resultado)  

        elif int(inputs) == 4:
            equipo =  input('¿Qué equipo te gustaria buscar?: ')
            fi = datetime.strptime(input('¿Qué fecha inicial quieres para la búsqueda?: '),'%Y-%m-%d').strftime('%Y-%m-%d')
            ff = datetime.strptime(input('¿Qué fecha final quieres para la búsqueda?:  '),'%Y-%m-%d').strftime('%Y-%m-%d') 
            mem = castBoolean(input('¿Quieres medir la memoria utilizada? (True o False) '))
            
            delta, final, numero_par, home, away, numero_equipos = controller.req_3(catalog, equipo, fi, ff , memflag=mem)
            
            print("============Req No. 3 Inputs============")
            print( "Team Name: "+ str(equipo))
            print("Start date: "+ str(fi))
            print("Start date: "+ str(ff))
            print("\n============Req No. 3 Results============")
            print("Total team with available information: "+str(numero_equipos))
            print("Total games for "+ str(equipo)+": "+str(numero_par))
            print("Total home games for "+str(equipo)+": "+str(home))
            print("Total away games for "+str(equipo)+": "+str(away))
            
            print_req_3(final)

        elif int(inputs) == 5:
            
            torneo =  input('¿Qué torneo te gustaria buscar?: ')
            fecha_i = datetime.strptime(input('¿Qué fecha inicial quieres para la búsqueda?: '),'%Y-%m-%d').strftime('%Y-%m-%d')
            fecha_f = datetime.strptime(input('¿Qué fecha final quieres para la búsqueda?:  '),'%Y-%m-%d').strftime('%Y-%m-%d') 
            mem = castBoolean(input('¿Quieres medir la memoria utilizada? (True o False) '))
            
            delta, lista_n, totals= controller.req_4(catalog, torneo, fecha_i, fecha_f , memflag=mem)
            
            torneos = mp.get(totals, 'total_torneos')
            total_torneos = me.getValue(torneos)
            matches = mp.get(totals, 'total_matches')
            total_matches = me.getValue(matches)
            own_goals = mp.get(totals, 'total_own_goals')
            total_own_goals = me.getValue(own_goals)
            country = mp.get(totals, 'total_country')
            total_country = me.getValue(country)
            cities = mp.get(totals, 'total_cities')
            total_cities = me.getValue(cities)
            winners = mp.get(totals, 'total_winners')
            total_winners = me.getValue(winners)
            teams = mp.get(totals, 'total_teams')
            total_teams = me.getValue(teams)

            print("\n" + "-" *20 + "PARÁMETROS"+ "-" *20 )
            print("\nTorneo: " + str(torneo))
            print("Fecha inicial: " + str(fecha_i))
            print("Fecha final " + str(fecha_f))
            
            print("\n" + "=" *20 + " LOS PARTIDOS RESULTANTES "+ "=" *20 )
            print("\nTotal de partidos con información disponible: " + str(total_torneos))
            print("Los partidos totales de " + str(torneo) + " son: " + str(total_matches))
            print("Los paises totales encontrados de "+ str(torneo) + "  son: " + str(lt.size(total_country)))
            print("Las ciudades totales encontrados de "+ str(torneo) + "  son: " + str(lt.size(total_cities)))
            print("La cantidad de penales de " + str(torneo)+ " son: " + str(total_own_goals))
            printLoadDataAnswer(delta)

            print_req_4(lista_n)


        elif int(inputs) == 6:

            goleador = input('Escriba el nombre de un jugador: ')
            fecha_i = datetime.strptime(input('¿Qué fecha inicial quieres para la búsqueda?: '),'%Y-%m-%d').strftime('%Y-%m-%d')
            fecha_f = datetime.strptime(input('¿Qué fecha final quieres para la búsqueda?:  '),'%Y-%m-%d').strftime('%Y-%m-%d')
            mem = castBoolean(input('¿Quieres medir la memoria utilizada? (True o False) '))
            deltas, resultado, suma, total, tot_torneos, penalty, auto = controller.req_5(catalog, goleador, fecha_i, fecha_f, mem)
                    
            if total == 0:
                print('No se encontro informacion de goles realizados por este jugador')
            else:
                print("\n" + "-" *20 + "PARÁMETROS"+ "-" *20 )
                print("Nombre del jugador: " + '"' + goleador  + '"' )
                print("Fecha inicial: " + '"' + str(fecha_i)  + '"' )
                print("Fecha final: " + '"' + str(fecha_f)  + '"' )
                
                print("\n" + "=" *20 + " LOS PARTIDOS RESULTANTES "+ "=" *20 )
                
                print(" jugadores totales: " + '"' + str(suma)  + '"')
                print(goleador + " Goles totales: " + '"' + str(total)  + '"')
                print(goleador + " Torneos totales: " + '"' + str(tot_torneos)  + '"')
                print(goleador + " Penalties totales: " + '"' + str(penalty)  + '"')
                print(goleador + " Autogoles totales: " + '"' + str(auto)  + '"')
                printLoadDataAnswer(deltas)
                
                if total<= 6:
                    print('Goal scorers struct has less than or equal to 6 results')
                
                print_req_5(resultado)


        elif int(inputs) == 7:
            torneo = input('¿Qué torneo te gustaria buscar?: ')
            n = int(input('Escribe el número de top a buscar: '))
            fecha_i = datetime.strptime(input('¿Qué fecha inicial quieres para la búsqueda?: '),'%Y-%m-%d')
            fecha_f = datetime.strptime(input('¿Qué fecha final quieres para la búsqueda?:  '),'%Y-%m-%d')
            mem = castBoolean(input('¿Quieres medir la memoria utilizada? (True o False) '))
            
            year = fecha_i.year
            deltas, (totales_de_equipos, totales_generales) = controller.req_6(catalog, n, torneo, year, memflag=mem)
            
            print("\n" + "-" *20 + "PARÁMETROS"+ "-" *20 )
            print("Nombre del torneo: " + '"' + torneo  + '"' )
            print("Número de TOP equipos a buscar es: " + (str(n)))
            print("Fecha Inicial: " + '"' + str(year)  + '"' )
            
            print("\n" + "=" *20 + " LOS PARTIDOS RESULTANTES "+ "=" *20 )
            print(torneo + "Total de años dentro del historial : " + '"' + str(totales_generales[0])  + '"')
            print(torneo + "Total de torneos : " + ' " ' + str(totales_generales[1])  + ' "')
            print(torneo + "Total de equipos : " + ' " ' + str(totales_generales[2])  + ' "')
            print(torneo + "Total de encuentros : " + ' " ' + str(totales_generales[3])  + ' "')
            print(torneo + "Total de paises : " + ' " ' + str(totales_generales[4])  + '"')
            print(torneo + "Total de ciudades : " + ' " ' + str(totales_generales[5])  + ' "')
            print(torneo + "Ciudad con más partidos: " + ' " ' + str(totales_generales[6])  + ' "')
            printLoadDataAnswer(deltas)
            
            print_req_6(totales_de_equipos)

        elif int(inputs) == 8:
            torneo = input('¿Qué torneo te gustaria buscar?: ')
            n = int(input('Escribe el número de puntos a buscar: '))
            mem = castBoolean(input('¿Quieres medir la memoria utilizada? (True o False) '))
            
            deltas, lista_jugadores, totales_generales = controller.req_7(catalog, torneo,n, memflag=mem)
            
            print("\n" + "-" *20 + "PARÁMETROS"+ "-" *20 )
            print("Nombre del torneo: " + '"' + torneo  + '"' )
            print("Número de de puntos a buscar es: " + (str(n)))
            
            print("\n" + "=" *20 + " LOS PARTIDOS RESULTANTES "+ "=" *20 )
            print(torneo + "Total de torneos disponibles para consultar : " + '"' + str(totales_generales[0])  + '"')
            print(torneo + "Total de anotadores que participaron en el torneo : " + ' " ' + str(totales_generales[1])  + ' "')
            print(torneo + "Total de partidos dentro del torneo : " + ' " ' + str(totales_generales[2])  + ' "')
            print(torneo + "Total de anotaciones obtenidos durante los partidos del torneo : " + ' " ' + str(totales_generales[3])  + ' "')
            print(torneo + "Total de goles por penal obtenidos en ese torneo : " + ' " ' + str(totales_generales[4])  + '"')
            print(torneo + "Total de autogoles de los anotadores en ese torneo : " + ' " ' + str(totales_generales[5])  + ' "')
            printLoadDataAnswer(deltas)
            
            
            print_req_7(lista_jugadores)

        elif int(inputs) == 9:
            años_en_el_período = [año for año in range(fecha_i.year, fecha_f.year + 1)]
            print_req_8(catalog)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        elif int(inputs) == 11: 

            deltas, resp, tot =controller.req_7(catalog, 'UEFA Euro qualification' , 2, False )
            print_req_7(resp)
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
    