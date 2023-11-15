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

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller(listType):
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller(listType)
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Listar los últimos N partidos de un equipo según su condicion")
    print("3- Listar los primeros N goles anotados por un jugador")
    print("4- Consultar los partidos que disputó un equipo durante un periodo especifico")
    print("5- Consultar los partidos relacionados con un torneo durante un periodo especifico")
    print("6- Consultar las anotaciones de un jugador durante un periodo especifico")
    print("7- Clasificar los N mejores equipos del año dentro de un torneo especifico")
    print("8- Encontrar los anotadores con N puntos dentro de un torneo especifico")
    print("9- Consultar el desempeño histórico de una selección en torneos oficiales")
    print("0- Salir")


def load_data(control, filesize):
    """
    Carga los datos
    """
    results, Goalscorers, shootouts,  = controller.load_data(control, filesize)
    return results, Goalscorers, shootouts



def print_req_2(control,jugador):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    filtro,tamaño= controller.req_2(control,jugador)
    return filtro,tamaño



def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

#Funcion encarga de tabular listas con mas de 6 elementos
def print_tabulate_6(lista, columnas):
    lista = lista["elements"][:3] + lista["elements"][-3:]
    reduced = []
    for result in lista:
        linea = []
        for c in columnas:
            linea.append(result[c])
        reduced.append(linea)  
    tabla = print(tabulate(reduced, headers=columnas, tablefmt="grid"))
    return tabla

#Funcion encarga de tabular listas con menos de 6 elementos
def print_tabulate(lista, columnas):
    reduced = []
    for result in lista["elements"]:
        linea = []
        for c in columnas:
            linea.append(result[c])
        reduced.append(linea)  
    tabla = print(tabulate(reduced, headers=columnas, tablefmt="grid"))
    return tabla
        
def print_tabulate2(lista, columnas):
    reduced = []
    for result in lista:
        linea = []
        for c in columnas:
            linea.append(result[c])
        reduced.append(linea)  
    tabla = print(tabulate(reduced, headers=columnas, tablefmt="grid"))
    return tabla
# Se crea el controlador asociado a la vista
listType = "ARRAY_LIST"
control=new_controller(listType)

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
            size = "small"
            results, goalscorers, shootouts = load_data(control, size)
            sorted_results = controller.sortResults(control)
            sorted_goalscorers = controller.sortGoalScorers(control)
            sorted_shootouts = controller.sortShootouts(control)
            controller.load_results(control)
            controller.load_torneos(control)
            controller.load_pais(control)
            controller.load_fullresults(control["model"])
            controller.load_torneosFTP(control)
            print("\nCargando información de los archivos ....")
            print("--------------------------------------")
            print("Recuento de partidos: " + str(results))
            print("Recuento de goles: " + str(goalscorers))
            print("Recuento de penaltis: " + str(shootouts))
            print("--------------------------------------\n")
            print("===================================================")
            print("=============== FIFA RECORDS REPORT ===============")
            print("===================================================\n")
            print("Mostrando los resultados por los primeros y ultimos 3 registros en el archivo.\n")
            print('---- MATCH RESULTS ----')
            print('Total de resultados cargados: ' + str(results))
            if lt.size(sorted_results) > 6:
                print("Los resultados tienen mas de 6 elementos...")
                print_tabulate_6(sorted_results, ["date","home_team","away_team","home_score","away_score","country","city","tournament"])
            else:
                print("Los resultados tienen menos de 6 elementos...")
                print_tabulate(sorted_results, ["date","home_team","away_team","home_score","away_score","country","city","tournament"])
            
            
            print('---- GOAL SCORERS ----')
            print('Goalscorers cargados: ' + str(goalscorers))
            if lt.size(sorted_goalscorers) > 6:
                print("Los resultados tienen mas de 6 elementos...")
                print_tabulate_6(sorted_goalscorers, ["date","home_team","away_team","scorer","team","minute","penalty","own_goal"])
            else:
                print("Los resultados tienen menos de 6 elementos...")
                print_tabulate(sorted_goalscorers, ["date","home_team","away_team","scorer","team","minute","penalty","own_goal"])
            
            
           
            print('---- SHOOTOUTS ----')
            print('Shoutouts cargados: ' + str(shootouts))
            if lt.size(sorted_shootouts) > 6:
                print("Los resultados tienen mas de 6 elementos...")
                print_tabulate_6(sorted_shootouts, ["date","home_team","away_team","winner"])
            else:
                print("Los resultados tienen menos de 6 elementos...")
                print_tabulate_6(sorted_shootouts, ["date","home_team","away_team","winner"])
    
        elif int(inputs) == 2:
            number = int(input("Numero de partidos que quieres conocer: "))
            pais = input("Ingrese el nombre del pais:  ")
            condicion= input("Ingrese la condicion del pais(local/visitante/indiferente): ")
            total_partidos_by_team, total_teams, total_matches,delta, memo = controller.req_1(control, pais, condicion)
            tiempo=f"{delta:.3f}"
            memoria= f"{memo:.3f}"
            print("\n" + 'Tiempo [ms]: ', tiempo, '||','Memoria [kB]: ', memoria,"\n") 
            filtro = total_partidos_by_team['partidos']
            size = lt.size(filtro)
            print("\n=============== Req No. 1 Inputs ===============")
            print("Numero de partidos: " + str(number))
            print("Nombre del equipo: " + str(pais))
            print("Condicion del equipo: " + str(condicion))
            if number > size :
                print("\n Solo " + str(size) + " partidos encontrados, seleccionado todos... \n")
                number = size
            filtro['elements'] = filtro['elements'][:number]
            
            print("=============== Req No. 1 Results ===============")
            print("Total de equipos con información disponible: " + str(total_teams))
            print("Total de partidos para " + pais + ": " + str(total_matches))
            print("Total de encuentro para " + str(pais) + " como " + condicion + ": " + str(size))
            print("\n")
            if size > 6:
                print("Los resultados tienen mas de 6 elementos...")
                print_tabulate_6(filtro, ["date","home_team", "away_team", "home_score", "away_score", "country", "city", "tournament"])
            else:
                print("Los resultados tienen menos de 6 elementos...")
                print_tabulate(filtro, ["date","home_team", "away_team", "home_score", "away_score", "country", "city", "tournament"])
            
  
            
            
        elif int(inputs) == 3:
            goles=input("Digite el numero de goles a consultar: ")
            jugador=input("Digite el nombre del jugador: ")
            goles_totales, total_scorers, total_penalties, delta,memo= controller.req_2(control,jugador)
            size = lt.size(goles_totales)
            tiempo=f"{delta:.3f}"
            memoria= f"{memo:.3f}"
            print("\n" + 'Tiempo [ms]: ', tiempo, '||','Memoria [kB]: ', memoria,"\n") 
            print("\n=============== Req No. 2 inputs ===============")
            print("Top N goles: " + goles)
            print("Nombre del jugador: " + jugador)
            if size < int(goles):
                print("\n Solo " + str(size) + " goles encontrados, seleccionando todos... \n")
                goles = size
            goles_totales['elements'] = goles_totales['elements'][:goles]

            print("=============== Req No. 2 Results ===============")
            print("Total de goleadores con información disponible: " + str(total_scorers))
            print("Total de goles para " + jugador + ": " + str(size))
            print("Total de penaltis para "+ jugador + ": " + str(total_penalties))
            print("\n")
            
            if lt.size(goles_totales) > 6:
                print("Los resultados tienen mas de 6 elementos...")
                print_tabulate_6(goles_totales, ["date","home_team", "away_team", "team", "scorer", "minute", "own_goal", "penalty"])
            else:
                print("Los resultados tienen menos de 6 elementos...")
                print_tabulate(goles_totales, ["date","home_team", "away_team", "team", "scorer", "minute", "own_goal", "penalty"])
            

        elif int(inputs) == 4:
            nombre=input('ingrese el nombre del país que desea consultar: ')
            fecha= input('ingrese la fecha inicial para consultar: ')
            fechaf= input('ingrese la fecha final para consultar: ')
            filtro,tamañoC,contadorTotal,contadorAway, contadorHome, delta, memo=controller.req_3(control,nombre,fecha,fechaf)
            tiempo=f"{delta:.3f}"
            memoria= f"{memo:.3f}"
            print("\n" + 'Tiempo [ms]: ', tiempo, '||','Memoria [kB]: ', memoria,"\n") 
            size=lt.size(filtro)
            print("\n=============== Req No. 3 Inputs ===============")
            print("total teams with avaible information: " + str(tamañoC))
            print("total games for  "+str(nombre) +" "+ str(contadorTotal))
            print("total home games for  "+str(nombre) +" " + str(contadorHome))
            print("total away teams for  "+str(nombre) +" " + str(contadorAway))
            if size> 6:
                print("Los resultados tienen mas de 6 elementos...")
                print_tabulate_6(filtro,["date","home_score","away_score","home_team","away_team","country","city","tournament","penalty","own_goal"])
            else:
                print("Los resultados tienen menos de 6 elementos...")
                print_tabulate(filtro, ["date","home_score","away_score","home_team","away_team","country","city","tournament","penalty","own_goal"])
            
            
            
            
        elif int(inputs) == 5:
            nombre = input("Ingrese el torneo a buscar: ")
            fecha_inicial = input("Ingrese la fecha inicial: ")
            fecha_final = input("Ingrese la fecha final: ")
            filtro, total_torneos, total_partidos, paises, ciudades, penaltis, delta, memo = controller.req_4(control, nombre,fecha_inicial,fecha_final)
            tiempo=f"{delta:.3f}"
            memoria= f"{memo:.3f}"
            print("\n" + 'Tiempo [ms]: ', tiempo, '||','Memoria [kB]: ', memoria,"\n") 
            size = lt.size(filtro)
            print("\n=============== Req No. 4 Inputs ===============")
            print("Nombre del torneo: " + nombre)
            print("Fecha de inicio: "+ fecha_inicial)
            print("Fecha final: "+ fecha_final)
            
            print("\n=============== Req No. 4 Results ===============")
            print("Total de torneos con información disponible: " + str(total_torneos))
            print("Total de partidos para: "+ nombre + ": " + str(total_partidos))
            print("Total de paises para: "+ nombre + ": " + str(paises))
            print("Total de ciudades para: "+ nombre + ": " + str(ciudades))
            print("Total de penaltis para: "+ nombre + ": " + str(penaltis))
            print("\n")
            if size> 6:
                print("Los resultados tienen mas de 6 elementos...")
                print_tabulate_6(filtro, ["date","tournament", "country", "city","home_team", "away_team","home_score", "away_score","winner"])
            else:
                print("Los resultados tienen menos de 6 elementos...")
                print_tabulate(filtro, ["date","tournament", "country", "city","home_team", "away_team","home_score", "away_score","winner"])
            
            
        elif int(inputs) == 6:
            jugador = input("Ingrese el jugador a buscar: ")
            fecha_inicial = input("Ingrese la fecha inicial: ")
            fecha_final = input("Ingrese la fecha final: ")
            filtro,sizes,s_penalty,s_autogoals, delta, memo = controller.req_5(control, jugador,fecha_inicial,fecha_final)
            tiempo=f"{delta:.3f}"
            memoria= f"{memo:.3f}"
            print("\n" + 'Tiempo [ms]: ', tiempo, '||','Memoria [kB]: ', memoria,"\n") 
            size = lt.size(filtro)
            print("\n=============== Req No. 5 Inputs ===============")
            print("Total players with available information: " +str(sizes))
            print("Total goals for " + jugador + " " + str(size))
            print("Total penalties for " + jugador + " " + str(s_penalty))
            print("Total autogoals for " + jugador + " " + str(s_autogoals))
    
            if size> 6:
                print("Los resultados tienen mas de 6 elementos...")
                print_tabulate_6(filtro, ["date","minute","home_team", "away_team","team","home_score", "away_score","tournament", "penalty","own_goal"])
            else:
                print("Los resultados tienen menos de 6 elementos...")
                print_tabulate(filtro, ["date","minute","home_team", "away_team","team","home_score", "away_score","tournament", "penalty","own_goal"])

        elif int(inputs) == 7:
            equipos=input("Ingrese el numero de equipos a consultar: ")
            torneo = input("Ingrese el torneo que desea consultar: ")
            fecha=input("Digite el año: ")
            filtro, torneos_con_info, total_teams, total_matches, total_countries, total_cities = controller.req_6(control,torneo, fecha)
            tiempo=f"{delta:.3f}"
            memoria= f"{memo:.3f}"
            print("\n" + 'Tiempo [ms]: ', tiempo, '||','Memoria [kB]: ', memoria,"\n") 
            print("\n=============== Req No. 6 Inputs ===============")
            print("Nombre del torneo: " + torneo)
            print("Top " + equipos + " equipos")
            print("Consult year: " + fecha)
            print("\n=============== Req No. 6 Results ===============")
            print("Total de torneos con informacion disponible: " + str(torneos_con_info))
            print("Total de equipos para " + torneo + ": " + str(total_teams))
            print("Total de partidos para " + torneo + ": " + str(total_matches))
            print("Total de paises para " + torneo + ": " + str(total_countries))
            print("Total de ciudades para " + torneo + " puntos: " + str(total_cities))   
            size =lt.size(filtro)
            if int(equipos) > size:
                equipos = size
            filtro = filtro["elements"][:int(equipos)]
            if  size > 6:
                print("Los resultados tienen mas de 6 elementos...")
                filtro = filtro[:3] + filtro[-3:]
                print(tabulate(filtro, headers="keys", tablefmt="grid"))
            else:
                print("Los resultados tienen menos de 6 elementos...")
                print(tabulate(filtro, headers="keys", tablefmt="grid"))

        elif int(inputs) == 8:
            torneo =input("Ingrese el torneo a consultar: ")
            puntos =input("Ingrese la cantidad de puntos: ")
            filtro, torneos_con_info, total_players, total_matches, total_goals, total_penalties, total_own_goals, total_p_2points,delta,memo = controller.req_7(control,torneo, puntos)
            tiempo=f"{delta:.3f}"
            memoria= f"{memo:.3f}"
            print("\n" + 'Tiempo [ms]: ', tiempo, '||','Memoria [kB]: ', memoria,"\n") 
            print("\n=============== Req No. 7 Inputs ===============")
            print("Nombre del torneo: " + torneo)
            print("Jugadores con " + puntos + " puntos en el ranking de goleadores")
            print("\n=============== Req No. 7 Results ===============")
            print("Total de torneos con informacion disponible: " + str(torneos_con_info))
            print("Total de jugadores para " + torneo + ": " + str(total_players))
            print("Total de partidos para " + torneo + ": " + str(total_matches))
            print("Total de goles para " + torneo + ": " + str(total_goals))
            print("Total de penalties para " + torneo + ": " + str(total_penalties))
            print("Total de autogoles para " + torneo + ": " + str(total_own_goals))
            print("Total de jugadores con " + puntos + " puntos: " + str(total_p_2points))      
            size =lt.size(filtro)
            if  size > 6:
                print("Los resultados tienen mas de 6 elementos...")
                filtro = filtro['elements'][:3] + filtro['elements'][-3:]
                print(tabulate(filtro, headers="keys", tablefmt="grid"))
            else:
                print("Los resultados tienen menos de 6 elementos...")
                print(tabulate(filtro['elements'], headers="keys", tablefmt="grid"))
                
                
        elif int(inputs) == 9:
            nombre= input("Pais que desea consultar: ")
            año1=input("Primer año para consultar: ")
            año2=input("Segundo año para consultar: ")
            filtro,primero,torneo,delta,memo,year,size_t,ultimo= controller.req_8(control,nombre,año1,año2)
            size =lt.size(filtro)
            tiempo=f"{delta:.3f}"
            memoria= f"{memo:.3f}"
            print("\n" + 'Tiempo [ms]: ', tiempo, '||','Memoria [kB]: ', memoria,"\n") 

            filtro = filtro["elements"]
            print_tabulate(primero,["date","home_team","away_team","home_score","away_score","tournament","country","city"])
            print("\n=============== Req No. 8 Inputs ===============")
            print("\n=============== "+nombre+" Stadistics"+" ===============")
            print("Years: " + str(year))
            print("Total matches: " +str(size_t))
            print("Oldest match date: " + ultimo)
            if  size > 6:
                
                print("Los resultados tienen mas de 6 elementos...")
                filtro = filtro[:3] + filtro[-3:]
                print(tabulate(filtro, headers="keys", tablefmt="grid"))
            else:
                print("Los resultados tienen menos de 6 elementos...")
                print(tabulate(filtro, headers="keys", tablefmt="grid"))
        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
