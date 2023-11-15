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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
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
assert cf
import datetime as dt

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs(tipo, factorcarga):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    data_structs = {'resultados':None,
                    'goleadores':None,
                    'tiros':None,
                    'hteam': None,
                    'ateam':None,
                    'torneo':None,
                    'goleadores_m':None,
                    'ciudad':None
                    }
    
    if tipo == 1:
        data_structs['hteam'] = mp.newMap(720/factorcarga, loadfactor=factorcarga,maptype='PROBING')
        data_structs['ateam'] = mp.newMap(720/factorcarga, loadfactor=factorcarga,maptype='PROBING')
        data_structs['torneo'] = mp.newMap(720/factorcarga, loadfactor=factorcarga,maptype='PROBING')
        data_structs['goleadores_m'] = mp.newMap(400/factorcarga, loadfactor=factorcarga,maptype='PROBING')
        
        
    elif tipo  == 2:
        data_structs['hteam'] = mp.newMap(720/factorcarga, loadfactor=factorcarga,maptype='CHAINING')
        data_structs['ateam'] = mp.newMap(720/factorcarga, loadfactor=factorcarga,maptype='CHAINING')
        data_structs['torneo'] = mp.newMap(720/factorcarga, loadfactor=factorcarga,maptype='CHAINING')
        data_structs['goleadores_m'] = mp.newMap(400/factorcarga, loadfactor=factorcarga,maptype='CHAINING')
        


    data_structs['resultados']=lt.newList('ARRAY_LIST')
    data_structs['goleadores']=lt.newList('ARRAY_LIST')
    data_structs['tiros']=lt.newList('ARRAY_LIST')

    return data_structs


# Funciones para agregar informacion al modelo
def add_goleadores_m(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    if (mp.contains(data_structs['goleadores_m'], data['scorer']))==False:
        lista_nueva = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lista_nueva,data)
        mp.put(data_structs['goleadores_m'], data['scorer'], lista_nueva)
    else:
        lista = me.getValue(mp.get(data_structs['goleadores_m'], data['scorer']))
        lt.addLast(lista, data)
        mp.put(data_structs['goleadores_m'], data['scorer'], lista)

def add_torneo(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    if (mp.contains(data_structs['torneo'], data['tournament']))==False:
        lista_nueva = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lista_nueva,data)
        mp.put(data_structs['torneo'], data['tournament'], lista_nueva)
    else:
        lista = me.getValue(mp.get(data_structs['torneo'], data['tournament']))
        lt.addLast(lista, data)
        mp.put(data_structs['torneo'], data['tournament'], lista)

def add_hometeam(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    if (mp.contains(data_structs['hteam'], data['home_team']))==False:
        lista_nueva = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lista_nueva,data)
        mp.put(data_structs['hteam'], data['home_team'], lista_nueva)
    else:
        lista = me.getValue(mp.get(data_structs['hteam'], data['home_team']))
        lt.addLast(lista, data)
        mp.put(data_structs['hteam'], data['home_team'], lista)

def add_awayteam(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    if (mp.contains(data_structs['ateam'], data['away_team']))==False:
        lista_nueva = lt.newList(datastructure = 'ARRAY_LIST')
        lt.addLast(lista_nueva,data)
        mp.put(data_structs['ateam'], data['away_team'], lista_nueva)
    else:
        lista = me.getValue(mp.get(data_structs['ateam'], data['away_team']))
        lt.addLast(lista, data)
        mp.put(data_structs['ateam'], data['away_team'], lista)
def add_goalscorers(football_data,data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    
    
    goleador = {"date": data["date"],"home_team":data["home_team"], "away_team":data["away_team"], "team":data["team"], 
                "scorer": data["scorer"], "minute":data["minute"], "own_goal":data["own_goal"], "penalty":data["penalty"]}
    lt.addLast(football_data["goleadores"], goleador)

def add_results(football_data, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    resultado = {"date": data["date"], "home_team":data["home_team"], "away_team": data["away_team"], "home_score":data["home_score"],
                           "away_score":data["away_score"], "tournament":data["tournament"], "city":data["city"], "country":data["country"], "neutral":data["neutral"]}
    lt.addLast(football_data["resultados"], resultado) 

def add_shotouts(football_data, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    tiro = {"date":data["date"],"home_team":data["home_team"], "away_team":data["away_team"], "winner":data["winner"]}
    lt.addLast(football_data["tiros"], tiro)

# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(control,numero_partidos:int, nombre_equipo: str, condicion_equipo:int):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1  

    if condicion_equipo == 1:
        control_r = control['hteam']
        map = mp.get(control_r,nombre_equipo)
        lista = me.getValue(map)
    if condicion_equipo == 2:
        control_r = control['ateam']
        map = mp.get(control_r,nombre_equipo)
        lista = me.getValue(map)
        
    quk.sort(lista,compareDates)
    return lista


def req_2(control,goles,goleador):
    """
    Función que soluciona el requerimiento 2
    """
        # TODO: Realizar el requerimiento 2
    r=[]
    controlg=control["goleadores_m"]
    map=mp.get(controlg,goleador)

    lista= me.getValue(map)
    quk.sort(lista,compareDates)
    return lista

def req_3(control, nombre_equipo, fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
 
    
    respuesta = lt.newList('ARRAY_LIST')

    control_h = control['hteam']
    control_a = control['ateam']
    control_t = control['goleadores'] 
   
    map_h = mp.get(control_h, nombre_equipo)
    map_a = mp.get(control_a, nombre_equipo)
    mapa = union(map_h, map_a) 

    respuesta = filtrar_fechas(lt.iterator(mapa), fecha_inicial, fecha_final)

    for e in lt.iterator(respuesta):
        for fila in lt.iterator(control_t):
            if e['date'] == fila['date'] and (e['home_team'] == fila['home_team'] or e['away_team'] == fila['away_team']) :
                e['penalty'] = fila['penalty']
                e['own_goal'] = fila['own_goal']
        if "penalty" not in e.keys():
            e['penalty'] = "Desconocido"
        if "own_goal" not in e.keys():
            e['own_goal'] = "Desconocido"

    return respuesta, mapa['size'], respuesta['size'], lt.size(map_h['value']), lt.size(map_a['value'])


def req_4(control, nombre_torneo,fecha_inicial,fecha_final):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    r = []
    control_r = control['torneo']
    control_t = control['tiros']
    map = mp.get(control_r, nombre_torneo)
    lista = me.getValue(map)
    quk.sort(lista,compareDates)  

    for i in lista['elements']:
        if int(i['date'][:4]) == int(fecha_inicial[:4]) and int(i['date'][:4]) == int(fecha_final[:4]):
            if int(i['date'][5:7]) == int(fecha_inicial[5:7]) and int(i['date'][5:7]) == int(fecha_final[5:7]):
                if int(i['date'][8:10]) >= int(fecha_inicial[8:10]) and int(i['date'][8:10]) <= int(fecha_final[8:10]):
                        r.append(i)
            elif int(i['date'][5:7]) >= int(fecha_inicial[5:7]) and int(i['date'][5:7]) <= int(fecha_final[5:7]):
                        r.append(i)
        elif int(i['date'][:4]) >= int(fecha_inicial[:4]) and int(i['date'][:4]) <= int(fecha_final[:4]):
                        r.append(i)
    
    for e in r:
        for fila in control_t['elements']:
            if e['date'] == fila['date'] and (e['home_team'] == fila['home_team'] or e['away_team'] == fila['away_team']) :
                e['winner'] = fila['winner']
        if "winner" not in e.keys():
            e['winner'] = "Desconocido"

    return r
    


def req_5(control,nombre_jugador,fecha_inicial,fecha_final):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    r=[]
    controlg=control["goleadores_m"]
    controlr=control["resultados"]
    map = mp.get(controlg, nombre_jugador)
    lista = me.getValue(map)
    quk.sort(lista,compareDates) 
    for i in lista["elements"]:
        if int(i['date'][:4]) == int(fecha_inicial[:4]) and int(i['date'][:4]) == int(fecha_final[:4]):
            if int(i['date'][5:7]) == int(fecha_inicial[5:7]) and int(i['date'][5:7]) == int(fecha_final[5:7]):
                if int(i['date'][8:10]) >= int(fecha_inicial[8:10]) and int(i['date'][8:10]) <= int(fecha_final[8:10]):
                        r.append(i)
            elif int(i['date'][5:7]) >= int(fecha_inicial[5:7]) and int(i['date'][5:7]) <= int(fecha_final[5:7]):
                        r.append(i)
        elif int(i['date'][:4]) >= int(fecha_inicial[:4]) and int(i['date'][:4]) <= int(fecha_final[:4]):
                        r.append(i)
    for e in r:
        for fila in lt.iterator(controlr):
            if e['date'] == fila['date'] and (e['home_team'] == fila['home_team'] or e['away_team'] == fila['away_team']) :
                e['tournament'] = fila['tournament']
                e['home_score'] = fila['home_score']
                e['away_score'] = fila['away_score']

    return r

    
    

def req_6(control, nombre_torneo, anio):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    control_t = control['torneo']
    control_r = control['resultados']
    control_g = control['goleadores']
    control_ti = control['tiros']

    respuesta = lt.newList("ARRAY_LIST")
    equipos = lt.newList("ARRAY_LIST")
    paises = lt.newList("ARRAY_LIST")
    ciudades = {}
    total_equipos = lt.newList("ARRAY_LIST")

    lista = mp.get(control_t, nombre_torneo)
    torneo = me.getValue(lista)
    
    for i in lt.iterator(torneo):
        if int(i['date'][:4]) == anio:
            lt.addLast(respuesta,i)
    
    for e in lt.iterator(respuesta):
        for fila in lt.iterator(control_ti):
            if e['date'] == fila['date'] and (e['home_team'] == fila['home_team'] or e['away_team'] == fila['away_team']) :
                e['winner'] = fila['winner']
        if "winner" not in e.keys():
            e['winner'] = "Desconocido"

    for e in lt.iterator(respuesta):
        for fila in lt.iterator(control_g):
            if e['date'] == fila['date'] and (e['home_team'] == fila['home_team'] or e['away_team'] == fila['away_team']) :
                e['team'] = fila['team']
                e['scorer'] = fila['scorer']
                e['minute'] = fila['minute']
                e['penalty'] = fila['penalty']
                e['own_goal'] = fila['own_goal']
        if "team" not in e.keys():
            e['team'] = "Desconocido"
        if "scorer" not in e.keys():
            e['scorer'] = "Desconocido"
        if "penalty" not in e.keys():
            e['penalty'] = "Desconocido"
        if "own_goal" not in e.keys():
            e['own_goal'] = "Desconocido"
    
    total_anios, total_torneos = calcule_totales(lt.iterator(control_r), anio)
    
    for elemento in lt.iterator(respuesta):
        equipo = elemento['home_team']
        if equipo not in equipos['elements']:
            lt.addLast(equipos,equipo)
        equipo = elemento['away_team']
        if equipo not in equipos['elements']:
            lt.addLast(equipos,equipo)
        pais = elemento['country']
        if pais not in paises['elements']:
            lt.addLast(paises,pais)
        
        ciudad = elemento['city']
        if ciudad not in ciudades:
            ciudades[ciudad] = 1
        else:
            ciudades[ciudad] += 1
    
    ocurrencias_maximas = 0
    
    for ciudad, ocurrencias in ciudades.items():
        if ocurrencias > ocurrencias_maximas:
            ciudad_comun = ciudad
            ocurrencias_maximas = ocurrencias
    
    for team in lt.iterator(equipos):
         lt.addLast(total_equipos,iberibe_req_6(team, respuesta))
    
    

    respuesta_general = {'Total años del historial ': total_anios,
                         'Total torneos en el año seleccionado ':total_torneos,
                         'Total equipos del torneo ': equipos['size'],
                         'Total encuentros disputados ': respuesta['size'],
                         'Total paises involucrados ': paises['size'],
                         'Total ciudades involucradas ': len(ciudades),
                         'Ciudad con mas partidos ': ciudad_comun
                        }
    
    return respuesta_general, lt.iterator(total_equipos)

def iberibe_req_6(equipo, lista):
    
    # Datos en Results discriminados

    goles_hechos = 0
    goles_recibidos = 0
    autogoles_away = 0
    ganado_por_penalty = 0

    partidos_jugados = 0
    partidos_ganados = 0
    partidos_empatados = 0
    partidos_perdidos = 0

    jugadores = lt.newList('ARRAY_LIST')
    # calcula los datos anteriores 
    for p in lt.iterator(lista):
         home_n = str(p["home_team"])
         away_n = str(p["away_team"])
         home_p = int(p["home_score"])
         away_p = int(p["away_score"])

         if (home_n == equipo) or (away_n == equipo):
            partidos_jugados += 1

            if (home_n == equipo) and (home_p > away_p): 
                    partidos_ganados += 1
                    goles_hechos += home_p
                    goles_recibidos += away_p

            elif (away_n == equipo) and (home_p < away_p):
                    partidos_ganados += 1
                    goles_hechos += away_p
                    goles_recibidos += home_p

            elif home_p == away_p:
                 partidos_empatados += 1
                 goles_hechos += away_p
                 goles_recibidos += home_p

            elif (home_n == equipo) and (home_p < away_p):
                 partidos_perdidos += 1
                 goles_hechos += home_p
                 goles_recibidos += away_p

            elif (away_n == equipo) and (home_p > away_p):
                 partidos_perdidos += 1
                 goles_hechos += away_p
                 goles_recibidos += home_p
         
         if p['winner'] == equipo:
              ganado_por_penalty +=1

         if p['team'] == equipo:
            lt.addLast(jugadores, p['scorer'])


    fechas_part_jugador = lt.newList('ARRAY_LIST')
    num_partidos = 0
    suma_min = 0
    goles_totales = 0
    if not lt.isEmpty(jugadores):
        l = jugadores['elements']
        nombre_prominente = max(l, key = (l.count))
        for w in lt.iterator(lista):
           if nombre_prominente == w['scorer']:
              suma_min += float(w['minute'])
              if not lt.isPresent(fechas_part_jugador,w['date']):
                 lt.addLast(fechas_part_jugador,w['date'])
                 num_partidos += 1
              goles_totales += 1
    else:
        nombre_prominente = ""
    
    Promedio_tiempo = 0
    if goles_totales != 0:
        Promedio_tiempo = suma_min/goles_totales
    
    respuesta = {'Nombre equipo': equipo, 
                'Puntos totales': 3*partidos_ganados + (partidos_empatados),
                'Diferencia de goles': goles_hechos - goles_recibidos,
                'Partidos': partidos_jugados,
                'Puntos penalties': 3*ganado_por_penalty,
                'Puntos Autogol': autogoles_away,
                'Victorias': partidos_ganados,
                'Empates':partidos_empatados,
                'Derrotas': partidos_perdidos,
                'Goles Hechos': goles_hechos,
                'Goles Recibidos':goles_recibidos,
                'Mejor Jugador': {
                    'Nombre': nombre_prominente,
                    'Goles Jugador': goles_totales,
                    'Partidos con Gol':num_partidos,
                    'Promedio de Tiempo de Goles': Promedio_tiempo
                    }
            }
    return respuesta

def req_7(control, torneo, puntos):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    r = []
    lista_g = []
    lista_r = []
    lista_nombres = []

    control_r = control['torneo']
    map = mp.get(control_r, torneo)
    lista = me.getValue(map)
    

    control_g = control['goleadores']


    for fila in lista['elements']:
        for e in control_g['elements']:
            if fila['date'] == e['date'] and fila['home_team'] == e['home_team'] and fila['away_team'] == e['away_team']:
                lista_g.append(e)
                lista_r.append(fila)
    for i in lista_g:
        lista_nombres, r = iberibe_req_7(lista_nombres, r, i)
    
    for j in r:
        for g in lista_r:
            j['último_gol']['torneo'] = g['tournament']
            j['último_gol']['goles_local'] = g['home_score']
            j['último_gol']['goles_visitante'] = g['away_score']

            if g['home_team'] == j['team'] and j['fecha'] == g['date']:

                if g['home_score'] > g['away_score']:
                    j['anotaciones_v'] += 1
                elif g['home_score'] < g['away_score']:
                    j['anotaciones_p'] += 1
                elif g['home_score'] == g['away_score']:
                    j['anotaciones_e'] += 1

            if g['away_team'] == j['team'] and j['fecha'] == g['date']: 
                if g['home_score'] > g['away_score']:
                    j['anotaciones_v'] += 1
                elif g['home_score'] < g['away_score']:
                    j['anotaciones_p'] += 1
                elif g['home_score'] == g['away_score']:
                    j['anotaciones_e'] += 1

    return r

def iberibe_req_7(lista_nombres, lista, i):
    lista_n = lista_nombres
    listo = lista
    if i['scorer'] in lista_n:
        pos = lista_n.index(i['scorer'])
        dic_juagador = lista[pos]
        dic_juagador['puntos'] += 1
        dic_juagador['goles_totales'] += 1
        if i['penalty'] == 'True':
            dic_juagador['goles_penal'] += 1
            dic_juagador['puntos'] += 1
        if i['own_goal'] == 'True':
            dic_juagador['auto_goles'] += 1
            dic_juagador['puntos'] -= 1
        dic_juagador['tiempo_promedio'] = ((dic_juagador['tiempo_promedio']*(dic_juagador['goles_totales']-1)) + float(i['minute']))/dic_juagador['goles_totales']
    else: 
        dic = {
            'fecha':i['date'],
            'team':i['team'],
            'nombre':i['scorer'],
            'puntos': 1,
            'goles_totales': 1,
            'goles_penal' : 0,
            'auto_goles' : 0,
            'tiempo_promedio' : float(i['minute']),
            'torneo': 0,
            'anotaciones_v':0,
            'anotaciones_p':0,
            'anotaciones_e':0,
            'último_gol': {
                'fecha' : i['date'],
                'torneo': "",
                'local' : i['home_team'],
                'visitante' : i['away_team'],
                'goles_local': 0,
                'goles_visitante': 0,
                'minuto' : float(i['minute']),
                'penal' : i['penalty'],
                'auto_gol' : i['own_goal']
            }
        }
        if i['penalty'] == 'True':
            dic['goles_penal'] += 1
            dic['puntos'] += 1
        if i['own_goal'] == 'True':
            dic['auto_goles'] += 1
            dic['puntos'] -= 1
        listo.append(dic)
        lista_n.append(i['scorer'])
    return lista_n, listo


def req_8(control, pais, anio_i, anio_f):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    r = []
    lista = []
    control_1 = control['hteam']
    control_2 = control['ateam']
    control_g = control['goleadores']

    map1 = mp.get(control_1, pais)
    map2 = mp.get(control_2, pais)

    lista1 = me.getValue(map1)
    lista2 = me.getValue(map2)

    lista = lista1['elements'] + lista2['elements']
    lista_anios = []
    

    for i in lista:
        if int(i['date'][:4]) >= anio_i and int(i['date'][:4]) <= anio_f:
            lista_anios,r = iberibe_req_8(lista_anios, r,pais, i)

    for e in r:
        lista_goleadores = []
        for fila in control_g['elements']:
            if e['año'] == fila['date'][:4] and (e['local'] == fila['home_team'] and e['visitante'] == fila['away_team']):
                if fila['penalty']:
                    e['goles_penal'] += 1
                if fila['own_goal']:
                    e['auto_goles'] += 1

    return r
    
def iberibe_req_8(lista_anios, lista,nombre, i):
    lista_a = lista_anios
    listo = lista

    if int(i['date'][:4]) in lista_a:
        pos = lista_a.index(int(i['date'][:4]))
        dic_resultados = lista[pos]
        dic_resultados['partidos'] += 1
        if nombre == i['home_team']:
            if i['home_score'] > i['away_score']:
                dic_resultados['victorias'] += 1
                dic_resultados['puntos'] += 3
            elif i['home_score'] < i['away_score']:
                dic_resultados['derrotas'] += 1
            else:
                dic_resultados['empates'] += 1
                dic_resultados['puntos'] += 1
            dic_resultados['goles_favor'] += int(i['home_score'])
            dic_resultados['goles_contra'] += int(i['away_score'])
            dic_resultados['diferencia_goles'] += dic_resultados['goles_favor'] - dic_resultados['goles_contra']
        elif nombre == i['away_team']:
            if i['home_score'] > i['away_score']:
                dic_resultados['derrotas'] += 1
            elif i['home_score'] < i['away_score']:
                dic_resultados['victorias'] += 1
                dic_resultados['puntos'] += 3
            else:
                dic_resultados['empates'] += 1
                dic_resultados['puntos'] += 1
            dic_resultados['goles_favor'] += int(i['away_score'])
            dic_resultados['goles_contra'] += int(i['home_score'])
            dic_resultados['diferencia_goles'] += dic_resultados['goles_favor'] - dic_resultados['goles_contra']
    else:
        dic = {
            'año':i['date'][:4],
            'local':i['home_team'],
            'visitante':i['away_team'],
            'partidos': 1,
            'puntos': 0,
            'diferencia_goles': 0,
            'goles_penal' : 0,
            'auto_goles' : 0,
            'victorias':0,
            'derrotas':0,
            'empates':0,
            'goles_favor':0,
            'goles_contra':0,
            'goleador': {
                'nombre' : '',
                'goles': 0,
                'partidos' :0,
                'minuto' :0
            }
        }  
        if nombre == i['home_team']:
            if i['home_score'] > i['away_score']:
                dic['victorias'] += 1
                dic['puntos'] += 3
            elif i['home_score'] < i['away_score']:
                dic['derrotas'] += 1
            else:
                dic['empates'] += 1
                dic['puntos'] += 1
            dic['goles_favor'] += int(i['home_score'])
            dic['goles_contra'] += int(i['away_score'])
            dic['diferencia_goles'] += dic['goles_favor'] - dic['goles_contra']
        elif nombre == i['away_team']:
            if i['home_score'] > i['away_score']:
                dic['derrotas'] += 1
            elif i['home_score'] < i['away_score']:
                dic['victorias'] += 1
                dic['puntos'] += 3
            else:
                dic['empates'] += 1
                dic['puntos'] += 1
            dic['goles_favor'] += int(i['away_score'])
            dic['goles_contra'] += int(i['home_score'])
            dic['diferencia_goles'] += dic['goles_favor'] - dic['goles_contra']
        listo.append(dic)
        lista_a.append(int(i['date'][:4]))
    return lista_a, listo 

    




# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    if int(data_1['date'][:4]) == int(data_2['date'][:4]):
        if int(data_1['date'][5:7]) == int(data_2['date'][5:7]):
            return int(data_1['date'][8:10]) > int(data_2['date'][8:10])
        else:
            return int(data_1['date'][5:7]) > int(data_2['date'][5:7])
    else:
        return int(data_1['date'][:4]) > int(data_2['date'][:4])

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (type): description
        data2 (type): description

    Returns:
        type: description
    """
    #TODO: Crear función comparadora para ordenar
    return compare(data_1, data_2)


def sort(data_structs,s):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    if s == 1:

        data_structs['resultados'] = se.sort(data_structs['resultados'], sort_criteria)
        data_structs['goleadores'] = se.sort(data_structs['goleadores'], sort_criteria)
        data_structs['tiros'] = se.sort(data_structs['tiros'], sort_criteria)
        return data_structs
    elif s == 2:

        data_structs['resultados'] = ins.sort(data_structs['resultados'], sort_criteria)
        data_structs['goleadores'] = ins.sort(data_structs['goleadores'], sort_criteria)
        data_structs['tiros'] = ins.sort(data_structs['tiros'], sort_criteria)
        return data_structs
    elif s == 3:

        data_structs['resultados'] = sa.sort(data_structs['resultados'], sort_criteria)
        data_structs['goleadores'] = sa.sort(data_structs['goleadores'], sort_criteria)
        data_structs['tiros'] = sa.sort(data_structs['tiros'], sort_criteria)
        return data_structs
    elif s == 4:
        data_structs = sa.sort(data_structs,sort_criteria)
        return data_structs
    
def cmp_partidos_by_fecha_y_pais (resultado1, resultado2):
    """
    Devuelve verdadero (True) si la fecha del resultado1 es menor que en el resultado2,
    en caso de que sean iguales tenga el nombre de la ciudad en que se disputó el partido,
    de lo contrario devuelva falso (False).
    Args:
        Resultado1: información del primer registro de resultados FIFA que incluye
        “date” y el “country”
        impuesto2: información del segundo registro de resultados FIFA que incluye
        “date” y el “country”
    """
    if int(resultado1['date'][:4]) == int(resultado2['date'][:4]):
        if int(resultado1['date'][5:7]) == int(resultado2['date'][5:7]):
            if int(resultado1['date'][8:10]) == int(resultado2['date'][8:10]):
                return resultado1['city'][0] < resultado2['city'][0]
            else:
                return int(resultado1['date'][8:10]) < int(resultado2['date'][8:10])
        else:
            return int(resultado1['date'][5:7]) < int(resultado2['date'][5:7])
    else:
        return int(resultado1['date'][:4]) < int(resultado2['date'][:4])
    
def compareDates(dicc1,dicc2):
    fecha1 = dicc1["date"]
    fecha2 = dicc2["date"]
    if fecha1 < fecha2:
        return 0
    elif fecha1 > fecha2:
        return 1
    
def union(tabla1, tabla2):
    tabla_union = lt.newList('ARRAY_LIST')
    filtro = lt.newList('ARRAY_LIST')

    for llave, datos in tabla1.items():
        lt.addLast(tabla_union,datos)

    for llave, datos in tabla2.items():
        lt.addLast(tabla_union,datos)

    lt.deleteElement(tabla_union,1); lt.deleteElement(tabla_union,2)
    for f in lt.iterator(tabla_union):
        for j in lt.iterator(f):
            lt.addLast(filtro,j)
    a=0
    return filtro

def filtrar_fechas(filtro, fecha_inicial, fecha_final):
    respuesta_filtrada = lt.newList('ARRAY_LIST')
    fecha_inicial_dt = dt.datetime.strptime(fecha_inicial, "%Y-%m-%d")
    fecha_final_dt = dt.datetime.strptime(fecha_final, "%Y-%m-%d")

    for i in filtro:
        fecha_i_dt = dt.datetime.strptime(i['date'],"%Y-%m-%d")
        if fecha_inicial_dt <= fecha_i_dt and fecha_i_dt <= fecha_final_dt:
            lt.addLast(respuesta_filtrada, i)
    quk.sort(respuesta_filtrada, compareDates)

    return respuesta_filtrada

def calcule_totales(lista, anio):
    anios = []
    torneos_anio = []
    for elemento in lista:
        anio_lista = int(elemento['date'][:4])
        if anio_lista not in anios:
            anios.append(anio_lista)
        if anio_lista == anio:
            nom_torneo = elemento['tournament']
            if nom_torneo not in torneos_anio:
                torneos_anio.append(nom_torneo)
    return len(anios), len(torneos_anio)
