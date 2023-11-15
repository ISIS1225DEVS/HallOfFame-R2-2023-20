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
from datetime import datetime as dt
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
from tabulate import tabulate

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    data_structs = {'partidos': None,
               'goleadores': None,
               'penales': None,
               'scorer':None,
               'Top':None,
               'Year_Tourna':None}

    data_structs['partidos'] =lt.newList('ARRAY_LIST',compare_date_home_away) 
    data_structs['goleadores'] = lt.newList('ARRAY_LIST',compare_date_minute)
    data_structs['penales'] = lt.newList('ARRAY_LIST',compare_date_home_away_team)
    
    data_structs['scorer']=mp.newMap(441114,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   )
    data_structs['Top']=mp.newMap(441114,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   )
    data_structs['torneos']=mp.newMap(150,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   )
    data_structs['team']=mp.newMap(320,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   )
    data_structs["Goleador Team"]=mp.newMap(320,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   )
    data_structs["Penales Team"]=mp.newMap(320,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   )
    data_structs["Year"]=mp.newMap(800,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   )
    
    return data_structs


# Funciones para agregar informacion al modelo
def add_partidos(data_structs, partidos):
    """
    Función para agregar nuevos elementos a la lista
    """
    lt.addLast(data_structs["partidos"],partidos)
    return data_structs


def add_goleadores(data_structs, goleadores):
    """
    Función para agregar nuevos elementos a la lista
    """
    lt.addLast(data_structs['goleadores'],goleadores)
    return data_structs


def add_penales(data_structs, penales):
    """
    Función para agregar nuevos elementos a la lista
    """
    lt.addLast(data_structs['penales'],penales)
    return data_structs


def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass

def addbytorneo(catalog, partido):
   
    tournaments = catalog["torneos"]
    title = partido["tournament"]
    existstorneo = mp.contains(tournaments, title)
    if existstorneo == True:
        entry = mp.get(tournaments, title)
        newtorneo = me.getValue(entry)
    else:
        newtorneo = createTorneo(title) 
        mp.put(tournaments, title, newtorneo)
    lt.addLast(newtorneo["results"],partido)
    return catalog


def addbyscorer(players, scorer):

    title = scorer["scorer"]
    existscorer = mp.contains(players, title)
    if existscorer == True:
        entry = mp.get(players, title)
        newscorer = me.getValue(entry)
    else:
        newscorer = createScorer(title) 
        mp.put(players, title, newscorer)
    lt.addLast(newscorer["results"],scorer)
    return players


def addbyteam(teams, equipo):
    equipo_home = equipo['home_team']
    existsteam = mp.contains(teams,equipo_home)
    if existsteam == True:
        entry = mp.get(teams,equipo_home)
        newteam = me.getValue(entry)
    else:
        newteam = createTeam(equipo_home)
        mp.put(teams,equipo_home,newteam)
    lt.addLast(newteam['results'],equipo)

    equipo_away = equipo['away_team']
    existsteam = mp.contains(teams,equipo_away)
    if existsteam == True:
        entry = mp.get(teams,equipo_away)
        newteam = me.getValue(entry)
    else:
        newteam = createTeam(equipo_away)
        mp.put(teams,equipo_away,newteam)
    lt.addLast(newteam['results'],equipo)

    return teams

def addbyYear(years, partido):
    year = partido['date']
    year = year[0:4]
    existsteam = mp.contains(years,year)
    if existsteam == True:
        entry = mp.get(years,year)
        newteam = me.getValue(entry)
    else:
        newteam = createTeam(year)
        mp.put(years,year,newteam)
    lt.addLast(newteam['results'],partido)

    
def createScorer(goal):
    title = {'scorer': "", "results": None}
    title['scorer'] = goal
    title['results'] = lt.newList('ARRAY_LIST')
    return title


def createTorneo(title):
    title = {'torneo': "", "results": None}
    title['torneo'] = title
    title['results'] = lt.newList('ARRAY_LIST')
    return title


def createTeam(equipo):
    team = {'Equipo': "", "results": None}
    team['Equipo'] = equipo
    team['results'] = lt.newList('ARRAY_LIST')
    return team


def addBytopscorer(catalog,scorer):
    Top_map=catalog['Top']
    
    Key1= str (scorer['date']) + scorer['home_team'] +scorer['away_team']
    existscorer = mp.contains(Top_map, Key1)
    
    if existscorer == True:
        entry = mp.get(Top_map, Key1)
        scorer["date"]=dt.strptime(scorer["date"], "%Y-%m-%d").date()
        newscorer = me.getValue(entry)
    else:
        newscorer = createTOP(Key1) 
        mp.put(Top_map, Key1, newscorer)
        scorer["date"]=dt.strptime(scorer["date"], "%Y-%m-%d").date()
    lt.addLast(newscorer["results"],scorer)
    return catalog
    

def top_scorer2(catalog,results):
    Top_map=catalog['Top']
    
    Key2= str (results['date']) + results['home_team'] + results['away_team']
    existscorer = mp.contains(Top_map, Key2)
    
    if existscorer == True:
        entry = mp.get(Top_map, Key2)
        newscorer = me.getValue(entry)
        newscorer1=lt.getElement(newscorer["results"],1)
        newscorer1['home_score']=results['home_score']
        newscorer1['away_score']=results['away_score']
        newscorer1['tournament']=results['tournament']
        mp.put(Top_map, Key2, newscorer)
    return catalog
    
    
     
     
def createTOP(TOPE):
   
    title = {'TOP': "", "results": None}
    title['scorer'] = TOPE
    title['results'] = lt.newList('ARRAY_LIST')
    return title
    
def ToPpro(catalog):
    Top_map=catalog['Top']
    values=mp.valueSet(Top_map)
    new_map=mp.newMap(800, 
                      maptype='PROBING',
                       loadfactor=0.5,)
    for value in lt.iterator(values):
        if value != None:
            scorer= lt.getElement(value['results'],1)
            new_scorer=scorer['scorer']
        
        
            existscorer = mp.contains(new_map, new_scorer)
            if existscorer == True:
                entry = mp.get(new_map, new_scorer)
                newscorer = me.getValue(entry)
            else:
                newscorer = createScorer(new_scorer) 
                mp.put(new_map,new_scorer, newscorer)
            lt.addLast(newscorer["results"],scorer)
        
    catalog['Top']=new_map
    return catalog
        
def addbyYear_tournament(catalog,results,scorer)  :
    Best_year=catalog['Year_Tourna']
    for result in lt.iterator(results):
        
    
        Key1= result["date"]
        existscorer = mp.contains(Best_year, Key1)
        
        if existscorer == True:
            entry = mp.get(Best_year, Key1)
            newscorer = me.getValue(entry)
            key2=result["Tournament"]
        else:
            newscorer = mp.newMap(800,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   )
            mp.put(Best_year, Key1, newscorer)
        lt.addLast(newscorer["results"],scorer)
        return catalog
    
   
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


def req_1(teams,NPartidos,equipo,condicion):
    """
    Función que soluciona el requerimiento 1
    """
    team = me.getValue(mp.get(teams,equipo))
    merg.sort(team["results"],compare_date_home_away)
    totalequippos = mp.size(teams)
    totalpartidos = lt.size(team['results'])
    home_list = lt.newList('ARRAY_LIST')
    away_list = lt.newList('ARRAY_LIST')
    total_home = 0
    total_away = 0

    for partido in lt.iterator(team['results']):
        if partido['home_team'] == equipo:
            lt.addLast(home_list,partido)
            total_home += 1
        elif partido['away_team'] == equipo:
            lt.addLast(away_list,partido)
            total_away += 1
    
    if condicion == 'local':
        merg.sort(home_list,comparedate)
        return totalequippos, totalpartidos, total_home, home_list
    elif condicion == 'visitante':
        merg.sort(away_list,comparedate)
        return totalequippos, totalpartidos, total_away, away_list
    elif condicion == 'indiferente':
        merg.sort(team['results'],comparedate)
        return totalequippos, totalpartidos, totalpartidos, team['results']
    


def req_2(goleadores,Ngoles,jugador):

    Scorer=me.getValue(mp.get(goleadores,jugador))
    merg.sort(Scorer["results"],compare_date_minute)
    total_jogadores=mp.size(goleadores)
    total_anotaciones=lt.size(Scorer["results"])
    sub_penal=0
    
    for goleador in lt.iterator(Scorer["results"]):
        if goleador["penalty"]=="True":
            sub_penal+=1         
    return total_jogadores,total_anotaciones,sub_penal,Scorer["results"]
    

def req_3(teams,goleadores_team,equipo,inicio,final):
    """
    Función que soluciona el requerimiento 3
    """
    totalequippos = mp.size(teams)
    team = me.getValue(mp.get(teams,equipo))
    merg.sort(team["results"],compare_date_home_away)
    partidos = FiltroFechas(team["results"],inicio,final)

    goleadores = me.getValue(mp.get(goleadores_team,equipo))
    merg.sort(goleadores["results"],compare_date_minute)
    goleadores = FiltroFechas(goleadores["results"],inicio,final)
    
    for partido in lt.iterator(partidos):
        penalty = "Unknown"
        owngoal = "Unknown"
        for goleador in lt.iterator(goleadores):
            if goleador["date"]== partido["date"] and goleador["team"]==equipo:
                penalty = goleador["penalty"]
                owngoal = goleador["own_goal"]
        partido["penalty"]=penalty
        partido["own_goal"]=owngoal

    partidos = merg.sort(partidos, comparedate2)
    total =lt.size(partidos)
    totalhome = 0
    totalaway = 0

    for partido in lt.iterator(partidos):
        if partido["home_team"] == equipo:
            totalhome+=1
        if partido["away_team"] == equipo: 
            totalaway+=1
    
    return partidos,total,totalhome,totalaway, totalequippos


def req_4(torneos,penales_team,torneo,inicio,final):
    """
    Función que soluciona el requerimiento 4
    """
    total_torneos = mp.size(torneos)
    partidos = me.getValue(mp.get(torneos,torneo))
    req4 = FiltroFechas(partidos['results'], inicio, final )
    merg.sort(req4,compare_date_home_away)
    total_partidos=lt.size(req4)
    totalshoot = 0
    totalcountry = 0
    countries = []
    totalcity = 0
    cities = []

    for partido in lt.iterator(req4):
        
        if partido["country"] not in countries:
            countries.append(partido["country"])
            totalcountry+=1
        
        if partido["city"] not in  cities:
            cities.append(partido["city"])
            totalcity+=1

        partido["winner"] = "Unknown"
        equipo = partido["home_team"]
        existpenales = mp.contains(penales_team,equipo)
        if existpenales == True:
            penales_posibles  = me.getValue(mp.get(penales_team,equipo))
            penales_posibles = FiltroFechas(penales_posibles["results"],inicio,final)
        
            for penal in lt.iterator(penales_posibles):
                if penal["date"] == partido["date"] and partido["home_team"] == penal["home_team"]:
                    partido["winner"]=penal["winner"]
                    totalshoot+=1

    merg.sort(req4,comparedate)
    return total_torneos,total_partidos, totalcountry,totalcity,totalshoot,req4


def req_5(Top,jugador,fecha_ini,fecha_fin):
    """
    Función que soluciona el requerimiento 5
    """
    Scorer=me.getValue(mp.get(Top,jugador))
    merg.sort(Scorer["results"],compare_date_minute)
    total_anotaciones=lt.size(Scorer["results"])
    sub_penal=0
    sub_torneos=0
    sub_autogol=0
    torneos=[]
    date_list=lt.newList('ARRAY_LIST')
    for goleador in lt.iterator(Scorer["results"]):
        if dt.strptime(fecha_ini , "%Y-%m-%d").date() <= goleador["date"] <=  dt.strptime(fecha_fin , "%Y-%m-%d").date():
            if goleador["penalty"]=="True":
                sub_penal+=1   
            if goleador["own_goal"]=="True":
                sub_autogol+=1  
            if goleador["tournament"] not in torneos:
                torneos.append(goleador["tournament"])
            sub_torneos += 1
        
            lt.addLast(date_list,goleador)
    merg.sort(date_list, comparedate)
    return total_anotaciones,sub_torneos,sub_penal,sub_autogol,date_list



def req_6 (torneos,years,goleadores_team,Nequipos,torneo,year):
    total_years = mp.size(years)
    partidos_year = me.getValue(mp.get(years,year))
    partidos_year = partidos_year["results"]

    partidos_torneo = me.getValue(mp.get(torneos,torneo))
    partidos_torneo = partidos_torneo['results']
    inicio = year + "-01-01"
    final = year + "12-31"
    partidos_torneo = FiltroFechas(partidos_torneo,inicio,final)
    total_partidos = lt.size(partidos_torneo)

    equipos = mp.newMap(800,
                            maptype='PROBING',
                            loadfactor=0.5,
                            )
    
    totalcountry = 0
    countries = []
    totalcity = 0
    cities = []

    for partido in lt.iterator(partidos_torneo):
        addbyteam(equipos,partido)

        if partido["country"] not in countries:
            countries.append(partido["country"])
            totalcountry+=1
        if partido["city"] not in  cities:
            cities.append(partido["city"])
            totalcity+=1
    
    total_equipos = mp.size(equipos)
    equipos_list = mp.valueSet(equipos)
    req6 = lt.newList('ARRAY_LIST')

    for equipo in lt.iterator(equipos_list):
        equipo = equipo['Equipo']
        partidos_equipo = me.getValue(mp.get(equipos,equipo))
        partidos_equipo = partidos_equipo['results']
        goleadores_equipo = me.getValue(mp.get(goleadores_team,equipo))
        goleadores_equipo = goleadores_equipo['results']

        equipo_dict = {
            "team": equipo,
            "total_points":0,
            "goal_difference":0,
            "penalty_points":0,
            "matches":0,
            "own_goal_points":0,
            "wins":0,
            "draws":0,
            "losses":0,
            "goals_for":0,
            "goals_againist":0,
            "top_scorer":{}
            }
        
        equipo_dict["matches"] = lt.size(partidos_equipo)
        wins = 0 
        draws = 0
        losses = 0

        for partido in lt.iterator(partidos_equipo):

            if equipo == partido["home_team"]:
                goals_team_scorer = int(partido["home_score"])
                goals_team_other = int(partido["away_score"])
            elif equipo == partido["away_team"]:
                goals_team_scorer = int(partido["away_score"])
                goals_team_other = int(partido["home_score"])
            
            equipo_dict["goal_difference"] = goals_team_scorer - goals_team_other

            if goals_team_scorer > goals_team_other:
                wins += 1
            elif goals_team_scorer == goals_team_other:
                draws += 1 
            elif goals_team_scorer < goals_team_other:
                losses += 1
        
        equipo_dict["wins"] = wins 
        equipo_dict["draws"] = draws
        equipo_dict["losses"] = losses
        equipo_dict["total_points"] = wins*3 + draws

        top_scorer = lt.subList(goleadores_equipo,0,1)
        top_scorer = tabulate(lt.iterator(top_scorer),headers="keys",tablefmt="grid")
        equipo_dict["top_scorer"] = top_scorer

        lt.addLast(req6,equipo_dict)
    
    #merg.sort(req6,comparedate)

    return total_years, total_equipos, total_partidos, totalcountry, totalcity, req6


def req_7(torneos,goleadores_team,torneo, NPuntos):
    """
    Función que soluciona el requerimiento 7
    """
    total_torneos = mp.size(torneos)
    partidos = me.getValue(mp.get(torneos,torneo))
    partidos = partidos["results"]
    merg.sort(partidos,compare_date_home_away)
    total_partidos = lt.size(partidos)
    total_goles = 0
    total_penales = 0
    total_owngoales = 0 
    anotadores = mp.newMap(800,
                            maptype='PROBING',
                            loadfactor=0.5,
                            )

    for partido in lt.iterator(partidos):
        total_goles += int(partido["home_score"]) + int(partido["away_score"])
        equipo = partido['home_team']
        scorer_team = me.getValue(mp.get(goleadores_team,equipo))
        scorer_team = scorer_team['results']

        for goleador in lt.iterator(scorer_team):
            if goleador["date"] == partido["date"] and goleador["home_team"] == partido["home_team"]:
                goleador['home_score'] = partido['home_score']
                goleador['away_score'] = partido['away_score']
                addbyscorer(anotadores,goleador)
    
    anotadores_list = mp.valueSet(anotadores)
    req7 = lt.newList('ARRAY_LIST')
    
    for scorer in lt.iterator(anotadores_list):
        scorer = scorer['scorer'] 
        anotaciones = me.getValue(mp.get(anotadores,scorer))
        anotaciones = anotaciones['results']

        scorer_torneo = {
            "scorer": scorer,
            "total_points":0,
            "total_goals":0,
            "penalty_goals":0,
            "own_goals":0,
            "avg_time (min)":0,
            "scored_in_wins":0,
            "scored_in_losses":0,
            "scored_in_draws":0,
            "last_goal":{}
        }
        sum_prom = 0
        n_prom = 0 
        wins = 0 
        draws = 0

        for anotacion in lt.iterator(anotaciones): 
            scorer_torneo["total_goals"] += 1
            sum_prom += float(anotacion["minute"])
            n_prom += 1

            if anotacion["penalty"]=="True":
                scorer_torneo["penalty_goals"] += 1
                total_penales += 1 
            if anotacion["own_goal"]=="True":
                scorer_torneo["own_goals"] += 1
                total_owngoales += 1 

            if anotacion["team"] == anotacion["home_team"]:
                goals_team_scorer = int(anotacion["home_score"])
                goals_team_other = int(anotacion["away_score"])
            elif anotacion["team"] == anotacion["away_team"]:
                goals_team_scorer = int(anotacion["away_score"])
                goals_team_other = int(anotacion["home_score"])

            if goals_team_scorer > goals_team_other:
                scorer_torneo["scored_in_wins"] += 1
                wins += 1
            elif goals_team_scorer == goals_team_other:
                scorer_torneo["scored_in_draws"] += 1
                draws += 1 
            elif goals_team_scorer < goals_team_other:
                scorer_torneo["scored_in_losses"] += 1
        
        scorer_torneo["total_points"] = wins*3 + draws
        scorer_torneo["avg_time (min)"] = sum_prom/n_prom
        last_goal = lt.subList(anotaciones,0,1)
        last_goal = tabulate(lt.iterator(last_goal),headers="keys",tablefmt="grid")
        scorer_torneo["last_goal"] = last_goal


        if scorer_torneo["total_points"] == int(NPuntos):
            lt.addLast(req7,scorer_torneo)

    merg.sort(req7,compare_avgminute)    
    total_scorers = mp.size(anotadores)
    
    return total_torneos,total_scorers,total_partidos,total_goles, total_penales, total_owngoales, req7



def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def comparedate(data1,data2):
    return (data1["date"] > data2["date"])

def comparedate2(data1,data2):
    return (data1["date"] < data2["date"])


def compare_date_minute(data1,data2):
    retorno = (data1["date"] < data2["date"])
    if data1["date"] == data2["date"]:
        return (data1["minute"] < data2["minute"])
    return retorno


def sort_date(data_structs):
    sorted_list = merg.sort(data_structs, comparedate)
    return sorted_list


def compare_date_home_away(data1,data2):
    retorno = data1["date"] > data2["date"]
    if data1["date"] == data2["date"]:
        return data1["home_score"] > data1["home_score"]
    if data1["home_score"] == data1["home_score"]:
        return data1["away_score"] > data1["away_score"]
    return retorno

def compare_date_home_away_team(data1,data2):
    retorno = data1["date"] > data2["date"]
    if data1["date"] == data2["date"]:
        return data1["home_team"] > data1["home_team"]
    if data1["home_team"] == data1["home_team"]:
        return data1["away_team"] > data1["away_team"]
    return retorno

def compare_avgminute(data1,data2):
    return data1["avg_time (min)"] < data2["avg_time (min)"]


def FiltroFechas(partidos, inicial, final):
    """FiltroEquposLocal filtra los datos de partidos por equipo dentro del atributo "date"
    Args:
        partidos(dict): el catalogo de partidos
        inicial(str): Fecha incial para filtrar
        final(str): Fecha final para filtrar 

    Returns:
        ADT List: lista de equipos filtrados, inicialmente vacia y por
        defecto SINGLE_LINKED
    """

    filt_list = lt.newList("ARRAY_LIST")
    for partido in lt.iterator(partidos):
        if partido["date"] >= inicial and partido["date"] <= final:
            lt.addLast(filt_list, partido)
    return filt_list


def FiltroTorneo(partidos, torneo):
    """FiltroEquposLocal filtra los datos de partidos por equipo dentro del atributo "home_team" o "away_team" o ambos
    Args:
        partidos(dict): el catalogo de partidos
        equipo (str): nombre del equipo nacional
        condicion(str): condicion del equipo (local,visitante,indiferente)

    Returns:
        ADT List: lista de equipos filtrados, inicialmente vacia y por
        defecto SINGLE_LINKED
    """

    filt_list = lt.newList("ARRAY_LIST")
    for partido in lt.iterator(partidos):
        if str(partido["tournament"]) == torneo:
            lt.addLast(filt_list, partido)
    return filt_list