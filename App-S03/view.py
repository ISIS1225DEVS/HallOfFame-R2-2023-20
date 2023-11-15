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


def new_controller():
    EDPartidos='ARRAY_LIST'
    EDGoleadores='ARRAY_LIST'
    EDPenales='ARRAY_LIST'
    """
    Crea una instancia del modelo
    """
    control = controller.new_controller()
    return control

def printLoadDataAnswer(answer,mem):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    if mem == True:
        print("Tiempo [ms]: ", f"{answer[4]:.3f}", "||",
              "Memoria [kB]: ", f"{answer[5]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer[4]:.3f}")


def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Listar los últimos N partidos de un equipo según su condición")
    print("3- Listar los últimos N goles anotados por un jugador")
    print("4- Consultar los partidos que disputó un equipo durante un periodo especifico")
    print("5- Consultar los partidos relacionados con un torneo durante un periodo especifico")
    print("6- Consultar las anotaciones de un jugador durante un periodo especifico")
    print("7- Clasificar los N mejores equipos de un torneo en un año especifico")
    print("8- Encontrar los anotadores con N puntos dentro un torneo especifico")
    print("9- Consultar el desempeño historico de dos selecciones en torneos oficiales")
    print("0- Salir")
    

filepartidos =  "Data/results-utf8-10pct.csv"
filegoleadores = "Data/goalscorers-utf8-10pct.csv"
filepenales = "Data/shootouts-utf8-10pct.csv"


def load_data(control, memflag):
    """
    Carga los datos
    """
    answer = controller.load_data(control,filepartidos,filegoleadores,filepenales, memflag)
    return  answer


def print_carga(partidos, goleadores, penales):
     print("-----------------------------------------------")
     print("Número de Partidos: " + str(partidos["size"]))
     print("Número de Goleadores: " + str(goleadores["size"]))
     print("Número de Penales: " + str(penales["size"]))
     print("-----------------------------------------------"+"\n")
     
     print("═══════════════════════════════════════════════")
     print("---------REPORTE RESULTADOS DE LA FIFA---------")
     print("═══════════════════════════════════════════════"+"\n")
     
     print("Imprimiendo resultados para los primeros 3 y los ultimos 3 datos en el archivo"+"\n")
     print("------RESULTADOS PARTIDOS------")
     print("Número de Partidos: " + str(lt.size(partidos)))
     print("La estructura de resultados tiene mas de 6 datos...")
     controller.sort_date(partidos)
     sub_partidos = lt.subList(partidos, 1, 3)
     for i in [2,1,0]:
         lt.addLast(sub_partidos, lt.getElement(partidos,lt.size(partidos)-i))
     print(tabulate(lt.iterator(sub_partidos),headers="keys",tablefmt="grid")+"\n")
     
     print("------RESULTADOS GOLEADORES------")
     print("Número de Goleadores: " + str(lt.size(goleadores)))
     print("La estructura de resultados tiene mas de 6 datos...")
     controller.sort_date(goleadores)
     sub_goleadores = lt.subList(goleadores, 1, 3) 
     for i in [2,1,0]:
         lt.addLast(sub_goleadores, lt.getElement(goleadores,lt.size(goleadores)-i))
     print(tabulate(lt.iterator(sub_goleadores),headers="keys",tablefmt="grid")+"\n")
     
     print("------RESULTADOS PENALES------")
     print("Número de Penales: " + str(lt.size(penales)))
     print("La estructura de resultados tiene mas de 6 datos...")
     controller.sort_date(penales)
     sub_penales = lt.subList(penales, 1, 3)
     for i in [2,1,0]:
         lt.addLast(sub_penales, lt.getElement(penales,lt.size(penales)-i))
     print(tabulate(lt.iterator(sub_penales),headers="keys",tablefmt="grid")+"\n")
    


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(teams,NPartidos,equipo,condicion):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    start=controller.get_time()
    totalequippos, totalpartidos, total_condicion, partidos_equipo = controller.req_1(teams,NPartidos,equipo,condicion)
    end=controller.get_time()
    delay=controller.delta_time(start,end)
    print(delay)
    
    print("====================Inputs Req. No 1===========================")
    print("TOP N matches:" + str(NPartidos))
    print("Team name:" + equipo) 
    print("Team condition: "+ condicion) 
    print("")

    print("===================Req. No 1 Results========================")
    print("Total teams with available information: " + str(totalequippos))
    print("Total matches for " + equipo + ": " + str(totalpartidos))
    print("Total matches for " + equipo + " as " + condicion + ": " + str(total_condicion))

    print("Selecting " + str(totalpartidos) + " matches")
    print("")
    if total_condicion < 6 and  total_condicion < NPartidos:
        print("El resultado tiene menos de 6 datos")
        print(tabulate(lt.iterator(partidos_equipo),headers="keys",tablefmt="grid")+"\n")
    else:
        print("El resultado tiene mas de 6 datos")
        print("")
        sub_req1 = lt.subList(partidos_equipo, 1, 3)
        for i in [2,1,0]:
            lt.addLast(sub_req1, lt.getElement(partidos_equipo,lt.size(partidos_equipo)-i))
        print(tabulate(lt.iterator(sub_req1),headers="keys",tablefmt="grid")+"\n")


    # TODO: Imprimir el resultado del requerimiento 1

    pass


def print_req_2(goleadores,n_goals,jugador):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
   
    start=controller.get_time()
    total_jogadores,total_anotaciones,sub_penal,Scorer= controller.req_2(goleadores,n_goals,jugador)
    end=controller.get_time()
    delay=controller.delta_time(start,end)
    print(delay)
    
  
    
    print("====================Inputs Req. No 2===========================")
    print("Number of scores:" + str(n_goals))
    print("Player name:" + jugador)  
    print("")

    print("===================Req. No 2 Results========================")
    print("Total scorers found:" + str(total_jogadores))
    print("Total scores found:" + str(total_anotaciones))
    print("Total Penalties:" + str(sub_penal))
    
    print("Selecting " + str(total_anotaciones) + " scorers")
    print("")
    if total_anotaciones < 6 and  total_anotaciones < int(n_goals):
        print("El resultado tiene menos de 6 datos")
        print(tabulate(lt.iterator(Scorer),headers="keys",tablefmt="grid")+"\n")
    else:
        print("El resultado tiene mas de 6 datos")
        print("")
        sub_req2 = lt.subList(Scorer, 1, 3)
        for i in [2,1,0]:
            lt.addLast(sub_req2, lt.getElement(Scorer,lt.size(Scorer)-i))
        print(tabulate(lt.iterator(sub_req2),headers="keys",tablefmt="grid")+"\n")


def print_req_3(teams,goleadore_team,equipo,inicio,final):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    start=controller.get_time()
    fltpartidos,total,totalhome,totalaway,totalequippos = controller.req_3(teams,goleadore_team,equipo,inicio,final)
    end=controller.get_time()
    delay=controller.delta_time(start,end)
    print(delay)


    print("====================Inputs Req. No 3===========================")
    print("Team name:" + equipo)
    print("Start date:" + inicio)
    print("End date:" + final)   
    print("")

    print("=================== Req. No 3 Results ========================")
    print(" Total teams: " + str(totalequippos))
    print(equipo + " Total games: " + str(total))
    print(equipo + " Total home games: " + str(totalhome))
    print(equipo + " Total away games: " + str(totalaway))
    print("")

    if total < 6: 
        print("El resultado tiene menos de 6 datos")
        print(tabulate(lt.iterator(fltpartidos),headers="keys",tablefmt="grid")+"\n")
    else:
        print("El resultado tiene mas de 6 datos")
        print("")
        sub_list = lt.subList(fltpartidos, 1, 3)
        for i in [2,1,0]:
            lt.addLast(sub_list, lt.getElement(fltpartidos,lt.size(fltpartidos)-i))
        print(tabulate(lt.iterator(sub_list),headers="keys",tablefmt="grid")+"\n") 



    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(torneos,penales_team,torneo,inicio,final):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    start=controller.get_time()
    total_torneos,total_partidos, totalcountry,totalcity,totalshoot,req4 =controller.req_4(torneos,penales_team,torneo,inicio,final)
    end=controller.get_time()
    delay=controller.delta_time(start,end)
    print(delay)

    
    print("====================Inputs Req. No 4===========================")
    print("Nombre del Torneo: " + torneo)
    print("Fecha de Inicio: " + inicio)
    print("Fecha de Inicio: " + final)   
    print("")
    
    print("===================Resultados Req. No 4========================")
    print("Total de torneos disponibles: " + str(total_torneos))
    print("Total de partidos del torneo " + torneo + ": " + str(total_partidos))
    print("Total de paises del torneo " + torneo + ": " + str(totalcountry))
    print("Total de ciudades del torneo " + torneo + ": " + str(totalcity))
    print("Total de partidos definidos por penales del torneo " + torneo + ": " + str(totalshoot))
    

    print("")
    if size < 6:
        print("El resultado tiene menos de 6 datos")
        print(tabulate(lt.iterator(req4),headers="keys",tablefmt="grid")+"\n")
    else:
        print("El resultado tiene mas de 6 datos")
        print("")
        sub_req4 = lt.subList(req4, 1, 3)
        for i in [2,1,0]:
            lt.addLast(sub_req4, lt.getElement(req4,lt.size(req4)-i))
        print(tabulate(lt.iterator(sub_req4),headers="keys",tablefmt="grid")+"\n")


def print_req_5(Top,jugador,fecha_ini,fecha_fin):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    time=controller.get_time()
    total_goals,total_tournaments,total_penalties,total_autogoals,scorer_prime=controller.req_5(Top,jugador,fecha_ini,fecha_fin)
    delay=controller.get_time()
    delta=controller.delta_time(time,delay)
    print(delta)
    
    print("===================Resultados Req. No 5========================")
    print("Goles totales de " + jugador + ": " + str(total_goals))
    print("Total de torneos de " + jugador+ ": " + str(total_tournaments))
    print("Numero de goles de penal"+ ": " + str(total_penalties))
    print("Numero de autogoles"+ ": " + str(total_autogoals))
    
    if total_goals < 6:
        print("El resultado tiene menos de 6 datos")
        print(tabulate(lt.iterator(scorer_prime),headers="keys",tablefmt="grid")+"\n")
    else:
        print("El resultado tiene mas de 6 datos")
        print("")
        sub_req5 = lt.subList(scorer_prime, 1, 3)
        for i in [2,1,0]:
            lt.addLast(sub_req5, lt.getElement(scorer_prime,lt.size(scorer_prime)-i))
        print(tabulate(lt.iterator(sub_req5),headers="keys",tablefmt="grid")+"\n")

    

def print_req_6(torneos,years,goleadores_team,Nequipos,torneo,year):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    
    
    start=controller.get_time()
    total_years, total_equipos, total_partidos, totalcountry, totalcity, req6 = controller.req_6(torneos,years,goleadores_team,Nequipos,torneo,year)
    end=controller.get_time()
    delay=controller.delta_time(start,end)
    print(delay)
    
    
    print("====================Inputs Req. No 7===========================")
    print("Tournament name:" + torneo)
    print("TOP N " + str(Nequipos) + " team ranking")
    print("Consult year:" + year) 
    print("Start date: " + year + "-01-01 in consult year")  
    print("End date: " + year + "-12-31 in consult year")  
    print("")
    

    print("===================Req. No 7 Results========================")
    #print("Total tournaments with available information: " + str(total_torneos))
    print("Total teams for " + torneo + ": " + str(total_equipos))
    print("Total matches for " + torneo + ": " + str(total_partidos))
    print("Total countries for " + torneo + ": " + str(totalcountry))
    print("Total cities for " + torneo + ": " + str(totalcity))
    print("")

    total = lt.size(req6)

    if total < 6:
        print("El resultado tiene menos de 6 datos")
        print(tabulate(lt.iterator(req6),headers="keys",tablefmt="grid")+"\n")
    else:
        print("El resultado tiene mas de 6 datos")
        print("")
        sub_req6 = lt.subList(req6, 1, 3)
        for i in [2,1,0]:
            lt.addLast(sub_req6, lt.getElement(req6,lt.size(req6)-i))
        print(tabulate(lt.iterator(sub_req6),headers="keys",tablefmt="grid")+"\n")



def print_req_7(torneos,goleadores_team,torneo, NPuntos):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    start=controller.get_time()
    total_torneos,total_scorers,total_partidos,total_goles, total_penales, total_owngoales, req7 = controller.req_7(torneos,goleadores_team,torneo, NPuntos)
    total_req7 = lt.size(req7)
    end=controller.get_time()
    delay=controller.delta_time(start,end)
    print(delay)


    print("====================Inputs Req. No 7===========================")
    print("Tournament name:" + torneo)
    print("Players with " + str(NPuntos) + " in the scorer ranking")  
    print("")

    print("===================Req. No 7 Results========================")
    print("Total tournaments with available information: " + str(total_torneos))
    print("Total players for " + torneo + ": " + str(total_scorers))
    print("Total matches for " + torneo + ": " + str(total_partidos))
    print("Total goals for " + torneo + ": " + str(total_goles))
    print("Total penalties for " + torneo + ": " + str(total_penales))
    print("Total own goals for " + torneo + ": " + str(total_owngoales))
    print("")
    print("Total of players with "+ str(NPuntos) + " points: " + str(total_req7) )

    if total_req7 < 6:
        print("El resultado tiene menos de 6 datos")
        print(tabulate(lt.iterator(req7),headers="keys",tablefmt="grid")+"\n")
    else:
        print("El resultado tiene mas de 6 datos")
        print("")
        sub_req7 = lt.subList(req7, 1, 3)
        for i in [2,1,0]:
            lt.addLast(sub_req7, lt.getElement(req7,lt.size(req7)-i))
        print(tabulate(lt.iterator(sub_req7),headers="keys",tablefmt="grid")+"\n")


    



def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        mem=False
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            control = new_controller()
            print("Cargando información de los archivos ....\n")
            print("Desea observar el uso de memoria? (True/False)")
            mem = input("Respuesta: ")
            mem = castBoolean(mem)
            answer = load_data(control, memflag=mem)
            partidos = answer[0]
            goleadores = answer[1]
            penales = answer[2]
            scorer = answer[3]
            Top_SC= answer[4] 
            torneos=answer[6]
            teams=answer[7]
            goleadores_team=answer[8]
            penales_team=answer[9]
            years=answer[10]

            print_carga(partidos, goleadores, penales)

            size=mp.size(scorer)
            print("Se cargaron los siguientes archivos ordenados por la llave de jugador: "+ str(size) )
            
            
        elif int(inputs) == 2:
            equipo = input('Ingrese el nombre del equipo (selección nacional en ingles):\n')
            NPartidos = int(input('Ingrese el numero de partidos de consulta:\n'))
            print("1.Local")
            print("2.Visitante")
            print("3.Indiferente")
            condicion=None
            while condicion==None:
                ConInput = input('Ingrese la condicion del equipo:\n')
                if int(ConInput) == 1:
                    condicion = "local"
                elif int(ConInput) == 2:
                    condicion = "visitante"
                elif int(ConInput) == 3:
                    condicion = "indiferente"
                else:
                    print("Esa opcion no es valida")
            
            print_req_1(teams,NPartidos,equipo,condicion)

        elif int(inputs) == 3:
            jugador = str(input('Ingrese el nombre completo del jugador:\n'))
            n_goals = str(input('Ingrese el número de goles que desea consultar:\n'))
            print_req_2(scorer,n_goals,jugador)
            

        elif int(inputs) == 4:
            equipo = str(input('Ingrese el nombre del equipo:\n'))
            inicio = str(input('Ingrese la fecha inicial del periodo a consultar (AÑO-MES-DIA Ej:2020-03-01):\n'))
            final = str(input('Ingrese la fecha final del periodo a consultar (AÑO-MES-DIA Ej:2020-03-01):\n'))
            print_req_3(teams,goleadores_team,equipo,inicio,final)

        elif int(inputs) == 5:
            torneo = str(input('Ingrese el nombre del torneo:\n'))
            inicio = str(input('Ingrese la fecha inicial del periodo a consultar (AÑO-MES-DIA Ej:2020-03-01):\n'))
            final = str(input('Ingrese la fecha final del periodo a consultar (AÑO-MES-DIA Ej:2020-03-01):\n'))
            print_req_4(torneos,penales_team,torneo,inicio,final)

        elif int(inputs) == 6:
            jugador= str(input('Ingrese el nombre del jugador a consultar:\n'))
            inicio = str(input('Ingrese la fecha inicial del periodo a consultar (AÑO-MES-DIA Ej:2020-03-01):\n'))
            final = str(input('Ingrese la fecha final del periodo a consultar (AÑO-MES-DIA Ej:2020-03-01):\n'))
            
            print_req_5(Top_SC,jugador,inicio,final)

        elif int(inputs) == 7:
            Nequipos = str(input('Ingrese el numero (N) de equipos de la consulta:\n'))
            torneo = str(input('Ingrese el nombre del torneo a consultar:\n'))
            year = str(input('Ingrese el año de la consulta:\n'))
            print_req_6(torneos,years,goleadores_team,Nequipos,torneo,year)

        elif int(inputs) == 8:
            torneo = str(input('Ingrese el nombre del torneo a consultar:\n'))
            NPuntos = str(input('Ingrese el puntaje(N) de jugadores dentro del torneo:\n'))
            print_req_7(torneos,goleadores_team,torneo, NPuntos)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
