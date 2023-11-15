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
from datetime import datetime
from datetime import timedelta
from tabulate import tabulate
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_catalog(list_type):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    
    mptipe = "CHAINING"
    factor = 4

    catalog = {     "Results": mp.newMap(224,
                                     maptype="PROBING",
                                     loadfactor=0.5),
                    "Goalscorers": mp.newMap(95,
                                     maptype=mptipe,
                                     loadfactor=factor),
                    "Shootouts":mp.newMap(95,
                                     maptype=mptipe,
                                     loadfactor=factor),
                    "Results_Team_H":mp.newMap(100,
                                     maptype=mptipe,
                                     loadfactor=factor),
                    "Results_Team_A":mp.newMap(100,
                                     maptype=mptipe,
                                     loadfactor=factor),
                    "torneos":mp.newMap(97,
                                     maptype="PROBING",
                                     loadfactor=0.5),
                    "paises":mp.newMap(150,
                                       maptype=mptipe,
                                     loadfactor=factor),
                    "tournaments_FTP":mp.newMap(127,
                                     maptype="PROBING",
                                     loadfactor=0.5),
                  
                    'goles_totales' : None,
                    'penaltis_totales' :None,
                    'partidos_totales': None,
                    }
    
    
    catalog['goles_totales'] = lt.newList(datastructure = list_type, cmpfunction = cmpID)
    catalog['penaltis_totales'] = lt.newList(datastructure = list_type, cmpfunction = cmpID)
    catalog["partidos_totales"] = lt.newList(datastructure = list_type, cmpfunction = cmpID)
    
    return catalog


# Funciones para agregar informacion al modelo

def add_gol(catalog, gol):
    gol["home_score"] = "unknown"
    gol["away_score"] = "unknown"
    gol["tournament"] = "unknown"
    gol["city"] = "unknown"
    gol["country"] = "unknown"
    gol["neutral"] = "unknown"
    lt.addLast(catalog["goles_totales"], gol)
    return catalog

def add_penalti(catalog, penalti):
    lt.addLast(catalog["penaltis_totales"], penalti)
    return catalog

def add_partido(catalog, partido):
    partido["own_goal"] = "unknown"
    partido["penalty"] = "unknown"
    partido["scorers"] = "unknown"
    partido["winner"] = "unknown"
    lt.addLast(catalog['partidos_totales'], partido)
    return catalog


#Funciones para añadir información

def new_result(date,home_team,away_team,home_score,away_score,tournament,city,country,neutral):
    """
    Crea una nueva estructura para modelar los datos
    """
    result = {
        "date":date,
        "home_team":home_team,
        "away_team":away_team,
        "home_score":home_score,
        "away_score":away_score,
        "tournament":tournament,
        "city":city,
        "country":country,
        "neutral":neutral
    }
    return result

def new_goalscorer(date,home_team,away_team,team,scorer,minute,own_goal,penalty):
    
    goalscorer = {
        "date":date,
        "home_team": home_team,
        "away_team": away_team,
        "team": team,
        "scorer":scorer ,
        "minute": minute,
        "own_goal": own_goal,
        "penalty":penalty
    
    }

    return goalscorer

def new_shootout(date,home_team,away_team,winner):
    
    shootout = {
        "date":date,
        "home_team": home_team,
        "away_team": away_team,
        "winner": winner

    }

    return shootout

#Funciones auxiliares para los nuevos mapas
def new_team(team):
    entry = {'team' : '', 'partidos' : None}
    entry['team'] = team
    entry['partidos'] = lt.newList('ARRAY_LIST', cmpID)
    return entry 

def new_tournament(torneo):
    entry = {'partidos' : None }
    entry["partidos"] = lt.newList("ARRAY_LIST", cmpID)
    return entry
    
def new_year(year):
    entry = {'year' : '', 'partidos' : None}
    entry['year'] = year
    entry['partidos'] = lt.newList('ARRAY_LIST', cmpID)
    return entry 



#Funciones que añade informacion a los mapas

#Funcion encargada de crear el mapa para partidos por equipo
def add_resultsT(catalog):
    partidos = catalog['partidos_totales']
    #Results, LLave: nombre de equipo, valor: todos los partidos que jugo este equipo
    partidos_t = catalog['Results']
    
    for partido in lt.iterator(partidos):
        existhome = mp.contains(partidos_t, partido["home_team"])
        existaway = mp.contains(partidos_t, partido["away_team"])
        
        if existhome:
            entry = mp.get(partidos_t, partido["home_team"])
            home_matchs = me.getValue(entry)
        else:
            home_matchs = lt.newList("ARRAY_LIST", cmpfunction=cmpID)
            mp.put(partidos_t,partido['home_team'], home_matchs)
        lt.addLast(home_matchs, partido)
        
    
        if existaway:
            entry = mp.get(partidos_t, partido["away_team"])
            away_matchs = me.getValue(entry)
        else:
            away_matchs = lt.newList("ARRAY_LIST", cmpfunction=cmpID)
            mp.put(partidos_t,partido['away_team'], away_matchs)
        lt.addLast(away_matchs, partido)
       
        
def add_results_AH(catalog):
    partidos = catalog['partidos_totales']
    # Results Team H esta ordeando de tal manera que la llave es el nombre del equipo y el valor todos los partidos que jugo este equipo de manera local(home)
    h = catalog['Results_Team_H']
    # Results Team A, Llave: nombre de equipo, Valor : Partidos jugados de manera visitante(Away)
    a = catalog['Results_Team_A']
    
    for partido in lt.iterator(partidos):
        existhome = mp.contains(h, partido["home_team"])
        existaway = mp.contains(a, partido["away_team"])
       
        if existhome:
            entry = mp.get(h, partido["home_team"])
            home_teams = me.getValue(entry)
        else:
            home_teams = new_team(partido["home_team"])
            mp.put(h,partido['home_team'], home_teams)
            
        lt.addLast(home_teams['partidos'], partido)
   
    
        if existaway:
            entry = mp.get(a, partido["away_team"])
            away_teams = me.getValue(entry)
        else:
            away_teams = new_team(partido["away_team"])
            mp.put(a,partido['away_team'], away_teams)
 
        lt.addLast(away_teams['partidos'], partido) 
        

#Funcion encargada de crear el mapa cuya llave son todos los torneos y el valor los partidos jugado en tal torneo
def add_torneos(catalog):
    partidos = catalog["partidos_totales"]
    torneos = catalog["torneos"]
    for partido in lt.iterator(partidos):
        existtorneo = mp.contains(torneos, partido["tournament"])
        if existtorneo:
            entry = mp.get(torneos, partido["tournament"])
            partidos_ = me.getValue(entry)
        else:
            partidos_ = lt.newList("ARRAY_LIST")
            mp.put(torneos,partido["tournament"], partidos_)
        lt.addLast(partidos_, partido)



def add_paises(catalog):
    partidos = catalog["partidos_totales"]
    torneos = catalog["paises"]
    
    """ for i in lt.iterator(partidos):
        año = i["date"][0:4]
        key = año + i["home_team"]
        key2 = año + i["away_team"]
        """

        
    
    for partido in lt.iterator(partidos):
        existpaisH = mp.contains(torneos, partido["home_team"])
        existpaisA = mp.contains(torneos, partido["away_team"])
        
        if existpaisA and existpaisH:
            entry1 = mp.get(torneos,partido["home_team"])
            entry2 = mp.get(torneos,partido["away_team"])
            partidos_ = me.getValue(entry1)
            partidos_2 = me.getValue(entry2)
            lt.addLast(partidos_, partido)
            lt.addLast(partidos_2, partido)
        
        if existpaisH and not existpaisA:
            
            entry = mp.get(torneos, partido["home_team"])
            partidos_ = me.getValue(entry)
        if not existpaisH and not existpaisA:
            key= partido["home_team"]
            partidos_ = lt.newList("ARRAY_LIST")
            mp.put(torneos,key, partidos_)
            lt.addLast(partidos_, partido)
        if existpaisA and not existpaisH:
           
            entry=mp.get(torneos, partido["away_team"])
            partidos=me.getValue(entry)
        if not existpaisA  and not existpaisH:
            key=  partido["away_team"]
            partidos_ = lt.newList("ARRAY_LIST")
            mp.put(torneos,key, partidos_)
            lt.addLast(partidos_, partido)
        
        
        
        
        
        
        
   
        
#Funcion encargada de crear el mapa cuya llave incial son fechas, el valor es otro mapa cuyas llaves son los torneos cuyo valor son los partidos. 
# FTP = Fecha-Torneos-Partidos
def add_torneosFTP(catalog):
    partidos = catalog["partidos_totales"]
    torneos = catalog["tournaments_FTP"]
    for partido in lt.iterator(partidos):
        existdate = mp.contains(torneos, partido["date"][:4])
        if existdate:
            entry = mp.get(torneos, partido["date"][:4])
            torneos_ = me.getValue(entry)
            existtorneo = mp.contains(torneos_, partido['tournament'])
            if existtorneo:
                entry_ = mp.get(torneos_, partido["tournament"])
                partidos_ = me.getValue(entry_)
            else:
                partidos_ = lt.newList("ARRAY_LIST")
                mp.put(torneos_,partido["tournament"], partidos_)
            lt.addLast(partidos_, partido)    
                
        else:
            torneos_ = mp.newMap(8,maptype="PROBING",loadfactor=0.5) 
            mp.put(torneos,partido['date'][:4],torneos_)
            partidos_ = lt.newList("ARRAY_LIST")
            mp.put(torneos_,partido["tournament"], partidos_)
            lt.addLast(partidos_, partido) 
                
                
                
                
def add_goalscorers(data_structs, data):

    jugador = data["scorer"]
    
    if mp.contains(data_structs["Goalscorers"],jugador):
        lt.addLast(me.getValue(mp.get(data_structs["Goalscorers"],jugador)),data)
    else:
        new_list = lt.newList("ARRAY_LIST")
        lt.addLast(new_list,data)
        mp.put(data_structs["Goalscorers"],jugador,new_list)

def add_shootouts(data_structs, data):
    
    año = data["date"][0:4]
    
    if mp.contains(data_structs["Shootouts"],año):
        lt.addLast(me.getValue(mp.get(data_structs["Shootouts"],año)),data)
    else:
        new_list = lt.newList("ARRAY_LIST")
        lt.addLast(new_list,data)
        mp.put(data_structs["Shootouts"],año,new_list)
        
        
#Funcion que añade la información a las columnas agregadas en 'partidos_totales'    
def conect_all_data(catalog):
    for gol in lt.iterator(catalog["goles_totales"]):
        pos = binarySearch_carga_de_datos(catalog["partidos_totales"],gol["date"],gol["home_team"],gol["away_team"]) 
        if pos != -1:
            partido = lt.getElement(catalog["partidos_totales"],pos)  
            scorer = {'team': gol['team'], 'name': gol['scorer'], 'minute':gol['minute'], 'own_goal':gol['own_goal'], 'penalty':gol['penalty']}
            
            if partido['scorers'] == 'unknown' :
                partido['scorers'] = lt.newList("ARRAY_LIST", cmpfunction=cmpID)
            lt.addLast(partido['scorers'], scorer)
           
            if partido['penalty'] == 'unknown':
               partido['penalty'] = gol['penalty']
            elif partido['penalty'] == 'False' and gol['penalty'] == "True":
                partido['penalty'] == 'True'
            
            if partido['own_goal'] == 'unknown':
                partido['own_goal'] = gol['own_goal']
            elif partido['own_goal'] == 'False' and gol['own_goal'] == "True":
                partido['own_goal'] == "True"

            lt.changeInfo(catalog["partidos_totales"],pos, partido)
            
            
    for penalti in lt.iterator(catalog["penaltis_totales"]):
        pos = binarySearch_carga_de_datos(catalog["partidos_totales"],penalti["date"],penalti["home_team"],penalti["away_team"]) 
        if pos != -1:
            partido = lt.getElement(catalog["partidos_totales"],pos)
            partido["winner"] = penalti["winner"]
            lt.changeInfo(catalog["partidos_totales"],pos, partido)
        
    return catalog

# Funciones de consulta

def partidostotales(catalog):
    return lt.size(catalog["partidos_totales"])

def golestotales(catalog):
    return lt.size(catalog["goles_totales"])

def penaltistotales(catalog):
    return lt.size(catalog["penaltis_totales"])



#Funciones para los requerimientos

def req_1(catalog,pais,condicion):
    
    partidos = catalog["Results"]
    home = catalog['Results_Team_H']
    away = catalog['Results_Team_A']
    entry = mp.get(partidos, pais)
    total_matches = me.getValue(entry)
  
    if condicion == "visitante" :
            entry = mp.get(away, pais)
            partidos_ = me.getValue(entry)
            
    elif condicion == "local" :
            entry = mp.get(home, pais)
            partidos_ = me.getValue(entry)
                  
    elif condicion == "indiferente":
        partidos_ = {'partidos': None} 
        partidos_['partidos'] = total_matches
    else:
        print("Error en la condicion")
    total_matches = mp.size(total_matches)
    total_teams = mp.size(partidos)
    return partidos_ , total_teams, total_matches


        
def req_2(catalog,jugador):
    goleadores = catalog["Goalscorers"]
    entry = mp.get(goleadores, jugador)
    goles = me.getValue(entry)
    
    total_scorers = mp.size(goleadores)
    total_penalties = 0
    for gol in lt.iterator(goles):
        if gol['penalty'] == "True":
            total_penalties += 1
    
    return goles, total_scorers, total_penalties



def req_3(catalog,pais,inicial,final):
    """
    Función que soluciona el requerimiento 3
    """
    contadorTotal=0
    contadorAway=0
    contadorHome=0
    filtro=lt.newList("ARRAY_LIST")
    mapa=catalog["paises"]
    entry = mp.get(mapa, pais)
    partidos = me.getValue(entry)
    
    tamañoC=mp.size(catalog["Results"])
    
    
    for partido in lt.iterator(partidos):
     if comparardelta(partido["date"][0:4],inicial, final):
        if partido["home_team"] == pais:
             contadorHome+=1
             contadorTotal+=1
             lt.addLast(filtro,partido)
        if partido["away_team"]== pais:
             contadorAway+=1
             contadorTotal+=1
             lt.addLast(filtro,partido)

   

    return filtro,tamañoC,contadorTotal,contadorAway, contadorHome
    

   
        
        
        
def req_4(catalog, nombre_t, fecha_inicial, fecha_final):
    #Contadores
    paises = lt.newList("ARRAY_LIST")
    ciudades = lt.newList("ARRAY_LIST")
    penaltis = lt.newList("ARRAY_LIST")
    
    #Se filtran los partidos según el torneo
    torneos = catalog["torneos"]
    entry = mp.get(torneos, nombre_t)
    #partidos es un array con todos los partidos del torneo en concreto
    partidos = me.getValue(entry)
    
    # Fecha 1 es la fecha mas antigua que hay dentro de los partidos
    fecha1 = binary_search_start_date(partidos, fecha_inicial)
    
    # Fecha 2 es la fecha mas reciente que hay dentro de los partidos
    fecha2 = binary_search_end_date(partidos, fecha_final)
    
    #numelem es la cantidad de elementos de la lista, esto es para pode utilizar subList
    numelem = fecha1 - fecha2
    
    #Si la fecha inicial es la primera, se cambia a 1 porque asi lo requerie subList
    if fecha2 == 0:
        fecha2 = 1
        
    #Se saca una sublista de acuerdo al rango proporcionado por el usuario  
    partidos_filtrados = lt.subList(partidos,fecha2, numelem)
    
    #Se recorren los partidos para las estadisticas
    for partido in lt.iterator(partidos_filtrados):
        if lt.isPresent(paises, partido['country']) == 0:
            lt.addLast(paises, partido['country'])
            
        if lt.isPresent(ciudades, partido['city']) == 0:
            lt.addLast(ciudades, partido['city'])
            
        if lt.isPresent(penaltis, partido['penalty']) == 0 and partido['winner'] != 'penalty':
            lt.addLast(penaltis, partido['penalty'])
            
        if lt.isPresent(penaltis, partido['winner']) == 0 and partido['winner'] != 'unknown':
            lt.addLast(penaltis, partido['winner'])
            
    #Se transforman los datos para poder imprmir en pantalla
    total_torneos = mp.size(torneos)
    total_partidos = lt.size(partidos_filtrados)
    paises = lt.size(paises)
    ciudades = lt.size(ciudades)
    penaltis = lt.size(penaltis)
    return partidos_filtrados, total_torneos, total_partidos, paises, ciudades, penaltis



def req_5(catalog, jugador, fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    turnaments = lt.newList("ARRAY_LIST")
    penalties = lt.newList("ARRAY_LIST")
    autogoals = lt.newList("ARRAY_LIST")

    size = mp.size(catalog["Goalscorers"])

    jugadores = catalog["Goalscorers"]
    entry = mp.get(jugadores, jugador)
    jug = me.getValue(entry)

    fecha1 = binary_search_start_date(jug, fecha_inicial)
    fecha2 = binary_search_end_date(jug, fecha_final)

    num = fecha1 - fecha2

    if fecha2 == 0:
        fecha2 == 1

    matches = lt.subList(jug,fecha2, num)

    for partido in lt.iterator(matches):
        if partido["penalty"] == "True":
            lt.addLast(penalties, partido['penalty'])

        if partido["own_goal"] == "True":
            lt.addLast(autogoals, partido['own_goal'])

    s_penalties = lt.size(penalties)
    s_autogoals = lt.size(autogoals)

    return jug,size,s_penalties,s_autogoals

def req_6(catalog, torneo, fecha):
    
    #Contadores
    teams = lt.newList("ARRAY_LIST")
    scorers = lt.newList("ARRAY_LIST")
    total_countries = lt.newList("ARRAY_LIST")
    total_cities = lt.newList("ARRAY_LIST")
    total_matches = 0
    
    equipos_t = lt.newList("ARRAY_LIST")
    #Funciones encargadas de encontrar los partidos segun los parametros
    partidosFTP = catalog['tournaments_FTP'] #Partidos FTP se refiere a el mapa organizado por Fecha-Torneo-Partidos
    
    entry = mp.get(partidosFTP,fecha)
    torneos = me.getValue(entry)
    entry2 = mp.get(torneos,torneo)
    partidos = me.getValue(entry2)
    
    #Aqui estamos iterando los partidos segun las condiciones del usuario
    for partido in lt.iterator(partidos):
                total_matches += 1
                if partido['city'] not in total_cities:
                    lt.addLast(total_cities,partido['city'])
                if partido['country'] not in total_countries:
                    lt.addLast(total_countries,partido['country'])
                if partido["home_team"] not in teams:
                    lt.addLast(teams,partido['home_score'])
                    lt.addLast(equipos_t, {"team" : partido["home_team"], "puntos_totales" : 0, "goles_diferencia" : 0, "puntos_penalti" : 0, "encuentros": 0 , "puntos_autogol":0, "victorias": 0, "empates": 0, "derrotas": 0, "goles_anotados":0 , "goles_en_contra" : 0, "goleadores": lt.newList("ARRAY_LIST")})
                if partido["away_team"] not in teams:
                    lt.addLast(teams,partido['away_score'])
                    lt.addLast(equipos_t, {"team" : partido["away_team"], "puntos_totales" : 0, "goles_diferencia" : 0, "puntos_penalti" : 0,  "encuentros": 0 , "puntos_autogol":0, "victorias": 0, "empates": 0, "derrotas": 0, "goles_anotados":0 , "goles_en_contra" : 0, "goleadores":lt.newList("ARRAY_LIST") }) 
                pos = posicion_equipo_home(equipos_t,partido)  
                pos2 = posicion_equipo_away(equipos_t,partido)
                sum_data(equipos_t, int(partido["home_score"]),int(partido["away_score"]),  pos)  
                sum_data(equipos_t, int(partido["away_score"]),int(partido["home_score"]),  pos2)
                
                if partido['scorers'] != "unknown":
                    for scorer in lt.iterator(partido['scorers']):  
                        sum_penal_gol(equipos_t, partido["home_team"], scorer, pos)
                        sum_penal_gol(equipos_t, partido["away_team"], scorer, pos2)
                        if scorer['name']not in scorers:
                            lt.addLast(scorers,scorer["name"])
                             
                        if partido["home_team"] == scorer['team']:
                            lt.addLast(equipos_t["elements"][pos]["goleadores"], {"scorer": scorer["name"], "goals": 0, "matches":0, "avg_time [min]": 0})
                            pos_ = posicion_scorer(equipos_t["elements"][pos]["goleadores"],scorer)
                            sum_scorer(scorer,pos_, equipos_t["elements"][pos]["goleadores"])
                            lt.addLast(equipos_t["elements"][pos2]["goleadores"] , {"scorer": 'unavailable', "goals": 0, "matches":0, "avg_time [min]": 0})
                        elif  partido["away_team"] == scorer['team']:
                            lt.addLast(equipos_t["elements"][pos2]["goleadores"] , {"scorer": scorer["name"], "goals": 0, "matches":0, "avg_time [min]": 0})
                            pos_ = posicion_scorer(equipos_t["elements"][pos2]["goleadores"],scorer)
                            sum_scorer(scorer,pos_, equipos_t["elements"][pos2]["goleadores"])
                            lt.addLast(equipos_t["elements"][pos]["goleadores"], {"scorer": 'unavailable', "goals": 0, "matches":0, "avg_time [min]": 0})
                        else:
                            lt.addLast(equipos_t["elements"][pos]["goleadores"], {"scorer": 'unavailable', "goals": 0, "matches":0, "avg_time [min]": 0})
                            lt.addLast(equipos_t["elements"][pos2]["goleadores"] , {"scorer": 'unavailable', "goals": 0, "matches":0, "avg_time [min]": 0})
            


    for equipo in lt.iterator(equipos_t):
        for goleador in lt.iterator(equipo['goleadores']):
            if goleador['scorer'] != 'unavailable':
                if goleador["goals"] >=2:
                    goleador["avg_time [min]"] = (goleador["avg_time [min]"]/goleador["matches"])
                    
        if lt.size(equipo['goleadores']) >= 2:
            scorers = sort_List(equipo["goleadores"], ordenar_goles) 
             
        top_scorer = equipo["goleadores"]["elements"][0:1]
        equipo["goleadores"] = tabulate(top_scorer, headers="keys", tablefmt="grid")
           
    torneos_con_info = mp.size(torneos)            
    total_teams = lt.size(teams)
    teams = lt.size(teams)
    scorers = lt.size(scorers)
    total_countries = lt.size(total_countries)
    total_cities = lt.size(total_cities)
    
    ordenados = sort_List(equipos_t, ordenar_puntos)
  
    return ordenados, torneos_con_info, total_teams, total_matches, total_countries, total_cities
        


def req_7(catalog,torneo, puntos):
    
    #Variables para info arriba de la tabla
    total_goals = 0
    total_penalties = 0
    total_own_goals = 0
    total_matches = 0
    
    #Variables para los calculos del requerimiento
    torneos = catalog['torneos']
    entry = mp.get(torneos,torneo)
    partidos = me.getValue(entry)
    
    scorers = lt.newList("ARRAY_LIST")
    nombres = []
    filtrados = lt.newList("ARRAY_LIST")
    for partido in lt.iterator(partidos):
        if partido["scorers"] != "unknown":
            total_matches += 1
            for scorer in lt.iterator(partido['scorers']):
                if scorer['name'] not in nombres:
                    nombres.append(scorer['name'])
                    lt.addLast(scorers,{"scorer": str(scorer['name']), "total_points":0, "total_goals":0, "penalty_goals":0, "own_goals":0, "avg_time [min]":0, "total_tournaments":0, "scored_in_wins":0, "scored_in_losses":0, "scored_in_draws":0, "last_goal" : lt.newList("ARRAY_LIST")})
                pos = posicion_scorer(scorers, scorer)
                sum_scorer2(partido,pos, scorers, scorer)
                #Funcion encargada de sumar estadisticas para info arriba de la tabla
                total_penalties, total_own_goals = sum_estadisticas(total_penalties, total_own_goals, scorer)
            total_goals += int(partido['home_score']) + int(partido['away_score'])
                
                
                
    for scorer in lt.iterator(scorers):
        if scorer['total_points'] == puntos:
            scorer["avg_time [min]"] = (scorer["avg_time [min]"]/scorer["total_goals"])
            ultimo = scorer["last_goal"]
            scorer["last_goal"] = print_tabulate(ultimo,["date","tournament","home_team","away_team","home_score","away_score","minute","penalty","own_goal"])
            lt.addLast(filtrados,scorer)
        
    ordenados = sort_List(filtrados, ordenar_puntos2) 
    
    torneos_con_info = mp.size(torneos)
    total_players = lt.size(scorers)   
    
    total_p_2points = lt.size(filtrados)
    return ordenados, torneos_con_info, total_players, total_matches, total_goals, total_penalties, total_own_goals,total_p_2points

def req_8(catalog, pais, inicial,final):
    teams = []
    scorers = []
    equipos_t = lt.newList("ARRAY_LIST")
    ultimo = lt.newList("ARRAY_LIST")
    paises = catalog['paises']  
    key_m =  pais
   
    entry = mp.get(paises,key_m)
    torneos = me.getValue(entry)
    
    for partido in lt.iterator(torneos):
        
        if comparardelta(partido["date"][0:4],inicial, final):
            if partido['tournament'] != "Friendly":
                lt.addLast(ultimo,partido)
                if partido["date"][0:4] not in teams:
                    teams.append(partido["date"][0:4])
                    lt.addLast(equipos_t, {"year" : partido["date"][0:4], "puntos_totales" : 0, "goles_diferencia" : 0, "puntos_penalti" : 0, "encuentros": 0 , "puntos_autogol":0, "victorias": 0, "empates": 0, "derrotas": 0, "goles_anotados":0 , "goles_en_contra" : 0, "goleadores": lt.newList("ARRAY_LIST")})
                
                pos = posicion_fecha1(equipos_t,partido)  
             
                
                sum_data2(equipos_t, int(partido["home_score"]),int(partido["away_score"]),  pos)
           
               
                
                if partido['scorers'] != "unknown":
                    for scorer in lt.iterator(partido['scorers']):  
                        sum_penal_gol(equipos_t, partido["home_team"], scorer, pos)
                       
                        if scorer['name']not in scorers:
                             scorers.append(scorer['name'])
                             
                        if partido["home_team"] == scorer['team']:
                            lt.addLast(equipos_t["elements"][pos]["goleadores"], {"scorer": scorer["name"], "goals": 0, "matches":0, "avg_time [min]": 0})
                            pos_ = posicion_scorer(equipos_t["elements"][pos]["goleadores"],scorer)
                            sum_scorer(scorer,pos_, equipos_t["elements"][pos]["goleadores"])
                            
                        elif  partido["away_team"] == scorer['team']:
                            
                            lt.addLast(equipos_t["elements"][pos]["goleadores"], {"scorer": 'unavailable', "goals": 0, "matches":0, "avg_time [min]": 0})
                        else:
                            lt.addLast(equipos_t["elements"][pos]["goleadores"], {"scorer": 'unavailable', "goals": 0, "matches":0, "avg_time [min]": 0})
                            
            


    for equipo in lt.iterator(equipos_t):
        for goleador in lt.iterator(equipo['goleadores']):
            if goleador['scorer'] != 'unavailable':
                if goleador["goals"] >=2:
                    goleador["avg_time [min]"] = (goleador["avg_time [min]"]/goleador["matches"])
                    
        if lt.size(equipo['goleadores']) >= 2:
            scorers = sort_List(equipo["goleadores"], ordenar_goles) 
             
        top_scorer = equipo["goleadores"]["elements"][0:1]
        equipo["goleadores"] = tabulate(top_scorer, headers="keys", tablefmt="grid")
           
    primero = lt.firstElement(torneos) 
    ultimo = lt.lastElement(ultimo)
    primero_y = lt.firstElement(equipos_t)
    ultimo_y = lt.lastElement(equipos_t)
    ultimo = ultimo["date"]
    
    
    year = int(primero_y["year"]) - int(ultimo_y["year"])
    
    
    size_t = lt.size(torneos)
    
    tablaInicio=lt.newList("ARRAY_LIST")
    lt.addLast(tablaInicio,primero)
    
    return equipos_t,tablaInicio,torneos,year,size_t,ultimo

def comparardelta(data,inicial,final):
    if inicial <= data and final >= data:
        return True
    else: 
        return False


# Funciones de ordenamiento

def sortResults(data_structs):
    
    sorted_list = sort_List(data_structs["partidos_totales"], compare_by_date_marcadorlocal_marcadorvisitante)
    return sorted_list

def sortGoalScorers(data_structs):
    sorted_list = sort_List(data_structs["goles_totales"], compare_by_date_minute_name)
    return sorted_list

def sortShootouts(data_structs):
    sorted_list = sort_List(data_structs["penaltis_totales"], compare_by_date_teamname)
    return sorted_list

def sort_List(list, comparefunction):
    
   sorted_list = merg.sort(list, comparefunction)
   return sorted_list

def cmpID(element1, element2):
    if (element1["id"] == element2['id']):
        return 0
    elif (element1["id"] > element2['id']):
        return 1
    return -1

#Funciones de comparación

def compare_by_date_marcadorlocal_marcadorvisitante(data_1, data_2):
    
    if data_1["date"] > data_2["date"]:
        return True
    elif data_1["date"] == data_2["date"]:
        if data_1["home_score"] > data_2["home_score"]:
            return True
    
        elif data_1["home_score"] == data_2["home_score"]:
            if data_1["away_score"] > data_2["away_score"]:
                return True
            else:
                return False
    
        else:
            return False
    else:
        return False
    
def compare_by_date_minute_name(data_1,data_2):
    if data_1["date"] > data_2["date"]:
        return True
    elif data_1["date"] == data_2["date"]:
        if data_1["minute"] > data_2["minute"]:
            return True
    
        elif data_1["minute"] == data_2["minute"]:
            if data_1["scorer"] > data_2["scorer"]:
                return True
            else:
                return False
    
        else:
            return False
    else:
        return False

def compare_by_date_teamname(data_1,data_2):
    if data_1["date"] > data_2["date"]:
        return True
    elif data_1["date"] == data_2["date"]:
        if data_1["home_team"] > data_2["home_team"]:
            return True
    
        elif data_1["home_team"] == data_2["home_team"]:
            if data_1["away_team"] > data_2["away_team"]:
                return True
            else:
                return False
    
        else:
            return False
    else:
        return False


#Seccion de busquedas binarias:

    # Busqueda Binaria Tradicional
def binarySearch(List, element, parameter):
    """
    Busqueda Binaria de un elemento en una lista ordenada ascendentemente
    Resultado: Indice en la lista donde se encuentra el elemento. -1 si no se encuentra.
    """
    i = 0
    f = lt.size(List)
    pos = -1
    found = False
    while i <= f and not found:
        # calcular la posicion de la mitad entre i y f
        m = (i + f) // 2
        if lt.getElement(List, m)[parameter] == element:
            pos = m
            found = True
        elif lt.getElement(List, m)[parameter] > element:
            
            f = m - 1
        else:
            i = m + 1
    print(lt.getElement(List, m)[parameter])
    return pos



#Busqueda binaria para encontrar la fecha inicial segun un array ordenado descendentemente
def binary_search_start_date(data_structs, start):
    """
    Busqueda binaria para encontrar una fecha de inicio
    """
    low = 1
    high = lt.size(data_structs)

    recent = (lt.firstElement(data_structs))['date']
    oldest = (lt.lastElement(data_structs))['date']
    
    formato_fecha = "%Y-%m-%d"
    recent = datetime.strptime(recent, formato_fecha)
    oldest = datetime.strptime(oldest, formato_fecha)
    start = datetime.strptime(start, formato_fecha)
    
    if start > recent:
        return -1

    #Confirmar que la fecha está en la lista en una posición intermedia
    if start >= oldest:

        #Buscar un día antes para evitar errores no encontrar la fecha mínima que coincide
        prev = start - timedelta(days=1)

        i = lt.size(data_structs)
        #Busqueda binaria
        while low <= high:
            mid = (low + high) // 2
            team = lt.getElement(data_structs, mid)
            mid_date = team['date']
            mid_date = datetime.strptime(mid_date, formato_fecha)
            if mid_date == prev:
                i = mid
                #Salir de un bucle infinito que no cambia el low
                low = lt.size(data_structs) + 1
            elif mid_date > prev:
                low = mid + 1
            else:
                high = mid - 1
            
            if low == high:
                i = mid
            i = mid
                
        find = False
        #Iterar hacia atrás para encontrar la primera fecha que coincide
        while not find:
            result = lt.getElement(data_structs, i)
            date = result['date']
            date = datetime.strptime(date, formato_fecha)
            if date >= start:
                #Se encuentra la fecha
                return i
            else:
                #Se sigue iterando
                i -= 1

            if i <= 0:
                return -1
    else:
        #Retornar posición de la fecha más antigua
        return lt.size(data_structs)
    
    
#Busqueda binaria para encontrar la fecha final segun un array ordenado descendentemente
def binary_search_end_date(data_structs, end):
    """
    Busqueda binaria para encontrar una fecha de final
    """
    low = 0
    high = lt.size(data_structs)

    recent = (lt.firstElement(data_structs))['date']
    oldest = (lt.lastElement(data_structs))['date']
    
    formato_fecha = "%Y-%m-%d"
    recent = datetime.strptime(recent, formato_fecha)
    oldest = datetime.strptime(oldest, formato_fecha)
    end = datetime.strptime(end, formato_fecha)
    #Confirmar si la fecha existe en el rango de la estructura
    if end < oldest:
        return -1
    #Confirmar que la fecha está en una posición intermedia
    if  end <= recent:
        #Buscar un día después para evitar errores no encontrar la fecha máxima que coincide
        next = end + timedelta(days=1)
        next_id = 1
        while low <= high:
            mid = (low + high) // 2
            team = lt.getElement(data_structs, mid)
            mid_date = team['date']
            mid_date = datetime.strptime(mid_date, formato_fecha)
            if mid_date == next:
                next_id = mid
                pass
            elif mid_date > next:
                low = mid + 1
            else:
                high = mid - 1
            if low == high:
                next_id = mid
                pass
        find = False
        i = next_id
        #Iterar hacia adelante para encontrar la primera fecha que coincide
        while not find:
            #Confirmar que el indice existe
            if i > 0 and i < lt.size(data_structs):
                date = (lt.getElement(data_structs, i))['date']
                date = datetime.strptime(date, formato_fecha)

                if date <= end:

                    return i
                else:
                    i += 1
            else:
                return 1
    else:
        return 0


#Busqueda binaria para la carga de datos, mas concretamente para conect_full_data
def binarySearch_carga_de_datos(list,date, home, away):
    i = 0
    f = lt.size(list)
    
    while i <= f:
        m = (i+f)//2
        dato = lt.getElement(list,m)
        fecha_dato = dato["date"]
        if fecha_dato < date:
            f = m-1
        elif fecha_dato > date:
            i = m+1
        else:
            hometeam_mid = dato["home_team"]
            awayteam_mid = dato["away_team"]
            if hometeam_mid == home and awayteam_mid == away:
                return m
            else:
                iprev = m-1
                prevelement = lt.getElement(list,iprev)
                while prevelement['date'] == date:
                    if prevelement['home_team'] == home and prevelement['away_team'] == away:
                        return iprev
                    iprev -= 1
                    prevelement = lt.getElement(list,iprev)
                inext = m +1
                nextelement = lt.getElement(list,inext)
                while nextelement['date'] == date:
                    if nextelement['home_team'] == home and nextelement['away_team'] == away:
                        return inext
                    inext += 1
                    nextelement = lt.getElement(list,inext)
                return -1
    return -1
             

#Funciones auxiliares para req 6


def ordenar_goles(scorer1,scorer2):
    if scorer1["goals"] > scorer2["goals"]:
        return True
    if scorer1["goals"] == scorer2["goals"]:
        if scorer1["avg_time [min]"] < scorer2["avg_time [min]"]:
            return True
        elif scorer1["avg_time [min]"] == scorer2["avg_time [min]"]:
            if scorer1["scorer"] == scorer2["scorer"]:
                return True
    else:
        return False

def ordenar_puntos(equipo1, equipo2):
    if equipo1["puntos_totales"] > equipo2["puntos_totales"]:
        return True
    if equipo1["puntos_totales"] == equipo2["puntos_totales"]:
        if equipo1["goles_diferencia"] > equipo2["goles_diferencia"]:
            return True
        if equipo1["goles_diferencia"] == equipo2["goles_diferencia"]:
            if  equipo1["puntos_penalti"] > equipo2["puntos_penalti"]:
                return True
            if equipo1["puntos_penalti"] == equipo2["puntos_penalti"]:
                if  equipo1["encuentros"] < equipo2["encuentros"]:
                    return True
                if  equipo1["encuentros"] == equipo2["encuentros"]:
                    if  equipo1["puntos_autogol"] < equipo2["puntos_autogol"]:
                        return True
    else:
        return False
    
def posicion_scorer(goleadores, partido):
    i = 0
    for scorer in lt.iterator(goleadores):
        if scorer["scorer"] == partido["name"]:
            return i
        i +=1
    return -1
    
    
def posicion_equipo_home(equipos_t,partido):
    i = 0
    for equipo in lt.iterator(equipos_t):
        if partido["home_team"] == equipo["team"]:
            return i
        i+=1
    return -1
def posicion_equipo_away(equipos_t,partido):
    i= 0
    for equipo in lt.iterator(equipos_t):
        if partido["away_team"] == equipo["team"]:
            return i
        i +=1
    return -1

def posicion_fecha1(equipos_t,partido):
    i = 0
    for equipo in lt.iterator(equipos_t):
        if partido["date"][0:4] == equipo["year"]:
            return i
        i+=1
    return -1
def posicion_fecha2(equipos_t,partido):
    i= 0
    for equipo in lt.iterator(equipos_t):
        if partido["date"][0:4] == equipo["year"]:
            return i
        i +=1
    return -1
                 
def sum_data(equipos_t, main, second, pos):
    # suma al total de encuentros del equipo
    equipos_t["elements"][pos]["encuentros"] +=1
    equipos_t["elements"][pos]["goles_anotados"] += main
    equipos_t["elements"][pos]["goles_en_contra"] += second
                       
    if main > second: 
        # suma al total de puntos y a la diferencia de goles          
       equipos_t["elements"][pos]["puntos_totales"] += 3
       equipos_t["elements"][pos]["goles_diferencia"] += (main-second) 
       equipos_t["elements"][pos]["victorias"] += 1   
    elif main == second:
        #Si fue empate no modifica goles diferencia porque los datos a restar son los mismos a sumar
        equipos_t["elements"][pos]["puntos_totales"] += 1
        equipos_t["elements"][pos]["empates"] += 1
    elif main < second:
        equipos_t["elements"][pos]["goles_diferencia"] += (main-second) 
        equipos_t["elements"][pos]["derrotas"] += 1
        

    return equipos_t

def sum_penal_gol(equipos_t, main_name, scorer, pos):
    # Suma puntos penalti si hubo anotacion
    if main_name == scorer["team"] and scorer["penalty"] == "True":
        equipos_t["elements"][pos]["puntos_penalti"] += 1
    if main_name == scorer["team"] and scorer["own_goal"] == "True":
        equipos_t["elements"][pos]["puntos_autogol"] += 1  
        
def sum_scorer(partido,pos, goleadores):
    
    goleadores["elements"][pos]["goals"] +=1
    goleadores["elements"][pos]["matches"] +=1
    goleadores["elements"][pos]["avg_time [min]"] += float(partido["minute"])
        
    return goleadores

#Funciones para el req 7 

def sum_scorer2(partido,pos, goleadores, scorer):
    if scorer["penalty"] == "True":
        goleadores["elements"][pos]["penalty_goals"] +=1
        goleadores["elements"][pos]["total_points"] += 1
    if scorer["own_goal"] == "True":
        goleadores["elements"][pos]["total_points"] += -1
    goleadores["elements"][pos]["total_points"] += 1
    goleadores["elements"][pos]["total_goals"] +=1
    if scorer["minute"] != "":
        goleadores["elements"][pos]["avg_time [min]"] += float(scorer["minute"])
    if lt.size(goleadores["elements"][pos]["last_goal"]) == 0:
        last_goal = {"date": partido['date'],"tournament": partido['tournament'],"home_team": partido['home_team'],"away_team":partido['away_team'],"home_score":partido['home_score'],"away_score":partido['away_score'],"minute" : scorer['minute'],"penalty":scorer['penalty'],"own_goal":scorer['own_goal']}
        lt.addLast(goleadores["elements"][pos]["last_goal"], last_goal)  

    if partido["home_team"] == scorer["team"]:
        if partido["home_score"] < partido["away_score"]:
            goleadores["elements"][pos]["scored_in_losses"] += 1
        elif partido["home_score"] > partido["away_score"]:
            goleadores["elements"][pos]["scored_in_wins"] += 1
        elif partido["home_score"] == partido["away_score"]:
            goleadores["elements"][pos]["scored_in_draws"] += 1

    elif partido["away_team"] == scorer["team"]:
        if partido["away_score"] < partido["home_score"]:
            goleadores["elements"][pos]["scored_in_losses"] += 1
        elif partido["away_score"] > partido["home_score"]:
            goleadores["elements"][pos]["scored_in_wins"] += 1
        elif partido["away_score"] == partido["home_score"]:
            goleadores["elements"][pos]["scored_in_draws"] += 1     


    return goleadores


def ordenar_puntos2(equipo1, equipo2):
    if equipo1["total_points"] > equipo2["total_points"]:
        return True
    if equipo1["total_points"] == equipo2["total_points"]:
        if equipo1["total_goals"] > equipo2["total_goals"]:
            return True
        if equipo1["total_goals"] == equipo2["total_goals"]:
            if  equipo1["penalty_goals"] > equipo2["penalty_goals"]:
                return True
            if equipo1["penalty_goals"] == equipo2["penalty_goals"]:
                if  equipo1["own_goals"] < equipo2["own_goals"]:
                    return True
                if  equipo1["own_goals"] == equipo2["own_goals"]:
                    if  equipo1["avg_time [min]"] < equipo2["avg_time [min]"]:
                        return True
    else:
        return False
    
def sum_data2(equipos_t, main, second, pos):
    # suma al total de encuentros del equipo
    equipos_t["elements"][pos]["encuentros"] +=1
    equipos_t["elements"][pos]["goles_anotados"] += main
    equipos_t["elements"][pos]["goles_en_contra"] += second
    # Suma puntos penalti si hubo anotacion                                
    if main > second: 
        # suma al total de puntos y a la diferencia de goles          
       equipos_t["elements"][pos]["puntos_totales"] += 3
       equipos_t["elements"][pos]["goles_diferencia"] += (main-second) 
       equipos_t["elements"][pos]["victorias"] += 1   
    if main < second:
        #si fue empate suma uno y no modifica goles diferencia porque los datos a restar son los mismos a sumar
        equipos_t["elements"][pos]["puntos_totales"] -=1
        equipos_t["elements"][pos]["derrotas"] += 1
    if main == second:
        equipos_t["elements"][pos]["empates"] += 1
        #si fue empate suma uno y no modifica goles diferencia porque los datos a restar son los mismos a sumar
        equipos_t["elements"][pos]["puntos_totales"] += 1
    
              
    return equipos_t

def sum_estadisticas(total_penalties, total_own_goals, scorer):
    if scorer['penalty'] == "True":
        total_penalties += 1
    if scorer['own_goal'] == "True":
        total_own_goals += 1
    return total_penalties, total_own_goals

def compare_fechas(data_1, inicial, final):
    formato_fecha = "%Y-%m-%d"
    data = datetime.strptime(data_1, formato_fecha)
    inicial = datetime.strptime(inicial, formato_fecha)
    final = datetime.strptime(final, formato_fecha)
    if inicial <= data and final >= data:
        return True
    else: 
        return False
    
def compare_fechas2(data_1, data_2):
    formato_fecha = "%Y-%m-%d"
    data1 = datetime.strptime(data_1, formato_fecha)
    data2 = datetime.strptime(data_2, formato_fecha)
    if data1 == data2:
        return True
    else:
        return False
        
def print_tabulate(lista, columnas):
    reduced = []
    for result in lista["elements"]:
        linea = []
        for c in columnas:
            linea.append(result[c])
        reduced.append(linea)  
    tabla = tabulate(reduced, headers=columnas, tablefmt="grid")
    return tabla

def getNumeroGoles(goles_filtrados, number):
    goles_t = lt.newList("ARRAY_LIST")
    if number > lt.size(goles_filtrados):
        number = lt.size(goles_filtrados)