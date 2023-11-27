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
from datetime import datetime

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# ------------------------------ Construccion de modelos ------------------------------


def newCatalog(size,  map_type, loadFactor):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    
    catalog = {'partidos': None, 
               'partidos_1': None, 
               'goleadores' : None,
               'Merge_part_jug' : None,
               'individuales' : None,
               'penales': None, 
               'equipos': None, 
               'torneos': None, 
               'years' : None, 
               'golea_torneos': None, 
               'equipos_años':  None }
    
    catalog['partidos_1'] = lt.newList('ARRAY_LIST', cmp_dates)
    goleadores = lt.newList('ARRAY_LIST', cmp_dates)
    penales = lt.newList('ARRAY_LIST', cmp_dates)
    partidos_2 = lt.newList('ARRAY_LIST', cmp_dates)
    
    catalog['Merge_part_jug'] = lt.newList('ARRAY_LIST')
    
    
    catalog['partidos'] = mp.newMap(6, 
                                    maptype= map_type, 
                                    loadfactor= loadFactor)
    mp.put(catalog['partidos'], 'partidos', partidos_2)
    mp.put(catalog['partidos'], 'goleadores', goleadores)
    mp.put(catalog['partidos'], 'penales', penales)


    catalog['goleadores'] = mp.newMap(size,
                                      maptype = map_type,
                                      loadfactor = loadFactor)
    
    catalog['goleadores_simples'] = {'goleadores' : mp.newMap(size,
                                      maptype = map_type,
                                      loadfactor = loadFactor)}
    
    
    catalog['equipos'] = mp.newMap(size, 
                                   maptype= map_type, 
                                   loadfactor= loadFactor, 
                                   cmpfunction= cmp_Map_names)
        
    
    catalog['torneos'] = mp.newMap(size, 
                                   maptype= map_type, 
                                   loadfactor= loadFactor, 
                                   cmpfunction= cmp_Map_names)
    
    catalog['years'] = mp.newMap(size, 
                                maptype= map_type, 
                                loadfactor= loadFactor, 
                                cmpfunction= compare_map_year)
    
    catalog['golea_torneos'] = mp.newMap(size, 
                                maptype= map_type, 
                                loadfactor= loadFactor, 
                                cmpfunction= cmp_Map_names)
    
    catalog['equipos_años'] = mp.newMap(size, 
                                maptype= map_type, 
                                loadfactor= loadFactor, 
                                cmpfunction= compare_map_year)
    return catalog
    

# ------------------------------ Funciones para agregar informacion al modelo ------------------------------



###############
def add_partidos_1(catalog, element):
    """
    Función para agregar nuevos elementos a la lista
    """
    element['date'] = datetime.strptime(element['date'], '%Y-%m-%d').strftime('%Y-%m-%d')
    lt.addLast(catalog['partidos_1'], element)
    
    return catalog

def load_goleadores_penales_1(ginput_file): 
    goleadores = lt.newList('ARRAY_LIST')
    for element in ginput_file:
        add_element_1(goleadores, element)
        golea = element['scorer']
        
    return goleadores

def add_element_1(catalog, element):
    """
    Agrega un elemento al catalogo y mientras lo hace, cambia la fecha de string a datetime
    """
    element['date'] = datetime.strptime(element['date'], '%Y-%m-%d').strftime('%Y-%m-%d')
    
    lt.addLast(catalog, element)
    return catalog


def load_equ_tor(catalog):
    for valor in range(1, lt.size(catalog['Merge_part_jug']) + 1):
        element = lt.getElement(catalog['Merge_part_jug'], valor)
        add_map_golea(catalog, element)
    return catalog['goleadores']


def add_map_golea(catalog, element): 
   
    golea = catalog['goleadores']
    nombre_jug = element['scorer']
    existyear = mp.contains(golea, nombre_jug)

    if existyear:
            entry = mp.get(golea, nombre_jug)
            value = me.getValue(entry)
            if element['penalty'] == 'True':
              value['total_pen'] += 1

    else:
            value = new_jugador(nombre_jug)
            mp.put(golea, nombre_jug, value)
            if element['penalty'] == 'True':
              value['total_pen'] += 1

            
    lt.addLast(value['info'], element)
    merg.sort(value['info'], compareGoleadoresMenaMay)
    
def new_jugador(nombre_jug):
    """
    Esta funcion crea la estructura de partidos y otra informacion asociados
    a un jugador.
    """
    entry = {'scorer': "", "info": None, 'total_pen':0 }
    entry['scorer'] = nombre_jug
    entry['info'] = lt.newList('ARRAY_LIST', compareGoleadoresMenaMay)
    return entry

#############

def add_element(catalog, element, filename):
    """
    Agrega un elemento al catalogo y mientras lo hace, cambia la fecha de string a datetime
    """
    if filename == 'partidos': 
        element['date'] = datetime.strptime(element['date'], '%Y-%m-%d').strftime('%Y-%m-%d')
        element['home_score'] = int(element['home_score'])
        element['away_score'] = int(element['away_score'])
        element['neutral'] = castBoolean(element['neutral'])
        element['team'] = 'Unknown'
        element['scorer'] = 'Unknown'
        element['minute'] = 'Unknown'
        element['own_goal'] = 'Unknown'
        element['penalty'] = 'Unknown'
        element['winner'] = 'Unknown'
    elif filename == 'goleadores':
        element['date'] = datetime.strptime(element['date'], '%Y-%m-%d').strftime('%Y-%m-%d')
        element['home_score'] = 'Unknown'
        element['away_score'] = 'Unknown'
        element['neutral'] = 'Unknown'
        element['city'] = 'Unknown'
        element['country'] = 'Unknown'
    else: 
        element['date'] = datetime.strptime(element['date'], '%Y-%m-%d').strftime('%Y-%m-%d')
        
    
    lt.addLast(catalog, element)
    return catalog

def load_otros(catalog): 
    """
    Función para cargar las estructuras aparte de las 3 estructuras principales
    """
    for element in catalog['model']['partidos']['elements']:
        add_equipos(catalog['model'], element)
        add_torneos(catalog['model'], element)
        add_year(catalog['model'], element)
        add_torneo_goleadores(catalog['model'], element)
        add_year_team(catalog['model'], element)
    
    add_puntajes(catalog['model']['golea_torneos'])
    
        
    return catalog

def mergeFiles(catalog, partidos, goleadores, penales):
    """
    Función para la estructura que combina los 3 partidos.
    """
    partidos_final = lt.newList('ARRAY_LIST', cmpfunction=comparePartidos)

    file2_keys = {}
    file3_keys = {}
    goleadores_l = []
    
    for partido2 in lt.iterator(goleadores):
        llaves_iguales = (partido2['date'], partido2['home_team'], partido2['away_team'])
        file2_keys[llaves_iguales] = partido2
        if partido2['scorer'] not in goleadores_l: 
            goleadores_l.append(partido2['scorer'])
            
    catalog['tamanio'] = len(goleadores_l)
        

    for partido3 in lt.iterator(penales):
        llaves_iguales = (partido3['date'], partido3['home_team'], partido3['away_team'])
        file3_keys[llaves_iguales] = partido3
       
    
    for partido in lt.iterator(partidos):
        partido1 = partido.copy()
        llaves_iguales = (datetime.strptime(partido['date'], '%Y-%m-%d').strftime('%Y-%m-%d'), partido['home_team'], partido['away_team'])

        if llaves_iguales in file2_keys:
            
            partido2 = file2_keys[llaves_iguales]
            partido1['team'] = partido2['team']
            partido1['scorer'] = partido2['scorer']
            if partido2['minute'] != '': 
                partido1['minute'] = float(partido2['minute'])
            partido1['own_goal'] = castBoolean(partido2['own_goal'])
            partido1['penalty'] = castBoolean(partido2['penalty'])
        if llaves_iguales in file3_keys:
            partido3 = file3_keys[llaves_iguales]
            partido1['winner'] = partido3['winner']
        
        lt.addLast(partidos_final, partido1)
    return partidos_final 

def load_goleadores_penales(ginput_file): 
    goleadores = lt.newList('ARRAY_LIST')
    for element in ginput_file:
        add_element_1(goleadores, element)
    return goleadores

def mergeFiles2(partidos, goleadores):

    """
    Fucnión para la estructura que combina los 3 partidos. Toma el array de partidos como 
    referencia para completar las llaves que necesita
    """

    file2 = partidos
    partidos_final = lt.newList('ARRAY_LIST')

    file2_keys = {}
    
    for partido2 in lt.iterator(file2):
        llaves_iguales = (partido2['date'], partido2['home_team'], partido2['away_team'])
        file2_keys[llaves_iguales] = partido2

    
    for partido in lt.iterator(goleadores):
        partido1 = partido.copy()
        llaves_iguales = (partido['date'], partido['home_team'], partido['away_team'])
        
        if llaves_iguales in file2_keys:
            partido2 = file2_keys[llaves_iguales]
            partido1['tournament'] = partido2['tournament']
            partido1['home_score'] = partido2['home_score']
            partido1['away_score'] = partido2['away_score'] 
        
        lt.addLast(partidos_final, partido1)
    
    return merg.sort(partidos_final, compareGoleadoresMenaMay)
              
def add_equipos(catalog, element):
    """
    Agrega un elemento al mapa de equipos
    """ 
    team1 = element['home_team']
    team2 = element['away_team']
    
    #Agrega el equipo que esta como home
    existteam1 = mp.contains(catalog['equipos'], team1)
    
    if existteam1:
        entry1 = mp.get(catalog['equipos'], team1)
        value1 = me.getValue(entry1)
    else: 
        value1 = new_equipo(team1)
        mp.put(catalog['equipos'], team1, value1)
    
    local = mp.get(value1['partidos'], 'home')
    valor = me.getValue(local)
    lt.addLast(valor, element)
    value1['total_partidos'] +=1
    
    ind = mp.get(value1['partidos'], 'ind')
    valor2 = me.getValue(ind)
    lt.addLast(valor2, element)
    
    #Agrega el equipo que esta como away
    existteam2 = mp.contains(catalog['equipos'], team2)
    
    if existteam2:
        entry2 = mp.get(catalog['equipos'], team2)
        value2 = me.getValue(entry2)
    else: 
        value2 = new_equipo(team2)
        mp.put(catalog['equipos'], team2, value2)
    
    visit = mp.get(value2['partidos'], 'away')
    valor = me.getValue(visit)
    lt.addLast(valor, element)
    value2['total_partidos'] +=1
    
    ind2 = mp.get(value2['partidos'], 'ind')
    valor3 = me.getValue(ind2)
    lt.addLast(valor3, element)

def add_torneos(catalog, element): 
    """
    Agrega un elemento al mapa de torneos
    """ 
    torneo = element['tournament']
    
    existtorneo = mp.contains(catalog['torneos'], torneo)
    if existtorneo:
        entry = mp.get(catalog['torneos'], torneo)
        value = me.getValue(entry)
    else: 
        value = new_torneo(torneo)
        mp.put(catalog['torneos'], torneo, value)
    
    lt.addLast(value['partidos'], element)
    value['total_partidos'] +=1
   
    
def add_year(catalog, element):
    """
    Agrega un elemento al mapa de años
    """ 
    fecha = element['date']
    if type(fecha) == str: 
        year = fecha.split('-')[0]
    else:
        year = fecha.year
    
    existtorneo = mp.contains(catalog['years'], year)
    if existtorneo: 
        entry = mp.get(catalog['years'], year)
        value = me.getValue(entry)
    else: 
        value = new_year(year)
        mp.put(catalog['years'], year, value)
    
    #Agrega un mapa dentro de torneos dentro de cada año
    add_torneos_to_year(value, element)
    
    value['total_partidos'] +=1

def add_torneos_to_year(catalog, element): 
    """
    Agrega un elemento al mapa de torneos del mapa años 
    """ 
    torneo = element['tournament']
    
    existtorneo = mp.contains(catalog['torneos'], torneo)
    
    if existtorneo:
        entry = mp.get(catalog['torneos'], torneo)
        value = me.getValue(entry)
    else: 
        value = new_torneo_to_year(torneo)
        mp.put(catalog['torneos'], torneo, value)
    
    #Agrega un mapa dentro de equipos dentro de cada torneo
    add_equipos_to_year(value, element)
    
    value['total_torneos'] +=1
    
def add_equipos_to_year(catalog, element):
    """
    Agrega un elemento al mapa de equipos del mapa torneos
    del mapa años
    """  
    team1 = element['home_team']
    team2 = element['away_team']
    
    existteam1= mp.contains(catalog['equipos'], team1)
    existteam2 = mp.contains(catalog['equipos'], team2)
    
    if existteam1: 
        entry1 = mp.get(catalog['equipos'], team1)
        value1 = me.getValue(entry1)
    else: 
        value1 = lt.newList('ARRAY_LIST')
        mp.put(catalog['equipos'], team1, value1)
    
    lt.addLast(value1, element)
    
    
    if existteam2: 
        entry2 = mp.get(catalog['equipos'], team2)
        value2 = me.getValue(entry2)
    else: 
        value2 = lt.newList('ARRAY_LIST')
        mp.put(catalog['equipos'], team2, value2)
    
    lt.addLast(value2, element)
    
    
def add_torneo_goleadores(catalog, element): 
    """
    Agrega un elemento al mapa de torneos que contiene jugadores
    """     
    torneo = element['tournament']
     
    existtorneo = mp.contains(catalog['golea_torneos'], torneo)
    
    if existtorneo:
        entry = mp.get(catalog['golea_torneos'], torneo)
        value = me.getValue(entry)
    else: 
        value = new_torneo_to_goleadores(torneo)
        mp.put(catalog['golea_torneos'], torneo, value)
    
    #Agrega el mapa de goleadores dentro del torneo
    add_goleadores_torneo(value, element)
    
    value['total_partidos'] +=1
    
def add_goleadores_torneo(catalog, element): 
    """
    Agrega un elemento al mapa de goleadores de cada torneo
    """
    golea = catalog['jugadores']
    nombre_jug = element['scorer']
    
    existyear = mp.contains(golea, nombre_jug)
    if existyear:
        entry = mp.get(golea, nombre_jug)
        value = me.getValue(entry)
    else:
        value= lt.newList('ARRAY_LIST')
        mp.put(golea, nombre_jug, value)
        
    lt.addLast(value, element)

def add_puntajes(catalog):
    torneos = mp.keySet(catalog)
    for torneo in lt.iterator(torneos):
        #Se realiza la división de jugadores para todos los torneos
        entry_torneo = mp.get(catalog, torneo)
        jugadores = me.getValue(entry_torneo)
        lista_jugadores = mp.keySet(jugadores['jugadores'])
        for jugador in lt.iterator(lista_jugadores):
            #Con los jugadores del torneo se sacan los totales para crear una nueva llave 
            lista_jugador = mp.get(jugadores['jugadores'], jugador)
            lista_partidos = merg.sort(me.getValue(lista_jugador), cmp_dates)
            totales, puntaje = totales_por_jugador(jugador, lista_partidos)
            last_goal = lt.getElement(lista_partidos, 1)
            entry_last = mp.get(totales, 'last_goal')
            me.setValue(entry_last, last_goal)
            #Se crea un nuevo mapa que se diferencie por los puntajes obtenidos
            existjugador = mp.contains(jugadores['puntajes'], puntaje)
            if existjugador: 
                entry_value = mp.get(jugadores['puntajes'], puntaje)
                value = me.getValue(entry_value)
            else: 
                value = new_puntaje(puntaje)
                mp.put(jugadores['puntajes'], puntaje, value)
                
            mp.put(value['jugadores'], jugador, totales)
            
            
def add_team_mini_year(catalog, element):
    """
    Agrega un elemento al mapa de equipos del mapa de años
    """  
    if element['tournament'] != 'Friendly':
        team1 = element['home_team']
        team2 = element['away_team']
        
        existteam1= mp.contains(catalog['equipos'], team1)
        existteam2 = mp.contains(catalog['equipos'], team2)
        
        if existteam1: 
            entry1 = mp.get(catalog['equipos'], team1)
            value1 = me.getValue(entry1)
        else: 
            value1 = new_equipo_mini(team1)
            mp.put(catalog['equipos'], team1, value1)
        
        value1['total_local'] += 1
        lt.addLast(value1['partidos'], element)
            
        
        if existteam2: 
            entry2 = mp.get(catalog['equipos'], team2)
            value2 = me.getValue(entry2)
        else: 
            value2 = new_equipo_mini(team2)
            mp.put(catalog['equipos'], team2, value2)
        
        value1['total_visitante'] += 1
        lt.addLast(value1['partidos'], element)
    
    
def add_year_team(catalog, element):
    """
    Agrega un elemento al mapa de años
    """ 
    fecha = element['date']
    if type(fecha) == str: 
        year = fecha.split('-')[0]
    else:
        year = fecha.year
    
    existtorneo = mp.contains(catalog['equipos_años'], year)
    if existtorneo: 
        entry = mp.get(catalog['equipos_años'], year)
        value = me.getValue(entry)
    else: 
        value = new_year_to_teams(year)
        mp.put(catalog['equipos_años'], year, value)
    
    #Agrega un mapa dentro de torneos dentro de cada año
    add_team_mini_year(value, element)
    
# ------------------------------ Funciones para creacion de datos ------------------------------

def new_jugador(nombre_jug):
    """
    Crea el valor para cada jugador con sus partidos
    """
    entry = {'scorer': "", "info": None, 'total_pen': 0}
    entry['scorer'] = nombre_jug
    entry['info'] = lt.newList('ARRAY_LIST', compareGoleadoresMenaMay)
    return entry

def new_equipo(equipo):
    """
    Crea el valor para cada equipo con sus partidos
    """    
    team = {'equipo' : equipo, 
            'partidos': None,
            'total_partidos': 0} 
    
    team['partidos'] = mp.newMap(3, 
                                 maptype= 'PROBING', 
                                 loadfactor= 0.5)
    
    mp.put(team['partidos'], 'home', lt.newList('ARRAY_LIST', cmpfunction= cmp_dates))
    mp.put(team['partidos'], 'away', lt.newList('ARRAY_LIST', cmpfunction= cmp_dates))
    mp.put(team['partidos'], 'ind', lt.newList('ARRAY_LIST', cmpfunction= compare_points))
    return team    

def new_torneo(torneo): 
    """
    Crea el valor para cada torneo con sus partidos
    """
    tournament =  {'torneo' : torneo,
                   'partidos': None, 
                   'total_partidos': 0}
    
    tournament['partidos'] = lt.newList('ARRAY_LIST', cmp_dates)
    return tournament

def new_year(year):
    """
    Crea el valor para cada año
    """ 
    anio = {'anio': int(year), 
            'torneos': None,
            'total_partidos': 0}
    
    anio['torneos'] = mp.newMap(80,
                                maptype= 'PROBING', 
                                loadfactor= 0.5, 
                                cmpfunction= cmp_Map_names)
    return anio

def new_torneo_to_year(torneo): 
    """
    Crea el valor para cada torneo de cada año con su mapa de 
    equipos
    """
    tournament =  {'torneo' : torneo,
                   'equipos': None, 
                   'total_torneos': 0}
    tournament['equipos'] = mp.newMap(83, 
                                      maptype= 'PROBING', 
                                      loadfactor= 0.5, 
                                      cmpfunction= cmp_Map_names)
    return tournament

def new_equipo_to_year(equipo):
    """
    Crea el valor para cada equipo de cada año como una lista
    """
    team =  lt.newList('ARRAY_LIST')
    return team

def new_puntaje(puntaje): 
    points = {'puntaje': puntaje, 
              'jugadores': None}
    points['jugadores'] = mp.newMap(83, 
                          maptype='PROBING', 
                          loadfactor= 0.7)

    return points

def new_torneo_to_goleadores(torneo):
    """
    Crea el valor para cada torneo con su mapa de 
    jugadores
    """
    tournament = { 'torneo': torneo, 
                    'jugadores': None,
                    'puntajes': None, 
                    'total_partidos': 0}
    
    tournament['jugadores'] = mp.newMap(83, 
                                      maptype= 'PROBING', 
                                      loadfactor= 0.5, 
                                      cmpfunction= cmp_Map_names)
    tournament['puntajes'] = mp.newMap(83, 
                                      maptype= 'PROBING', 
                                      loadfactor= 0.5, 
                                      cmpfunction= cmp_Map_names)
    return tournament

def new_year_to_teams(anio): 
    year = { 'year': anio, 
            'equipos': None, 
            'tota_partidos': 0}
    
    year['equipos'] = mp.newMap(83,
                                maptype='PROBING', 
                                loadfactor= 0.7)
    year['tota_partidos'] +=1
    return year

def new_equipo_mini(equipo): 
    
    team = {'equipo': equipo, 
            'partidos': None, 
            'total_partidos': 0, 
            'total_local': 0, 
            'total_visitante': 0}
    team['partidos'] = lt.newList('ARRAY_LIST', cmp_dates)
    team['total_partidos'] +=1
    return team
# ------------------------------ Funciones de consulta ------------------------------

def get_timeframe(list_partidos, date1, date2):
    """
    Función que toma una lista y un rango de fechas y retorna una sublista
    que se encuentre en el rango de fechas con los totales de esa lista
    """
    
    timeframe = lt.newList('ARRAY_LIST', cmpfunction=cmp_dates)
    #Mapa que cuenta con los totales de la lista. 
    resultados = mp.newMap(5, 
                       maptype='PROBING',
                       loadfactor= 0.5)

    mp.put(resultados, 'total_matches', 0)
    mp.put(resultados, 'total_own_goals', 0 )
    mp.put(resultados, 'total_country', lt.newList('ARRAY_LIST') )
    mp.put(resultados, 'total_cities',  lt.newList('ARRAY_LIST'))
    mp.put(resultados, 'total_winners', lt.newList('ARRAY_LIST') )
    mp.put(resultados, 'total_teams', lt.newList('ARRAY_LIST') )
    
    for partido in lt.iterator(list_partidos):
        if date1 <= datetime.strptime(partido['date'], '%Y-%m-%d').strftime('%Y-%m-%d')<= date2:
            #Luego de la verificación se el partido se almacena dentro de una lista y se sacan todos los totales necesarios
            lt.addLast(timeframe, partido)
            matches = mp.get(resultados, 'total_matches')
            total_matches = me.getValue(matches) + 1
            me.setValue(matches, total_matches)
            
            if partido['own_goal']:
                own = mp.get(resultados, 'total_matches')
                total_own_goals = me.getValue(own) + 1
                me.setValue(own, total_own_goals)
           
            country = mp.get(resultados, 'total_country')
            countries = me.getValue(country)
            if not lt.isPresent(countries, partido['country']):
                lt.addLast(countries, partido['country'])

            city = mp.get(resultados, 'total_cities')
            cities = me.getValue(city)
            if not lt.isPresent(cities, partido['city']):
                lt.addLast(cities, partido['city'])

            winner = mp.get(resultados, 'total_winners')
            winners = me.getValue(winner)
            if not lt.isPresent(winners, partido['winner']) and partido['winner'] != 'Unknown':
                lt.addLast(winners, partido['winner'])

            team = mp.get(resultados, 'total_teams')
            teams = me.getValue(team)
            if not lt.isPresent(teams, partido['home_team']):
                lt.addLast(teams, partido['home_team'])

            if not lt.isPresent(teams, partido['away_team']): 
                lt.addLast(teams, partido['away_team'])
    
    #Retorna una lista ordenada junto con el mapa con todos los totales
    # timeframe = merg.sort(timeframe, compare_date_name_city)
    return timeframe, resultados


def totales_por_equipos(equipo, entry_equipo, total_paises, total_ciudades, total_encuentros):
    """
    Función que toma un equipo, una pareja llave valor, un ARRAY de paises y un diccionario
    de ciudades y retorna un mapa de los totales, y el ARRAY y el diccionario con nuevos datos.  
    """
    partidos = me.getValue(entry_equipo)
    totales = mp.newMap(10, 
                        maptype='PROBING',
                        loadfactor=0.5)
    #Agrega las diferentes llaves de los totales del equipo
    mp.put(totales, 'equipo', equipo )
    mp.put(totales, 'total_puntos_obtenidos', 0)
    mp.put(totales, 'diferencia_goles', 0)
    mp.put(totales, 'total_partidos', 0)
    mp.put(totales, 'total_linea_penal', 0)
    mp.put(totales, 'total_autogol', 0)
    mp.put(totales, 'total_victorias', 0)
    mp.put(totales, 'total_empates', 0)
    mp.put(totales, 'total_derrotas', 0)
    mp.put(totales, 'total_goles', 0)
    mp.put(totales, 'total_goles_recibidos', 0)
    mp.put(totales, 'mejor_jugador', None)

    
    for match in lt.iterator(partidos):
        #Se realizan los totales para todos los partidos
        total_encuentros+= 1
        if equipo == match['home_team']: 
            valor_equipo = match['home_score']
            valor_opuesto = match['away_score']
        else: 
            valor_equipo = match['away_score']
            valor_opuesto = match['home_score']
        
        total_puntos_obtenidos = mp.get(totales, 'total_puntos_obtenidos')
        total_victorias = mp.get(totales, 'total_victorias')
        total_empates = mp.get(totales, 'total_empates')
        total_derrotas = mp.get(totales, 'total_derrotas')

        puntos_obtenidos = me.getValue(total_puntos_obtenidos)
        victorias = me.getValue(total_victorias)
        empates = me.getValue(total_empates)
        derrotas = me.getValue(total_derrotas)

        if valor_equipo > valor_opuesto:
            puntos_obtenidos += 3
            me.setValue(total_puntos_obtenidos, puntos_obtenidos)
            victorias += 1
            me.setValue(total_victorias, victorias)
        elif valor_equipo == valor_opuesto:
            puntos_obtenidos += 1
            me.setValue(total_puntos_obtenidos, puntos_obtenidos)
            empates += 1
            me.setValue(total_empates, empates)
        else:
            derrotas += 1
            me.setValue(total_derrotas, derrotas)

        total_goles = mp.get(totales, 'total_goles')
        goles_marcados = me.getValue(total_goles)
        goles_marcados += valor_equipo
        me.setValue(total_goles, goles_marcados)

        total_goles_recibidos = mp.get(totales, 'total_goles_recibidos')
        goles_recibidos = me.getValue(total_goles_recibidos)
        goles_recibidos += valor_opuesto
        me.setValue(total_goles_recibidos, goles_recibidos)

        diferencia_goles =abs(goles_marcados - goles_recibidos)
        total_diferencia_goles = mp.get(totales, 'diferencia_goles')
        me.setValue(total_diferencia_goles, diferencia_goles)

        total_partidos = mp.get(totales, 'total_partidos')
        partidos_jugados = me.getValue(total_partidos)
        partidos_jugados += 1
        me.setValue(total_partidos, partidos_jugados)

        if match['penalty'] != False and match['penalty'] != 'Unknown' :
            total_linea_penal = mp.get(totales, 'total_linea_penal')
            lineas_penales = me.getValue(total_linea_penal)
            lineas_penales += 1
            me.setValue(total_linea_penal, lineas_penales)

        if match['own_goal']:
            total_autogol = mp.get(totales, 'total_autogol')
            autogoles = me.getValue(total_autogol)
            autogoles += 1
            me.setValue(total_autogol, autogoles)
            
        ranking_jugadores = {}
        #Para el ranking de jugadores, se almacenan todos los jugadores dentro de un diccionario con sus resultados para compararlos
        if match['scorer'] != 'Unknown' and equipo == match['team'] :
            jugador = match['scorer']
            if jugador not in ranking_jugadores :
                ranking_jugadores[jugador] = {'scorer': match['scorer'], 'goles': 1, 'partidos': [match['date']], 'tiempo': float(match['minute'])}
            else:
                ranking_jugadores[jugador]['goles'] += 1
                ranking_jugadores[jugador]['partidos'].append(match['date'])
                ranking_jugadores[jugador]['tiempo'] += float(match['minute'])

            mejor_jugador_key = mp.get(totales, 'mejor_jugador')
        
            max_jugador = max(ranking_jugadores, key=lambda jugador: ranking_jugadores[jugador]['goles'])
            mejor_jugador = ranking_jugadores[max_jugador]
            mejor_jugador['tiempo'] = float(mejor_jugador['tiempo']/  mejor_jugador['goles'])
            me.setValue(mejor_jugador_key, mejor_jugador)
        else: 
            mejor_jugador = {'scorer': 'Unavailable', 'goles': 0, 'partidos': 0, 'tiempo': 0.0}
            mejor_jugador_key = mp.get(totales, 'mejor_jugador')
            me.setValue(mejor_jugador_key, mejor_jugador)
            

        if not lt.isPresent(total_paises, match['country']):
            lt.addLast(total_paises, match['country'])
        
        if match['city'] not in total_ciudades:
            total_ciudades[match['city']] = 0
            total_ciudades['total']+=1
        else:
            total_ciudades[match['city']] += 1
        
    return totales, total_paises, total_ciudades, total_encuentros

def totales_por_jugador(jugador, lista_partidos):
    totales = mp.newMap(10, 
                        maptype='PROBING',
                        loadfactor=0.5)
    
    #agrega las diferentes llaves de los totales del jugador
    mp.put(totales, 'jugador', jugador  )
    mp.put(totales, 'total_points', 0)
    mp.put(totales, 'total_goals', 0)
    mp.put(totales, 'penalty_goals', 0)
    mp.put(totales, 'own_goals', 0)
    mp.put(totales, 'avg_time', 0.0)
    mp.put(totales, 'scored_in_wins', 0)
    mp.put(totales, 'scored_in_loses', 0)
    mp.put(totales, 'scored_in_draws', 0)
    mp.put(totales, 'last_goal', None)
    
    for match in lt.iterator(lista_partidos): 
        if match['scorer'] != 'Unknown':
            #Se realizan los totales para cada jugador existente 
            if match['penalty']: 
                penalty_goals = mp.get(totales, 'penalty_goals')
                penalty = me.getValue(penalty_goals)
                penalty += 1
                me.setValue(penalty_goals, penalty)
                
            if match['own_goal']: 
                own_goals = mp.get(totales, 'own_goals')
                own_goal = me.getValue(own_goals)
                own_goal += 1
                me.setValue(own_goals, own_goal) 
                
            if match['minute'] != 'Unknown':
                avg_time = mp.get(totales, 'avg_time')
                time = me.getValue(avg_time)
                time += match['minute']
                me.setValue(avg_time, time)
            
            wins = mp.get(totales, 'scored_in_wins')
            scored_in_wins = me.getValue(wins)
            
            loses = mp.get(totales, 'scored_in_loses' )
            scored_in_loses = me.getValue(loses)
            
            draws = mp.get(totales, 'scored_in_draws')
            scored_in_draws = me.getValue(draws)
                    
            if match['home_team'] == match['team']: 
                if match['home_score'] > match['away_score']:
                    scored_in_wins += 1
                    me.setValue(wins, scored_in_wins)
                elif match['away_score'] > match['home_score']: 
                    scored_in_loses += 1
                    me.setValue(loses, scored_in_loses)
                elif match['home_score'] == match['away_score']:
                    scored_in_draws += 1
                    me.setValue(draws, scored_in_draws)
            else:
                if match['away_score'] > match['home_score']:
                    scored_in_wins += 1
                    me.setValue(wins, scored_in_wins)
                elif match['home_score'] > match['away_score']: 
                    scored_in_loses += 1
                    me.setValue(loses, scored_in_loses)
                elif match['home_score'] == match['away_score']:
                    scored_in_draws += 1
                    me.setValue(draws, scored_in_draws)
        
        entry_goals = mp.get(totales, 'total_goals')
        total_goals = me.getValue(entry_goals)
        total_goals += me.getValue(mp.get(totales, 'scored_in_wins'))
        total_goals += me.getValue(mp.get(totales, 'scored_in_loses'))
        total_goals += me.getValue(mp.get(totales, 'scored_in_draws'))
        me.setValue(entry_goals, total_goals)
                
        entry_points = mp.get(totales, 'total_points')
        total_points = me.getValue(entry_points)
        total_points+= me.getValue(mp.get(totales, 'total_goals'))    
        if match['penalty']:
            total_points += me.getValue(mp.get(totales, 'penalty_goals'))
        if match['own_goal']: 
            total_points-= me.getValue(mp.get(totales, 'own_goals'))
        me.setValue(entry_points, total_points)
        

        entry_time = mp.get(totales, 'avg_time')
        time = me.getValue(entry_time)
        if time != 0.0:
            time /= me.getValue(mp.get(totales, 'total_goals'))
        me.setValue(entry_time, round(float(time), 1))
    
    return totales, total_points    
    

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

# ------------------------------ REQUERIMIENTOS ------------------------------

def req_1(catalog, n, equipo, condicion):
    """ 
    Función para obtener los ultimos N partidos jugados por un equipo según su condición

    Args:
        catalog (dict): Catálogo con todas las estructuras que organizan la información de partidos
        n (int): El número de N partidos a consultar
        equipo (str): Nombre del equipo a consultar
        condicion (str): Condición del equipo a consultar 

    Returns:
        lista_partidos (ARRAY_LIST): La lista ordenada de los partidos que jugó el equipo con la condición
        totales (tuple): Tupla que cuenta con el número de equipos y el número de partidos
    """
    equipos = catalog['equipos']
    equipo_buscado = mp.get(equipos, equipo)
    part = me.getValue(equipo_buscado)
    condicion_n = mp.get(part['partidos'], condicion)
    #Se obtienen los partidos como un single_linked el cual se organizará 
    lista_partidos = me.getValue(condicion_n)
    totales = (mp.size(equipos), part['total_partidos'], lt.size(lista_partidos))
    #Sacamos la sublista y la comparamos según los criterios
    lista_partidos= merg.sort(lista_partidos, comparePartidos)
    if n > lt.size(lista_partidos): 
        sub_lista = lista_partidos
    else:
        sub_lista = lt.subList(lista_partidos, 1, n)
    return (sub_lista, totales)


def req_2(catalog, goleador_nom, n):
    """
    Función para obtener los primeros N goles anotados por un jugador especifico

    Args:
        catalog (dict): Catálogo con todas las estructuras que organizan la información de partidos
        goleador_nom (str): Nombre del goleador a consultar
        n (int): El número de n goles anotados por el jugador

    Returns:
        resultado (ARRAY_LIST): La lista de los top partidos de ese jugador 
        suma (int): El número total de jugadores 
        total (int): El número total de partidos
        penal (int): El número total de penales
    """
    
    jugadores = catalog['goleadores']
    suma = mp.size(jugadores)
    #total de jugadores = size del mapa 
    jugador_seleccionado = mp.get(jugadores, goleador_nom)
    if jugador_seleccionado:
        partidos = me.getValue(jugador_seleccionado)['info'] 
        
    total = lt.size(partidos)
     
    if n >= total:
        resultado = lt.subList(partidos, 1, total)
    else:
        resultado = lt.subList(partidos, 1, n)
    
    penal = me.getValue(jugador_seleccionado)['total_pen']
    return resultado, suma, total, penal


def req_3(catalog, equipo, fi, ff):
    """
    Función para obtener los partidos que disputo un equipo utilizando su nombre
    y un periodo entre dos fechas especificadas

    Args:
        catalog (dict): Catálogo con todas las estructuras que organizan la información de partidos
        equipo (str):  Nombre del equipo a consultar
        fecha_i (datetime): Fecha inicial para la búsqueda
        fecha_f (datetime): Fecha final para la búsqueda

    Returns:
       final (ARRAY_LIST): La lista con los partidos que disputó el equipo
    """
    
    partidos = catalog['partidos']
    equipos = catalog['equipos']
    total_equ= mp.size(equipos)
    lista = lt.newList("ARRAY_LIST")
    home_games=0
    away_games=0
    for partido in lt.iterator(partidos):
            fecha= partido['date']
            if partido['home_team'] == equipo and fi<=fecha<=ff:
                lt.addLast(lista, partido)
                home_games+=1
            elif partido['away_team'] == equipo and fi<=fecha<=ff:
                lt.addLast(lista, partido)
                away_games+=1    
    numero_par = lt.size(lista)
    lista = merg.sort(lista, comparePartidos)
    return lista, numero_par, home_games, away_games,total_equ
    
    

def req_4(catalog, torneo, fecha_i, fecha_f):
    """
    Función para obtener los partidos relacionados con un torneo utilizando
    su nombre y un periodo entre dos fechas especificadas.

    Args:
        catalog (dict): Catálogo con todas las estructuras que organizan la información de partidos
        torneo (str): _description_
        fecha_i (datetime): Fecha inicial para la búsqueda
        fecha_f (datetime): Fecha final para la búsqueda

    Returns:
        torneo_ff (ARRAY_LIST): Una lista ordenada de los partidos del torneo en el periodo de tiempo
        totals (map): Un mapa con todos generales de los partidos
    """
    torneos = catalog['torneos']
    total_torneos = mp.size(torneos)
    torneo_buscado = mp.get(torneos, torneo)
    lista = me.getValue(torneo_buscado)
    #Con la lista de partidos, hallamos los partidos que se encuentran en ese periodo y sus totales
    torneo_ff, totals = get_timeframe(lista['partidos'], fecha_i, fecha_f)
    mp.put(totals, 'total_torneos', total_torneos)
    
    return merg.sort(torneo_ff, compare_date_name_city), totals


def req_5(catalog, goleador_nom, fecha_i, fecha_f):
    """
    Función que soluciona el requerimiento 5
    """
    jugadores = catalog['goleadores']
    penalty = 0
    auto = 0
    torneos = lt.newList('ARRAY_LIST')
    suma = mp.size(jugadores)
    jugador_seleccionado = mp.get(jugadores, goleador_nom)
    lista = lt.newList('SINGLE_LINKED')
    if jugador_seleccionado:
        partidos = me.getValue(jugador_seleccionado)['info']  
        for valor in range(1, lt.size(partidos) + 1):
            golea = lt.getElement(partidos, valor)
            if fecha_i <= golea['date'] <= fecha_f:
                lt.addFirst(lista, golea)
            if golea['penalty'] == 'True':
                penalty += 1
            if golea['own_goal'] == 'True':
                auto += 1
            if lt.isPresent(torneos, golea['tournament']) == 0:
                lt.addLast(torneos, golea['tournament'])
                
    total_torneos = lt.size(torneos)
                
    total = lt.size(partidos)

    return lista, suma, total, total_torneos, penalty,auto


def req_6(catalog, n, torneo, year):
    """
    Función para obtener los N mejores equipos de una liga o torneo dentro de un periodo de 
    tiempo. Esto puede entenderse como el TOP ranking de cierta cantidad de equipos en el torneo

    Args:
        catalog (dict): Catálogo con todas las estructuras que organizan la información de partidos
        n (int): El número de equipos a consultar
        torneo (str): El torneo de búsqueda 
        year (int): El año de búsqueda

    Returns:
       equipo_list ('ARRAY_LIST): La lista ordenada de los N equipos con sus totales del torneo dentro del año
       totales (map): Un mapa con todos generales de los partidos 
    """
    
    #Se va sacando totales generales según el tamaño del mapa
    total_years = mp.size(catalog['years'])
    entry = mp.get(catalog['years'], str(year))
    año = me.getValue(entry)
    total_matches= año['total_partidos']
    
    total_torneos = mp.size(año['torneos'])
    entry_torneo = mp.get(año['torneos'], torneo)
    torneos = me.getValue(entry_torneo)
    total_equipos = mp.size(torneos['equipos'])
    #Se obtiene todos los equipos que se encuentran con las especificaciones 
    equipos = mp.keySet(torneos['equipos'])
    total_encuentros = 0
    total_paises = lt.newList('ARRAY_LIST')
    total_ciudades = {'total':0}
    equipo_list = lt.newList('ARRAY_LIST')
    
    for equipo in lt.iterator(equipos):
        #Se itera cada equipo para hallar los totales de este dentro del mapa
        entryeq = mp.get(torneos['equipos'], equipo)
        totales_equipo, total_paises, total_ciudades, total_encuentros= totales_por_equipos(equipo, entryeq, total_paises, total_ciudades, total_encuentros)
        lt.addLast(equipo_list, totales_equipo)
    
    #Los partidos se ordenan segun puntos dentro de la lista
    merg.sort(equipo_list, compare_points)
    if n< lt.size(equipo_list): 
        equipo_list = lt.subList(equipo_list, 1, n)
    
    
    total_country = lt.size(total_paises)
    total_cities = total_ciudades['total']
    del total_ciudades['total']
    mayor_ciudad = max(total_ciudades, key=total_ciudades.get)
    #Se completan los totales
    
    totales_generales =(total_years, total_torneos, total_equipos, total_matches, total_country, total_cities, mayor_ciudad)
    
   
    return equipo_list, totales_generales
        
    
        
def req_7(catalog, torneo, n):
    """
    Función para obtener los jugadores de futbol con N puntos dentro de una competencia especifica.

    Args:
        catalog (dict): Catálogo con todas las estructuras que organizan la información de partidos
        torneo (srt): El torneo de búsqueda 
        n (int): El puntaje que deben tener los goleadores

    Returns:
        lista_totales_jugadores (ARRAY_LIST): La lista con los totales de los jugadores con los n puntos del torneo
        totales_generales (tuple): La tupla contiene todos los totales generales de los partidos 
    """
    #Se sacan totales generales según el tamaño del mapa
    total_torneos = mp.size(catalog['golea_torneos'])
    entry_torneo = mp.get(catalog['golea_torneos'], torneo)
    total_goleadores = mp.size(catalog['golea_torneos'])
    torneo_pair = me.getValue(entry_torneo)
    #Se toman los partidos con el puntaje seleccionado
    map_puntaje = torneo_pair['puntajes']
    puntaje = mp.get(map_puntaje, n)
    jugadores = me.getValue(puntaje)
    map_jugadores = jugadores['jugadores']
    #Se completan totales
    total_jugadores_torneo = mp.size(map_jugadores)
    lista_jugadores = mp.keySet(map_jugadores)
    lista_totales_jugadores = lt.newList('ARRAY_LIST')
    total_goles = 0
    total_penal = 0
    total_autogoles = 0
    for jugador in lt.iterator(lista_jugadores): 
        #Por cada jugadorse hallan y almacenan los totales individuales  
        totales_jug = me.getValue(mp.get(map_jugadores, jugador))
        lt.addLast(lista_totales_jugadores, totales_jug)
        #Se hallan más totales generales
        jug_total_goles = me.getValue(mp.get(totales_jug, 'total_goals'))
        jug_total_penal = me.getValue(mp.get(totales_jug, 'penalty_goals'))
        jug_total_autogoles = me.getValue(mp.get(totales_jug, 'own_goals'))
        total_goles += jug_total_goles
        total_penal += jug_total_penal
        total_autogoles += jug_total_autogoles
    lista_provicional = merg.sort(lista_totales_jugadores, compare_points_jug)
    totales_generales = (total_torneos, total_goleadores, total_jugadores_torneo,
                         total_goles, total_penal, total_autogoles)
    return lista_totales_jugadores, totales_generales
    

def req_8(catalog, equipo, fecha_i, fecha_f):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    


# ------------------------------Funciones utilizadas para comparar elementos dentro de una lista ------------------------------
def compare_map_year(year, partido):
    """
    Función cmp que organiza los años otorgados en el mapa
    """
    yearentry = me.getKey(partido)
    if year > yearentry: 
        return 1
    elif year < yearentry: 
        return -1
    else:
        return 0
    
    
def comparePartidos(partido1, partido2 ): 
    """
    cmp que compara los 2 partidos según su fecha, si son iguales, se guia por el pais.
    """
    if partido1['date']== partido2['date']: 
        return  ((partido1["country"]) > (partido2["country"]))
    else: 
        return partido1['date'] > partido2['date']

def compare_dates_ind(partido1, partido2 ): 
    """
    cmp que compara los 2 partidos según su fecha, si son iguales, se guia por el pais.
    """
    if partido1['date']== partido2['date']: 
        return  ((partido1["home_team"]) > (partido2["home_team"]))
    else: 
        return partido1['date'] > partido2['date']
    
def cmp_dates(partido1, partido2): 
    """
    cmp que compara los 2 partidos según su fecha, si son iguales, se guia por el pais.
    """
    if partido1['date']> partido2['date']: 
        return 1
    elif partido1['date'] < partido2['date']: 
        return -1
    else: 
        return 0

def cmp_Map_names(equipo, partido): 
    """
    cmp que compara 2 equipos segun su nomreb
    """
    equipoentry = me.getKey(partido)
    if equipo > equipoentry:
        return 1
    elif equipo < equipoentry:
        return -1
    else: 
        return 0

def compare_goleadores(gol1, gol2):
    if gol1['date'] == gol2['date']: 
        return gol1['minute']< gol2['minute']
    else:
        return gol1['date'] > gol2['date']
    
def compare_date_name_city(partido1, partido2):
    """
    Función que compara 2 partidos según su fecha, pais y condición 
    """
    if partido1['date'] == partido2['date']: 
        
        if partido1['country'] == partido2['country']: 
            return partido1['city']> partido2['city']
        else: 
            return partido1['country'] > partido2['country']
    else: 
        return partido1['date'] > partido2['date']
        
    
def compare_points( equipo1, equipo2): 
    """
    Función que compara 2 partidos segun el total de puntos obtenidos, la diferencia de goles, los totales de la linea penal 
    y el total de partiods
    """
    if me.getValue(mp.get(equipo1, 'total_puntos_obtenidos')) == me.getValue(mp.get(equipo2, 'total_puntos_obtenidos')): 
        if me.getValue(mp.get(equipo1, 'diferencia_goles')) == me.getValue(mp.get(equipo2, 'diferencia_goles')): 
            if me.getValue(mp.get(equipo1, 'total_linea_penal')) == me.getValue(mp.get(equipo2, 'total_linea_penal')): 
                    return me.getValue(mp.get(equipo1, 'total_partidos'))> me.getValue(mp.get(equipo2, 'total_partidos'))
            else: 
                return me.getValue(mp.get(equipo1, 'total_linea_penal')) > me.getValue(mp.get(equipo2, 'total_linea_penal'))
        else: 
            return me.getValue(mp.get(equipo1, 'diferencia_goles'))  > me.getValue(mp.get(equipo2, 'diferencia_goles'))
    
    else:
        return me.getValue(mp.get(equipo1, 'total_puntos_obtenidos')) >  me.getValue(mp.get(equipo2, 'total_puntos_obtenidos')) 

def compare_points_jug( equipo1, equipo2): 
    """
    Función que compara 2 partidos segun el total de puntos obtenidos, el total de goles, los goles de los penales 
    y tiempo promedio de los goles
    """
    if me.getValue(mp.get(equipo1, 'total_points')) == me.getValue(mp.get(equipo2, 'total_points')): 
        if me.getValue(mp.get(equipo1, 'total_goals')) == me.getValue(mp.get(equipo2, 'total_goals')): 
            if me.getValue(mp.get(equipo1, 'penalty_goals')) == me.getValue(mp.get(equipo2, 'penalty_goals')): 
                return me.getValue(mp.get(equipo1, 'avg_time')) < me.getValue(mp.get(equipo2, 'avg_time'))  
            else: 
                return me.getValue(mp.get(equipo1, 'penalty_goals')) > me.getValue(mp.get(equipo2, 'penalty_goals'))
        else: 
            return me.getValue(mp.get(equipo1, 'total_goals'))  > me.getValue(mp.get(equipo2, 'total_goals'))
    
    else:
        return me.getValue(mp.get(equipo1, 'total_points')) >  me.getValue(mp.get(equipo2, 'total_points')) 
    
def compareGoleadoresMenaMay(partido1, partido2 ): 

    if partido1['date']== partido2['date']:
        if partido1['minute'] == partido2['minute']: 
            return 0
        else:
            return 1
    elif partido1['date'] < partido2['date']: 
        return 1
    else: 
        return 0

# ------------------------------ Funciones de ordenamiento ------------------------------

def sortData(catalog, size,  filename): 
    return merg.sort(lt.subList(catalog[filename], 1, size), comparePartidos)
