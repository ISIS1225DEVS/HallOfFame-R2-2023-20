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
import tracemalloc

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
    
    t = int(input("Elija el tipo de mapeo que desea usar: \n 1-Probing\n 2-Chaining\n" ))
    f = float(input("Digite el factor de carga: "))


    control = controller.new_controller(t,f)

    return control
    



def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Listar los últimos N partidos de un equipo según su condición")
    print("3- Listar los primeros N goles anotados por un jugador")
    print("4- Consultar los partidos que disputó un equipo durante un periodo especifico")
    print("5- Consultar los partidos relacionados con un torneo durante un periodo especifico")
    print("6- Consultar las anotaciones de un jugador durante un periodo especifico")
    print("7- Clasificar los N mejores equipos del año dentro de un torneo especifico")
    print("8- Encontrar los anotadores con N puntos dentro un torneo especifico")
    print("9- Consultar el desempeño histórico de una selección en torneos oficiales")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos

    tamanho = ''
    c = int(input('Elija el tamaño del archivo que desea usar: \n 1-5pct\n 2-10pct\n 3-20pct\n 4-30pct\n 5-50pct\n 6-80pct\n 7-large\n 8-small\n'))
    if c == 1:
        tamanho = '5pct'
    elif c == 2:
        tamanho = '10pct'
    elif c == 3:
        tamanho = '20pct'
    elif c == 4:
        tamanho = '30pct'
    elif c == 5:
        tamanho = '50pct'
    elif c == 6:
        tamanho = '80pct'
    elif c == 7:
        tamanho = 'large'
    elif c == 8:
        tamanho = 'small'
    else:
        tamanho = 'small'


    goleador = controller.load_data_goalscorers(control,tamanho)
    resultados = controller.load_data_results(control,tamanho)
    tiros = controller.load_data_shoootouts(control,tamanho)
    hometeam = controller.load_hometeam(control,tamanho)
    awayteam = controller.load_awayteam(control,tamanho)
    torneo = controller.load_torneo(control,tamanho)
    goleadores_m = controller.load_goleadores_m(control, tamanho)
    
    return goleador, resultados, tiros, hometeam, awayteam, torneo, goleadores_m

def print_data(control):
    """
        Función que imprime un dato dado su ID
    """

    #TODO: Realizar la función para imprimir un elemento
    """
    Función que imprime los datos en formato tabular.
    """
    print("-----------------------")
    print("Resultados count: " + str(lt.size(control['resultados'])))
    print("Goleadores count: " + str(lt.size(control['goleadores'])))
    print("Tiros count: " + str(lt.size(control['tiros'])))
    print("-----------------------")


    print("=======================================")
    print("==========FIFA RECORDS REPORT==========")
    print("=======================================")

    print("Información de los tres primeros y tres últimos partidos:")

    lista_r = []
    lista_g = []
    lista_t = []
    for datos in control['resultados']['elements']:
        lista_r.append(datos)
    for datos in control['goleadores']['elements']:
        lista_g.append(datos)
    for datos in control['tiros']['elements']:
        lista_t.append(datos)

    a = len(lista_r) -1
    b = len(lista_r) -2
    c = len(lista_r) -3
    
    prnt = [lista_r[0], lista_r[1], lista_r[2], lista_r[a], lista_r[b], lista_r[c]]
    print('resultados: ' + str(len(lista_r)))
    print(tabulate(prnt, headers = 'keys', tablefmt = 'grid'))


    d = len(lista_g) -1
    e = len(lista_g) -2
    f = len(lista_g) -3

    prnt = [lista_r[0], lista_r[1], lista_r[2], lista_r[d], lista_r[e], lista_r[f]]
    print('goleadores: ' + str(len(lista_g)))
    print(tabulate(prnt, headers = 'keys', tablefmt = 'grid'))

    g = len(lista_t) -1
    h = len(lista_t) -2
    i = len(lista_t) -3

    prnt = [lista_t[0], lista_t[1], lista_t[2], lista_t[g], lista_t[h], lista_t[i]]
    print('tiros: ' + str(len(lista_t)))
    print(tabulate(prnt, headers = 'keys', tablefmt = 'grid'))


  


def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    
    numero_partidos = int(input('Ingrese el numero de partidos de consulta: '))
    nombre_equipo = input('Ingrese el nombre del equipo (país de selección en inglés): ')
    condicion_equipo = int(input('Seleccione:\n 1. Local\n 2. Visitante \n '))
    lista,delta_time_r = controller.req_1(control, numero_partidos,nombre_equipo,condicion_equipo)
    

    print('==========req No 1 inputs ========== ')
    print('Numero de partidos: ' + str(numero_partidos))
    print('Nombre equipo: ' + nombre_equipo)
    if condicion_equipo == 1:
        cond = 'home'
    elif condicion_equipo == 2:
        cond = 'away'
    else:
        cond = ''

    print('Condicion equipo: ' + cond)

    print('\n\n==========req No 1 results ========== ')

    print('Partidos totales encontrados: ' + str(len(lista)))
    print('Seleccionando ' + str(numero_partidos) + ' partidos')
    print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")

    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3

    if len(lista) > numero_partidos and len(lista) < 6:
        prnt = []
        while numero_partidos > 0:
            prnt.append(lista[t])
            numero_partidos -=1
            t-= 1
        print(tabulate(prnt, headers = 'keys', tablefmt = 'grid'))
    elif len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]

        print(tabulate(prnt, headers = 'keys', tablefmt = 'grid'))
    else:
        print(tabulate(lista, headers = 'keys', tablefmt = 'grid'))

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    goles = int(input('Ingrese el numero de goles de consulta: '))
    goleador = input('Ingrese el nombre del goleador: ')
    lista,delta_time_r=controller.req_2(control,goles,goleador)
    print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")

    
    a=len(lista)-1
    b=len(lista)-2
    c=len(lista)-3

    if len(lista) > goles and len(lista) < 6:
        prnt = []
        while goles > 0:
            prnt.append(lista[l])
            goles -=1
            l-= 1
        print(tabulate(prnt, headers = 'keys', tablefmt = 'grid'))
    elif len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]

        print(tabulate(prnt, headers = 'keys', tablefmt = 'grid'))
    else:
        print(tabulate(lista, headers = 'keys', tablefmt = 'grid'))



def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    nombre_equipo = input("Ingrese el nombre del equipo que desea consultar: ")
    fecha_inicial = input('Ingrese la fecha inicial del periodo que desea consultar (El formato ha de ser: %Y-%M-%D, por ejemplo: 1998-05-25): ')
    fecha_final = input('Ingrese la fecha final del periodo que desea consultar (El formato ha de ser: %Y-%M-%D, por ejemplo: 1998-05-25): ')

    lista, num_partidos, num_partidos_equipo, num_home, num_away, delta_time = controller.req_3(control, nombre_equipo, fecha_inicial, fecha_final)
    print('==========req No 3 inputs ========== ')
    print('Nombre equipo: ' + nombre_equipo)
    print('Fecha inicial: ' + fecha_inicial)
    print('Fecha final: ' + fecha_final)

    print('==========req No 3 inputs ========== ')
    print('Juegos totales con informacion disponible: ' + str(num_partidos))
    print('Juegos totales de ' + nombre_equipo + ': ' + str(num_partidos_equipo))
    print(str(nombre_equipo) + ' jugo como local: ' + str(num_home))
    print(str(nombre_equipo) + ' jugo como visitante: ' + str(num_away))
    print("El tiempo de ejecución es: "+ str(round(delta_time,2))+" milisegundos")

    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3
    if len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]

        print(tabulate(prnt, headers = 'keys', tablefmt = 'grid'))
    else:
        print(tabulate(lista, headers = 'keys', tablefmt = 'grid'))


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    nombre_torneo = (input("Dijite el nombre del torneo: "))
    fecha_i= (input("Dijite la fecha del rango inferior el cual desea la busqueda: "))
    fecha_f= (input("Dijite la fecha del rango superior el cual desea la busqueda: "))

    lista,delta_time_r = controller.req_4(control, nombre_torneo,fecha_i,fecha_f)
    print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")

    a=len(lista)-1
    b=len(lista)-2
    c=len(lista)-3
    prnt=[lista[a],lista[b],lista[c],lista[0],lista[1],lista[2]]
    if len(lista)>6:
        print(tabulate(prnt,headers="keys",tablefmt="grid"))

    else:
        print(tabulate(lista,headers="keys",tablefmt="grid"))


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    nombre_jugador = input("Ingrese el nombre del jugador que desea consultar: ")
    fecha_inicial = input('Ingrese la fecha inicial del periodo que desea consultar (El formato ha de ser: %Y-%M-%D, por ejemplo: 1998-05-25): ')
    fecha_final = input('Ingrese la fecha final del periodo que desea consultar (El formato ha de ser: %Y-%M-%D, por ejemplo: 1998-05-25): ')
    lista,torneos,penaltis,autogoles,delta_time_r = controller.req_5(control, nombre_jugador, fecha_inicial, fecha_final)  


    print('==========Req No 5 inputs ========== ')
    print('Nombre del jugador: ' + nombre_jugador)
    print('Fecha inicial: ' + fecha_inicial)
    print('Fecha final: ' + fecha_final)

    print('==========Req No 5 results ========== ')
    print(nombre_jugador + ' Goles totales: ' +  str(len(lista)))
    print(nombre_jugador + ' Torneos totales: ' + str(torneos))
    print(nombre_jugador + ' Penales totales: ' + str(penaltis))
    print(nombre_jugador + ' Autogoles totales: ' + str(autogoles))
    print("El tiempo de ejecución es: "+ str(round(delta_time_r,2))+" milisegundos")

    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3
    if len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]

        print(tabulate(prnt, headers = 'keys', tablefmt = 'grid'))
    else:
        print(tabulate(lista, headers = 'keys', tablefmt = 'grid'))


def print_req_6(control):
    #"""
    #    Función que imprime la solución del Requerimiento 6 en consola
    #"""
    # TODO: Imprimir el resultado del requerimiento 6
    num_equipos = int(input('Ingrese el numero de equipos que desea consultar: '))
    nombre_torneo = input ('Ingrese el nombre del torneo que desea consultar: ')
    anio = int(input('Ingrese la fecha que desea consultar: '))
    lista, respuesta_general,diferencia_t = controller.req_6(control, nombre_torneo, anio, num_equipos)
    
    print('==========Req No 6 inputs ========== ')
    print('Nombre del torneo: ' + nombre_torneo)
    print('Numero de equipos: '+ str(num_equipos))
    print('Fecha inicial: ' + str(anio))

    print('==========Req No 6 results ========== ')
    print('Numero de años del historial: ' + str(respuesta_general['Total años del historial ']))
    print('Torneos en el año seleccionado ' + str(respuesta_general['Total torneos en el año seleccionado ']))
    print('Equipos en ' + nombre_torneo + ': ' +  str(respuesta_general['Total equipos del torneo ']))
    print('Numero de partidos en ' + nombre_torneo + ': ' + str(respuesta_general['Total encuentros disputados ']))
    print('Paises involucrados en ' + nombre_torneo + ': ' + str(respuesta_general['Total paises involucrados ']))
    print('Ciudades en los que se jugo ' + nombre_torneo + ': ' + str(respuesta_general['Total ciudades involucradas ']))
    print('Ciudad con mas partidos en ' + nombre_torneo + ': ' + str(respuesta_general['Ciudad con mas partidos ']))
    print("El tiempo de ejecución es: "+ str(round(diferencia_t,2))+" milisegundos")
    
    prnt = []
    
    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3
    
    if len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]
        for d in prnt:
            d['Mejor Jugador'] = tabulate([[k,v] for k,v in d['Mejor Jugador'].items()],headers =['Campo','valor'],tablefmt='grid',maxcolwidths = [None, None, 5, None, 9, 7, 13, 6, 5, None, 6, 7, 17])

        print(tabulate(prnt,headers = 'keys', tablefmt = 'grid'))
    else:
        for d in prnt:
            d['Mejor Jugador'] = tabulate([[k,v] for k,v in d['Mejor Jugador'].items()],headers =['Campo','valor'],tablefmt='grid',maxcolwidths = [None, None, 5, None, 9, 7, 13, 6, 5, None, 6, 7, 17])
        print(tabulate(lista,headers = 'keys', tablefmt = 'grid'))   


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    
    torneo = input('Ingrese el nombre del torneo que desea consultar: ')
    puntos = int(input('puntaje de los jugadores dentro del torneo: '))

    lista,total_goles,total_penaltis,total_autogoles,total_jugadores,diferencia_t = controller.req_7(control, torneo, puntos)

    print('==========req No 7 inputs ========== ')
    print("nombre del torneo: " + str(torneo))
    print("jugadores con: " + str(puntos) + " puntos")

 
    print('==========req No 7 results ========== ')
    print('Torneos oficiales total jugadores: ' + str(total_jugadores))
    print('Torneos oficiales total goles: ' + str(total_goles))
    print('Torneos oficiales total penaltis: ' + str(total_penaltis))
    print('Torneos oficiales total autogoles: ' + str(total_autogoles))
    print("El tiempo de ejecución es: "+ str(round(diferencia_t,2))+" milisegundos")

    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3
    
    if len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]

        for d in prnt:
            d['último_gol'] = tabulate([[k,v] for k,v in d['último_gol'].items()],headers =['Campo','valor'],tablefmt='grid',maxcolwidths = [None, None, 5, None, 9, 7, 13, 6, 5, None, 6, 7, 17])

        print(tabulate(prnt,headers = 'keys', tablefmt = 'pretty'))

    else:
        for d in lista:
            d['último_gol'] = tabulate([[k,v] for k,v in d['último_gol'].items()],headers =['Campo','valor'],tablefmt='grid',maxcolwidths = [None, None, 5, None, 9, 7, 13, 6, 5, None, 6, 7, 17])

        print(tabulate(lista,headers = 'keys', tablefmt = 'grid'))


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    
    pais = input('Ingrese el pais que desea consultar: ')
    anio_i = int(input('Ingrese el primer año: '))
    anio_f = int(input('Ingrese el segundo año: '))

    lista,diferencia_t = controller.req_8(control, pais, anio_i, anio_f)
    print("El tiempo de ejecución es: "+ str(round(diferencia_t,2))+" milisegundos")
    a = len(lista) - 1
    b = len(lista) - 2
    c = len(lista) - 3
    if len(lista) > 6:
        prnt = [lista[0], lista[1], lista[2], lista[a], lista[b], lista[c]]

        print(tabulate(prnt, headers = 'keys', tablefmt = 'grid'))
    else:
        print(tabulate(lista, headers = 'keys', tablefmt = 'grid'))



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
            print('Elija que tipo de sort desea usar: ')
            print('1-selection sort')
            print('2-insertion sort')
            print('3-shell sort')
            s = 0
            ch = int(input('Ingrese su seleccion: '))
            if ch == 1:
                s = 1
                print('Se utilizara el selection sort')
            elif ch == 2:
                s = 2
                print('Se utilizara el insertion sort')
            elif ch == 3:
                s = 3
                print('Se utilizara el shell sort')
            else:
                s = 3
                print('Opcion no valida se utilizara el shell sort como predeterminado')

            control = controller.sort(control,s)
            print_data(control)

        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

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
