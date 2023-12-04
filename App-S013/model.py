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
from datetime import date
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs(tipo_estructura, factor_carga, num_elementos): #Hecha por Juan Sebastián Ríos
    estructuras_de_datos = {
        "match_results": None,
        "scores": None,
        "penalties": None,
        "lista_match_results": None,
        "lista_scores": None,
        "lista_penalties": None,
        "match_results_year": None,
        "match_results_alphabetically": None,
        "goles_jugador": None
    }
    map_type = 'CHAINING' if tipo_estructura == '1' else 'PROBING'

    if map_type == 'CHAINING':
        factor_carga = 2 if factor_carga == '1' else (4 if factor_carga == '2' else (6 if factor_carga == '3' else 8))

    elif map_type == 'PROBING':
        factor_carga = 0.1 if factor_carga == '1' else (0.5 if factor_carga == '2' else (0.7 if factor_carga == '3' else 0.9))

    estructuras_de_datos["match_results"] = mp.newMap(numelements=num_elementos, maptype=map_type, loadfactor=factor_carga)
    estructuras_de_datos["scores"] = mp.newMap(numelements=num_elementos, maptype=map_type, loadfactor=factor_carga)
    estructuras_de_datos["penalties"] = mp.newMap(numelements=num_elementos, maptype=map_type, loadfactor=factor_carga)
    estructuras_de_datos["match_results_alphabetically"] = mp.newMap(numelements=num_elementos, maptype=map_type, loadfactor=factor_carga)
    estructuras_de_datos["goles_jugador"] = mp.newMap(numelements=num_elementos, maptype=map_type, loadfactor=factor_carga)
    estructuras_de_datos["goles_anio_torneo"] = mp.newMap(numelements=num_elementos, maptype=map_type, loadfactor=factor_carga)
    estructuras_de_datos["scores_date"] = mp.newMap(numelements=num_elementos, maptype=map_type, loadfactor=factor_carga)
    estructuras_de_datos["lista_match_results"] = lt.newList('ARRAY_LIST')
    estructuras_de_datos["lista_scores"] = lt.newList('ARRAY_LIST')
    estructuras_de_datos["lista_penalties"] = lt.newList('ARRAY_LIST')

    return estructuras_de_datos

def add_mresults(data_structs, data):
    match = new_mresult(data)
    mp.put(data_structs['match_results'], data["date"]+"-"+data["home_team"]+"-"+data["away_team"] , match)
    mp.put(data_structs['match_results_alphabetically'], data["date"]+"-"+data["home_team"]+"-"+data["away_team"], match)
    lt.addLast(data_structs["lista_match_results"], data["date"]+"-"+data["home_team"]+"-"+data["away_team"])
    return data_structs

def add_score(data_structs, data):
    score = new_score(data)
    mp.put(data_structs['scores'], data['date'] + '-' + data['home_team'] + '-' + data['away_team'] + '-' + data['team'] + '-' + data['scorer'], score)
    lt.addLast(data_structs["lista_scores"],data['date'] + '-' + data['home_team'] + '-' + data['away_team'] + '-' + data['team'] + '-' + data['scorer'])
    mp.put(data_structs['scores_date'], data['date'] + '-' + data['home_team'] + '-' + data['away_team'] + '-' + data['team'], score)
    return data_structs

def add_penaltie(data_structs, data):

    penaltie = new_penaltie(data)
    mp.put(data_structs['penalties'], data["date"]+"-"+data["home_team"]+"-"+data["away_team"], penaltie)
    lt.addLast(data_structs["lista_penalties"], data["date"]+"-"+data["home_team"]+"-"+data["away_team"])
    return data_structs

def add_score_player(data_structs, data):

    if mp.contains(data_structs["goles_jugador"],data["scorer"]):
        jugador = mp.get(data_structs["goles_jugador"],data["scorer"])
        lista = me.getValue(jugador)
        lt.addLast(lista,data)
    else:
        score_player = new_score_player(data)
        lt.addLast(score_player,data)
        mp.put(data_structs['goles_jugador'], data["scorer"], score_player)

    return data_structs

def add_year_tournament(data_structs, data):
    anio = data["date"].split("-")[0]

    if mp.contains(data_structs["goles_anio_torneo"],anio):
        llave_valor_torneo = mp.get(data_structs["goles_anio_torneo"],anio)
        mapa_torneo = me.getValue(llave_valor_torneo)
        if mp.contains(mapa_torneo,data["tournament"]):
            torneo = me.getValue(mp.get(mapa_torneo,data["tournament"]))
            lt.addLast(torneo,data)
        else:
            torneo = new_tournament_list()
            lt.addLast(torneo,data)
            mp.put(mapa_torneo,data["tournament"],torneo)
    else:
        mapa_anio = new_year_map()
        lista_torneo = new_tournament_list()
        lt.addLast(lista_torneo,data)
        mp.put(mapa_anio,data["tournament"],lista_torneo)
        mp.put(data_structs["goles_anio_torneo"],anio,mapa_anio)


def new_mresult(data):
    mresult = {
        'date': data['date'],
        'home_team': data['home_team'],
        'away_team': data['away_team'],
        'tournament': data['tournament'],
        'city': data['city'],
        'country': data['country'],
        'neutral': data['neutral'],
        'home_score': data['home_score'],
        'away_score': data['away_score']
    }
    return mresult

def new_score(data):
    score = {
        'date': data['date'],
        'home_team': data['home_team'],
        'away_team': data['away_team'],
        'team': data['team'],
        'scorer': data['scorer'],
        'minute': data['minute'],
        'own_goal': data['own_goal'],
        'penalty': data['penalty']
    }
    return score

def new_penaltie(data):
    penalty = {
        'date': data['date'],
        'home_team': data['home_team'],
        'away_team': data['away_team'],
        'winner': data['winner']
    }
    return penalty

def new_score_player(data):
    return lt.newList('ARRAY_LIST')

def new_year_map():
    return mp.newMap(numelements=50,maptype='PROBING', loadfactor=0.5)

def new_tournament_list():
    return lt.newList('ARRAY_LIST')

def get_mresult(data_structs, data):
    match = new_mresult(data)
    mp.put(data_structs['match_results'], data['date'] + '-' + data['home_team'] + '-' + data['away_team'], match)
    mp.put(data_structs['match_results_alphabetically'], data['date'] + '-' + data['home_team'] + '-' + data['away_team'], match)
    return data_structs


def get_score(data_structs, data):
    score = new_score(data)
    mp.put(data_structs['scores'], data['date'] + '-' + data['home_team'] + '-' + data['away_team'] + '-' + data['scorer'], score)
    return data_structs

def get_penaltie(data_structs, data):
    penaltie = new_penaltie(data)
    mp.put(data_structs['penalties'], data['date'] + '-' + data['home_team'] + '-' + data['away_team'] + '-' + data['winner'], penaltie)
    return data_structs

def data_size(data_structs):
    results_size = mp.size(data_structs['match_results'])
    scores_size = mp.size(data_structs['scores'])
    penalties_size = mp.size(data_structs['penalties'])
    return results_size, scores_size, penalties_size


def req_1(data_structs, n_matches, team_name, condition):
    team_matches = mp.newMap(numelements=mp.size(data_structs['match_results']), maptype='PROBING', loadfactor=0.5)

    matches = mp.keySet(data_structs['match_results'])
    for match_id in lt.iterator(matches):
        entry = mp.get(data_structs['match_results'], match_id)
        match = me.getValue(entry)
        
        if condition == "Local" and match['home_team'] == team_name:
            mp.put(team_matches, match_id, match)
        elif condition == "Visitante" and match['away_team'] == team_name:
            mp.put(team_matches, match_id, match)
        elif condition == 'Indiferente' and (match['home_team'] == team_name or match['away_team'] == team_name):
            mp.put(team_matches, match_id, match)

    length = mp.size(team_matches)
    
    if n_matches <= length:
        sub_matches = [me.getValue(mp.get(team_matches, match_id)) for match_id in range(1, n_matches + 1)]
    else:
        sub_matches = [me.getValue(mp.get(team_matches, match_id)) for match_id in lt.iterator(mp.keySet(team_matches))]

    if length > 6:
        first_matches = sub_matches[:3]
        last_matches = sub_matches[-3:]
        result_matches = first_matches + last_matches
    else:
        result_matches = sub_matches

    return length, result_matches, n_matches


def req_2(data_structs, n_score, name):
    goles_map = data_structs['goles_jugador'] #Mapa de goles
    llave_vl_gol = mp.get(goles_map, name)
    goles = me.getValue(llave_vl_gol)
    quk.sort(goles, compare_goals_jugador_req2)
    if lt.size(goles) > 6:
        lista_goles = lt.subList(goles, 1, 3)
        for gol in lt.iterator(lt.subList(goles,lt.size(goles)-2 , 3)):
            lt.addLast(lista_goles, gol)
    else:
        lista_goles = goles

    if n_score < lt.size(lista_goles):
        lista_goles_final = lt.subList(lista_goles, 1, n_score)
    else:
        lista_goles_final = lista_goles

    penalties = 0
    for gol in lt.iterator(lista_goles_final) :
        if gol["penalty"] == "True":
            penalties += 1

    return lista_goles_final , lt.size(lista_goles_final) , penalties , mp.size(goles_map)


def req_3(data_structs, t_name, start_d, end_d):
    start_d = date.fromisoformat(start_d)
    end_d = date.fromisoformat(end_d)

    match_list = mp.newMap(numelements=mp.size(data_structs['match_results']), maptype='PROBING', loadfactor=0.5)
    total_matches = 0
    matches_as_home = 0
    matches_as_away = 0

    matches = me.setKey(data_structs['match_results'], t_name)
    for match_id in lt.iterator(matches):
        entry = mp.get(data_structs['match_results'], match_id)
        match = me.getValue(entry)
        match_date = date.fromisoformat(match['date'])
        
        if start_d <= match_date <= end_d and (match['home_team'] == t_name or match['away_team'] == t_name):
            mp.put(match_list, match_id, match)
            total_matches += 1

            if match['home_team'] == t_name:
                matches_as_home += 1
            else:
                matches_as_away += 1

            scores = me.keySet(data_structs['scores'])
            for score_id in lt.iterator(scores):
                entry = mp.get(data_structs['scores'], score_id)
                goalscore = me.getValue(entry)

                if match['date'] == goalscore['date'] and match['home_team'] == goalscore['home_team'] and match['away_team'] == goalscore['away_team']:
                    if 'penalty' in match:
                        if goalscore['penalty'] == "True":
                            match['penalty'] = "True"
                        elif goalscore['penalty'] == "" and match['penalty'] == "False":
                            goalscore['penalty'] = "Unknown"
                    else:
                        if goalscore['penalty'] != "":
                            match['penalty'] = goalscore['penalty']
                        else:
                            match['penalty'] = "Unknown"

                    if 'own_goal' in match:
                        if goalscore['own_goal'] == "True":
                            match['own_goal'] = "True"
                        elif goalscore['own_goal'] == "" and match['own_goal'] == "False":
                            goalscore['own_goal'] = "Unknown"
                    else:
                        if goalscore['own_goal'] != "":
                            match['own_goal'] = goalscore['own_goal']
                        else:
                            match['own_goal'] = "Unknown"

    return total_matches, matches_as_home, matches_as_away, match_list

def req_4(data_structs, t_name, start_d, end_d):
    date_frmt1 = ([int(x) for x in (start_d.split('-'))])
    date_frmt2 = ([int(x) for x in (end_d.split('-'))])
    start_d = date(*date_frmt1)
    end_d = date(*date_frmt2)

    match_list = mp.newMap(numelements=lt.size(data_structs['match_results']), maptype='PROBING', loadfactor=0.5)
    n_matches = 0
    country_list = mp.newMap(numelements=10, maptype='CHAINING', loadfactor=0.5)
    city_list = mp.newMap(numelements=10, maptype='CHAINING', loadfactor=0.5)
    penalties = 0

    for entry in mp.iterator(data_structs['match_results']):
        match_id = entry['key']
        match = entry['value']
        match_date = date.fromisoformat(match['date'])

        if start_d <= match_date <= end_d and match['tournament'].lower() == t_name.lower():
            n_matches += 1

            if 'neutral' in match:
                match.pop('neutral')

            if match['home_score'] == match['away_score']:
                penalties += 1
                pos_penalties = mp.get(data_structs['penalties'], match_id)['value']
                penalty_winner = pos_penalties['winner']
                match['winner'] = penalty_winner
            else:
                match['winner'] = 'Unknown'

            mp.put(match_list, match_id, match)

            if not mp.contains(country_list, match['country']):
                mp.put(country_list, match['country'], match['country'])
            if not mp.contains(city_list, match['city']):
                mp.put(city_list, match['city'], match['city'])

    sorted_matches = [entry['value'] for entry in sorted(mp.iterator(match_list), key=req4_sort_criteria) if entry is not None]

    length = mp.size(match_list)
    if length > 6:
        firstelements = sorted_matches[:3]
        lastelements = sorted_matches[-3:]
        elements = firstelements + lastelements
    else:
        elements = sorted_matches

    return elements, n_matches, mp.size(country_list), mp.size(city_list)

def req_5(data_structure,jugador,f_inicial,f_final):
    """
    Función que soluciona el requerimiento 5
    """
    goles_map = data_structure['goles_jugador'] #Mapa de goles
    partidos = data_structure['match_results'] #Mapa de partidos
    llave_vl_gol = mp.get(goles_map, jugador)
    goles = me.getValue(llave_vl_gol)
    quk.sort(goles, compare_goals_jugador_req5)
    torneos = {}
    lista_torneos = lt.newList('ARRAY_LIST')
    penalties = 0
    autogol = 0
    lista_goles = lt.newList('ARRAY_LIST')
    for gol in lt.iterator(goles):
        llave = ""
        if gol["date"] >= f_inicial and gol["date"] <= f_final:
            llave = gol["date"]+"-"+gol["home_team"]+"-"+gol["away_team"]
            torneo = me.getValue(mp.get(partidos,llave))
            lt.addLast(lista_torneos,torneo)
            lt.addLast(lista_goles,gol)
            torneos[torneo["tournament"]] = 1
            if gol["penalty"] == "True":
                penalties += 1
            if gol["own_goal"] == "True":
                autogol += 1

    if lt.size(lista_goles) > 6:
        lista_goles_final = lt.subList(lista_goles, 1, 3)
        for gol in lt.iterator(lt.subList(lista_goles,lt.size(lista_goles)-2 , 3)):
            lt.addLast(lista_goles_final, gol)
        lista_torneos_final = lt.subList(lista_torneos, 1, 3)
        for torneo in lt.iterator(lt.subList(lista_torneos,lt.size(lista_torneos)-2 , 3)):
            lt.addLast(lista_torneos_final, torneo)
    else:
        lista_goles_final = lista_goles
        lista_torneos_final = lista_torneos

    return lista_goles_final,lt.size(lista_goles),len(torneos),mp.size(goles_map),penalties,autogol,lista_torneos_final



def req_6(data_structs,n_equipos,torneo,anio):

    mapa_goles_fecha = data_structs['scores_date']
    mapa_anios = data_structs['goles_anio_torneo']
    mapa_torneos = me.getValue(mp.get(mapa_anios,anio))
    lista_torneos = me.getValue(mp.get(mapa_torneos,torneo))
    paises = {}
    ciudades = {}
    mapa_equipos = mp.newMap(numelements=lt.size(lista_torneos), maptype='PROBING', loadfactor=0.5)

    for partido in lt.iterator(lista_torneos):
        if partido["city"] in ciudades:
            ciudades[partido["city"]] += 1
        else:
            ciudades[partido["city"]] = 1
        paises[partido["country"]] = 1

        if mp.contains(mapa_equipos,partido["home_team"]):
            equipo_local = me.getValue(mp.get(mapa_equipos,partido["home_team"]))
            equipo_local["equipo"] = partido["home_team"]
            equipo_local["partidos"] += 1
            if mp.contains(mapa_goles_fecha,partido["date"]+"-"+partido["home_team"]+"-"+partido["away_team"]+"-"+partido["home_team"]): 
                gol = me.getValue(mp.get(mapa_goles_fecha,partido["date"]+"-"+partido["home_team"]+"-"+partido["away_team"]+"-"+partido["home_team"]))
                if gol["penalty"] == "True":
                    equipo_local["penalties"] += 1
                if gol["own_goal"] == "True":
                    equipo_local["autogoles"] += 1
            equipo_local["goles_favor"] += int(partido["home_score"])
            equipo_local["goles_contra"] += int(partido["away_score"])
            if int(partido["home_score"]) > int(partido["away_score"]):
                equipo_local["victorias"] += 1
                equipo_local["puntos"] += 3
            elif int(partido["home_score"]) < int(partido["away_score"]):
                equipo_local["derrotas"] += 1
            else:
                equipo_local["empates"] += 1
                equipo_local["puntos"] += 1

        else:
            equipo_local = diccionarios_req_6()
            equipo_local["equipo"] = partido["home_team"]
            equipo_local["partidos"] += 1
            if mp.contains(mapa_goles_fecha,partido["date"]+"-"+partido["home_team"]+"-"+partido["away_team"]+"-"+partido["home_team"]): 
                gol = me.getValue(mp.get(mapa_goles_fecha,partido["date"]+"-"+partido["home_team"]+"-"+partido["away_team"]+"-"+partido["home_team"]))
                if gol["penalty"] == "True":
                    equipo_local["penalties"] += 1
                if gol["own_goal"] == "True":
                    equipo_local["autogoles"] += 1
            equipo_local["goles_favor"] += int(partido["home_score"])
            equipo_local["goles_contra"] += int(partido["away_score"])
            if int(partido["home_score"]) > int(partido["away_score"]):
                equipo_local["victorias"] += 1
                equipo_local["puntos"] += 3
            elif int(partido["home_score"]) < int(partido["away_score"]):
                equipo_local["derrotas"] += 1
            else:
                equipo_local["empates"] += 1
                equipo_local["puntos"] += 1
            
            mp.put(mapa_equipos,partido["home_team"],equipo_local)
        
        if mp.contains(mapa_equipos,partido["away_team"]):
            equipo_visitante = me.getValue(mp.get(mapa_equipos,partido["away_team"]))
            equipo_visitante["equipo"] = partido["away_team"]
            equipo_visitante["partidos"] += 1
            if mp.contains(mapa_goles_fecha,partido["date"]+"-"+partido["home_team"]+"-"+partido["away_team"]+"-"+partido["away_team"]): 
                gol = me.getValue(mp.get(mapa_goles_fecha,partido["date"]+"-"+partido["home_team"]+"-"+partido["away_team"]+"-"+partido["away_team"]))
                if gol["penalty"] == "True":
                    equipo_visitante["penalties"] += 1
                if gol["own_goal"] == "True":
                    equipo_visitante["autogoles"] += 1
            equipo_visitante["goles_favor"] += int(partido["away_score"])
            equipo_visitante["goles_contra"] += int(partido["home_score"])
            if int(partido["home_score"]) < int(partido["away_score"]):
                equipo_visitante["victorias"] += 1
                equipo_visitante["puntos"] += 3
            elif int(partido["home_score"]) > int(partido["away_score"]):
                equipo_visitante["derrotas"] += 1
            else:
                equipo_visitante["empates"] += 1
                equipo_visitante["puntos"] += 1

        else:
            equipo_visitante = diccionarios_req_6()
            equipo_visitante["equipo"] = partido["away_team"]
            equipo_visitante["partidos"] += 1
            if mp.contains(mapa_goles_fecha,partido["date"]+"-"+partido["home_team"]+"-"+partido["away_team"]+"-"+partido["away_team"]):
                gol = me.getValue(mp.get(mapa_goles_fecha,partido["date"]+"-"+partido["home_team"]+"-"+partido["away_team"]+"-"+partido["away_team"]))
                if gol["penalty"] == "True":
                    equipo_visitante["penalties"] += 1
                if gol["own_goal"] == "True":
                    equipo_visitante["autogoles"] += 1
            equipo_visitante["goles_favor"] += int(partido["away_score"])
            equipo_visitante["goles_contra"] += int(partido["home_score"])
            if int(partido["home_score"]) < int(partido["away_score"]):
                equipo_visitante["victorias"] += 1
                equipo_visitante["puntos"] += 3
            elif int(partido["home_score"]) > int(partido["away_score"]):
                equipo_visitante["derrotas"] += 1
            else:
                equipo_visitante["empates"] += 1
                equipo_visitante["puntos"] += 1

            mp.put(mapa_equipos,partido["away_team"],equipo_visitante)

    lista_equipos = lt.newList('ARRAY_LIST')

    for equipo in lt.iterator(mp.keySet(mapa_equipos)):
        lt.addLast(lista_equipos,me.getValue(mp.get(mapa_equipos,equipo)))
    quk.sort(lista_equipos,compare_equipos_req6)

    if lt.size(lista_equipos) > n_equipos:
        lista_equipos = lt.subList(lista_equipos, 1, n_equipos)

    if lt.size(lista_equipos) > 6:
        lista_equipos_final = lt.subList(lista_equipos, 1, 3)
        for equipo in lt.iterator(lt.subList(lista_equipos,lt.size(lista_equipos)-2 , 3)):
            lt.addLast(lista_equipos_final, equipo)
    else:
        lista_equipos_final = lista_equipos

    for equipo in lt.iterator(lista_equipos_final):
        nom_equipo = equipo["equipo"]
        goleadores = {"":0}
        for goles in lt.iterator(mp.keySet(mapa_goles_fecha)):
            gol = me.getValue(mp.get(mapa_goles_fecha,goles))
            if gol["team"] == nom_equipo:
                if gol["scorer"] in goleadores:
                    goleadores[gol["scorer"]] += 1
                else:
                    goleadores[gol["scorer"]] = 1
        maximo_goleador = max(goleadores, key=goleadores.get)

        equipo["jugador_mas_goles"] = {"nombre":maximo_goleador,"goles":goleadores[maximo_goleador]}

    return mp.size(mapa_anios),mp.size(mapa_torneos),mp.size(mapa_equipos),lt.size(lista_torneos),len(paises),len(ciudades),max(ciudades, key=ciudades.get),lista_equipos_final

def req_7(data_structs, n_players, start_d, end_d):
    date_frmt1 = [int(x) for x in start_d.split('-')]
    date_frmt2 = [int(x) for x in end_d.split('-')]
    start_d = date(*date_frmt1)
    end_d = date(*date_frmt2)

    players = mp.newMap(numelements=lt.size(data_structs['match_results_alphabetically']), maptype='PROBING', loadfactor=0.5)
    matches = lt.newList('ARRAY_LIST', cmpfunction=compare_matches)
    tournaments = mp.newMap(numelements=lt.size(data_structs['match_results_alphabetically']), maptype='CHAINING', loadfactor=0.5)
    total_scores = 0
    total_penalties = 0
    total_own_goals = 0

    for entry in mp.iterator(data_structs['match_results_alphabetically']):
        match = entry['value']
        match_date = date(*[int(x) for x in match['date'].split('-')])

        if match['tournament'] != 'Friendly' and start_d <= match_date <= end_d:
            lt.addLast(matches, match)
            total_scores += int(match['away_score']) + int(match['home_score'])
            mp.put(tournaments, match['tournament'], match['tournament'])

    for entry in lt.iterator(data_structs['scores']):
        score = entry['value']
        score_match = {'date': score['date'], 'away_team': score['away_team'], 'home_team': score['home_team']}
        pos = get_mresult(matches, score_match)

        if pos:
            match = lt.getElement(matches, pos)
            player_pos = mp.isPresent(players, score)

            if not player_pos:
                player = {
                    'scorer': score['scorer'],
                    'total_points': 0,
                    'total_goals': 0,
                    'penalty_goals': 0,
                    'own_goals': 0,
                    'avg_time': 0,
                    'total_tournaments': lt.newList('ARRAY_LIST', compare_string),
                    'scored_in_wins': 0,
                    'scored_in_losses': 0,
                    'scored_in_draws': 0,
                    'last_goal': lt.newList('ARRAY_LIST')
                }
                lt.addLast(players, player)
                player_pos = mp.size(players)

            modify_player = lt.getElement(players, player_pos)['value']
            modify_player['total_goals'] += 1
            modify_player['total_points'] += 1

            if score['penalty'] == 'True':
                modify_player['penalty_goals'] += 1
                modify_player['total_points'] += 1
                total_penalties += 1

            if score['own_goal'] == 'True':
                modify_player['own_goals'] += 1
                modify_player['total_points'] -= 1
                total_own_goals += 1

            if score['minute']:
                modify_player['avg_time'] = ((modify_player['avg_time'] * (modify_player['total_goals'] - 1) / modify_player['total_goals']) + (float(score['minute']) / modify_player['total_goals']))

            tournament = mp.isPresent(modify_player['total_tournaments'], match['tournament'])
            if not tournament:
                lt.addLast(modify_player['total_tournaments'], match['tournament'])

            winner = winner_determiner(match)
            team_that_scored = scorer_team(score)

            if winner == 'home':
                if team_that_scored == 'home':
                    modify_player['scored_in_wins'] += 1
                elif team_that_scored == 'away':
                    modify_player['scored_in_losses'] += 1
            elif winner == 'draw':
                modify_player['scored_in_draws'] += 1
            elif winner == 'away':
                if team_that_scored == 'away':
                    modify_player['scored_in_wins'] += 1
                elif team_that_scored == 'home':
                    modify_player['scored_in_losses'] += 1

            lt.addLast(modify_player['last_goal'], score)
            lt.changeInfo(players, player_pos, modify_player)

    merg.sort(players, req7_sort_criteria)

    if lt.size(players) < n_players:
        best_players = players
    else:
        best_players = lt.subList(players, 1, n_players)

    best_players_modified = lt.newList('ARRAY_LIST')

    for entry in lt.iterator(best_players):
        player = entry['value']
        player['total_tournaments'] = lt.size(player['total_tournaments'])
        player['last_goal'] = lt.getElement(player['last_goal'], 1)
        lt.addLast(best_players_modified, player)

    length = lt.size(best_players)

    if lt.size(best_players) > 6:
        firstelements = [lt.getElement(best_players_modified, x) for x in range(1, 4)]
        lastelements = [lt.getElement(best_players_modified, x) for x in range(length - 2, length + 1)]
        elements = firstelements + lastelements
    else:
        elements = [entry['value'] for entry in lt.iterator(best_players_modified)]

    player_num = lt.size(players)
    n_matches = lt.size(matches)
    n_tournaments = mp.size(tournaments)

    return player_num, n_matches, n_tournaments, total_scores, total_penalties, total_own_goals, elements
    pass



def req_8(data_structs, team1, team2, start_d, end_d):
    date_frmt1 = ([int(x) for x in (start_d.split('-'))])
    date_frmt2 = ([int(x) for x in (end_d.split('-'))])
    start_d = date(*date_frmt1)
    end_d = date(*date_frmt2)
    #.

    years_1 = mp.newMap(numelements=lt.size(data_structs['match_results']), maptype='PROBING', loadfactor=0.5)
    matches_1 = lt.newList('ARRAY_LIST', cmpfunction=compare_matches)
    home_matches1 = 0
    away_matches1 = 0

    years_2 = mp.newMap(numelements=lt.size(data_structs['match_results']), maptype='PROBING', loadfactor=0.5)
    matches_2 = lt.newList('ARRAY_LIST', cmpfunction=compare_matches)
    home_matches2 = 0
    away_matches2 = 0

    joint_wins1 = 0
    joint_wins2 = 0
    joint_losses1 = 0
    joint_losses2 = 0
    joint_draws = 0
    joint_matches = lt.newList('ARRAY_LIST', cmpfunction=compare_matches)
    joint_scores = lt.newList('ARRAY_LIST')

    for entry in lt.iterator(data_structs['match_results']):
        match = entry['value']
        if match['tournament'] != 'Friendly' and start_d < match['date'] < end_d:
            if match['away_team'] == team1 or match['home_team'] == team1:
                lt.addLast(matches_1, match)
                year = mp.isPresent(years_1, match['date'].year)

                if not year:
                    new_year = {
                        'year': match['date'].year,
                        'matches': 0,
                        'total_points': 0,
                        'goal_difference': 0,
                        'penalties': 0,
                        'own_goals': 0,
                        'wins': 0,
                        'draws': 0,
                        'losses': 0,
                        'goals_for': 0,
                        'goals_against': 0,
                        'top_scorer': lt.newList('ARRAY_LIST', compare_players)
                    }
                    lt.addLast(years_1, new_year)
                    year = mp.size(years_1)

                winner = winner_determiner(match)
                modify_year = lt.getElement(years_1, year)
                modify_year['matches'] += 1

                if match['away_team'] == team1:
                    away_matches1 += 1

                    if winner == 'away':
                        modify_year['total_points'] += 3
                        modify_year['wins'] += 1
                    elif winner == 'draw':
                        modify_year['total_points'] += 1
                        modify_year['draws'] += 1
                    elif winner == 'home':
                        modify_year['losses'] += 1

                    modify_year['goals_for'] += int(match['away_score'])
                    modify_year['goals_against'] += int(match['home_score'])
                    modify_year['goal_difference'] += int(match['away_score']) - int(match['home_score'])

                elif match['home_team'] == team1:
                    home_matches1 += 1

                    if winner == 'away':
                        modify_year['losses'] += 1
                    elif winner == 'draw':
                        modify_year['total_points'] += 1
                        modify_year['draws'] += 1
                    elif winner == 'home':
                        modify_year['wins'] += 1
                        modify_year['total_points'] += 3

                    modify_year['goals_for'] += int(match['home_score'])
                    modify_year['goals_against'] += int(match['away_score'])
                    modify_year['goal_difference'] += int(match['home_score']) - int(match['away_score'])

                lt.changeInfo(years_1, year, modify_year)

            if match['away_team'] == team2 or match['home_team'] == team2:
                lt.addLast(matches_2, match)
                year = mp.isPresent(years_2, match['date'].year)

                if not year:
                    new_year = {
                        'year': match['date'].year,
                        'matches': 0,
                        'total_points': 0,
                        'goal_difference': 0,
                        'penalties': 0,
                        'own_goals': 0,
                        'wins': 0,
                        'draws': 0,
                        'losses': 0,
                        'goals_for': 0,
                        'goals_against': 0,
                        'top_scorer': lt.newList('ARRAY_LIST', compare_players)
                    }
                    lt.addLast(years_2, new_year)
                    year = mp.size(years_2)

                winner = winner_determiner(match)
                modify_year = lt.getElement(years_2, year)
                modify_year['matches'] += 1

                if match['away_team'] == team2:
                    away_matches2 += 1

                    if winner == 'away':
                        modify_year['total_points'] += 3
                        modify_year['wins'] += 1
                    elif winner == 'draw':
                        modify_year['total_points'] += 1
                        modify_year['draws'] += 1
                    elif winner == 'home':
                        modify_year['losses'] += 1

                    modify_year['goals_for'] += int(match['away_score'])
                    modify_year['goals_against'] += int(match['home_score'])
                    modify_year['goal_difference'] += int(match['away_score']) - int(match['home_score'])

                elif match['home_team'] == team2:
                    home_matches2 += 1

                    if winner == 'away':
                        modify_year['losses'] += 1
                    elif winner == 'draw':
                        modify_year['total_points'] += 1
                        modify_year['draws'] += 1
                    elif winner == 'home':
                        modify_year['wins'] += 1
                        modify_year['total_points'] += 3

                    modify_year['goals_for'] += int(match['home_score'])
                    modify_year['goals_against'] += int(match['away_score'])
                    modify_year['goal_difference'] += int(match['home_score']) - int(match['away_score'])

                lt.changeInfo(years_2, year, modify_year)

            if (match['away_team'] == team1 or match['home_team'] == team1) and (
                    match['away_team'] == team2 or match['home_team'] == team2):
                winner = winner_determiner(match)
                lt.addLast(joint_matches, match)

                if winner == 'draw':
                    joint_draws += 1
                elif match['away_team'] == team1:
                    if winner == 'away':
                        joint_wins1 += 1
                        joint_losses2 += 1
                    elif winner == 'home':
                        joint_wins2 += 1
                        joint_losses1 += 1
                elif match['home_team'] == team1:
                    if winner == 'away':
                        joint_wins2 += 1
                        joint_losses1 += 1
                    elif winner == 'home':
                        joint_wins1 += 1
                        joint_losses2 += 1

    for score in lt.iterator(data_structs['scores']):
        if start_d < score['date'] < end_d:
            if score['team'] == team1:
                pos = lt.isPresent(matches_1, score)

                if pos:
                    score_yr = {'year': score['date'].year}
                    year = mp.isPresent(years_1, score_yr)

                    if year:
                        modify_year = mp.get(years_1, year)

                        if score['own_goal'] == 'True':
                            modify_year['own_goals'] += 1

                        if score['penalty'] == 'True':
                            modify_year['penalties'] += 1

                        player = lt.isPresent(modify_year['top_scorer'], score)

                        if not player:
                            new_player = {
                                'scorer': score['scorer'],
                                'goals': 1,
                                'matches': lt.newList('ARRAY_LIST', compare_matches),
                                'avg_time': float(score['minute'])
                            }
                            lt.addLast(new_player['matches'], score)
                            lt.addLast(modify_year['top_scorer'], new_player)
                        else:
                            modify_player = lt.getElement(modify_year['top_scorer'], player)
                            modify_player['goals'] += 1
                            player_match = lt.isPresent(modify_player['matches'], score)

                            if not player_match:
                                lt.addLast(modify_player['matches'], score)

                            modify_player['avg_time'] = (
                                    (modify_player['avg_time'] * (modify_player['goals'] - 1) + float(score['minute'])) /
                                    modify_player['goals']
                            )

                            lt.changeInfo(modify_year['top_scorer'], player, modify_player)
                        mp.put(years_1, year, modify_year)

            if score['team'] == team2:
                pos = lt.isPresent(matches_2, score)

                if pos:
                    score_yr = {'year': score['date'].year}
                    year = mp.isPresent(years_2, score_yr)

                    if year:
                        modify_year = mp.get(years_2, year)

                        if score['own_goal'] == 'True':
                            modify_year['own_goals'] += 1

                        if score['penalty'] == 'True':
                            modify_year['penalties'] += 1

                        player = lt.isPresent(modify_year['top_scorer'], score)

                        if not player:
                            new_player = {
                                'scorer': score['scorer'],
                                'goals': 1,
                                'matches': lt.newList('ARRAY_LIST', compare_matches),
                                'avg_time': float(score['minute'])
                            }
                            lt.addLast(new_player['matches'], score)
                            lt.addLast(modify_year['top_scorer'], new_player)
                        else:
                            modify_player = lt.getElement(modify_year['top_scorer'], player)
                            modify_player['goals'] += 1
                            player_match = lt.isPresent(modify_player['matches'], score)

                            if not player_match:
                                lt.addLast(modify_player['matches'], score)

                            modify_player['avg_time'] = (
                                    (modify_player['avg_time'] * (modify_player['goals'] - 1) + float(score['minute'])) /
                                    modify_player['goals']
                            )

                            lt.changeInfo(modify_year['top_scorer'], player, modify_player)

                        mp.put(years_2, year, modify_year)

            if (score['away_team'] == team1 or score['home_team'] == team1) and (
                    score['away_team'] == team2 or score['home_team'] == team2):
                pos = lt.isPresent(joint_matches, score)

                if pos:
                    lt.addLast(joint_scores, score)

    length1 = mp.size(years_1)

    if length1 > 6:
        firstelements1 = [mp.get(years_1, x) for x in range(1, 4)]
        lastelements1 = [mp.get(years_1, x) for x in range(length1 - 2, length1 + 1)]
        elements1 = firstelements1 + lastelements1
    else:
        elements1 = [mp.get(years_1, x) for x in range(1, length1 + 1)]

    length2 = mp.size(years_2)

    if length2 > 6:
        firstelements2 = [mp.get(years_2, x) for x in range(1, 4)]
        lastelements2 = [mp.get(years_2, x) for x in range(length2 - 2, length2 + 1)]
        elements2 = firstelements2 + lastelements2
    else:
        elements2 = [mp.get(years_2, x) for x in range(1, length2 + 1)]

    for element in elements1:
        if lt.size(element['top_scorer']):
            element['top_scorer'] = lt.firstElement(element['top_scorer'])
            element['top_scorer']['matches'] = lt.size(element['top_scorer']['matches'])
        else:
            element['top_scorer'] = 'No scores registered for this year.'

    for element in elements2:
        if lt.size(element['top_scorer']):
            element['top_scorer'] = lt.firstElement(element['top_scorer'])
            element['top_scorer']['matches'] = lt.size(element['top_scorer']['matches'])
        else:
            element['top_scorer'] = 'No scores registered for this year.'

    n_years1 = mp.size(years_1)
    n_years2 = mp.size(years_2)
    n_matches1 = lt.size(matches_1)
    n_matches2 = lt.size(matches_2)
    oldest_date1 = lt.lastElement(matches_1)['date']
    oldest_date2 = lt.lastElement(matches_2)['date']
    newest_match1 = lt.firstElement(matches_1)
    newest_match2 = lt.firstElement(matches_2)
    n_joint_matches = lt.size(joint_matches)
    newest_joint_match = lt.firstElement(joint_matches)

    length_score = lt.size(joint_scores)

    if length_score > 6:
        firstelements = [lt.getElement(joint_scores, x) for x in range(1, 4)]
        lastelements = [lt.getElement(joint_scores, x) for x in range(length_score - 2, length_score + 1)]
        scores = firstelements + lastelements
    else:
        scores = [lt.getElement(joint_scores, x) for x in range(1, length_score + 1)]

    return n_years1, n_matches1, home_matches1, away_matches1, oldest_date1, newest_match1, elements1, n_years2, n_matches2, home_matches2, away_matches2, oldest_date2, newest_match2, elements2, n_joint_matches, joint_wins1, joint_losses1, joint_wins2, joint_losses2, joint_draws, newest_joint_match, scores




# Funciones utilizadas para comparar elementos dentro de una lista
def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    
    if (data_1['home_team']==data_2['home_team']) and data_2['away_team']==data_1['away_team'] and data_1['date']==data_2['date']:
        return 0
    elif data_1['date']>data_2['date']:
        return 1
    elif data_1['date']==data_2['date'] and data_1['home_team']<data_2['home_team']:
        return 1
    elif data_1['date']==data_2['date'] and data_1['home_team']==data_2['home_team'] and data_1['away_team']<data_2['away_team']:
        return 1
    return -1

def compare_string(data_1, data_2):
    if data_1 == data_2:
        return 0
    elif data_1>data_2:
        return 1
    return -1

def compare_teams(data_1, data_2):
    if data_1== data_2['team']:
        return 0
    elif data_1>data_2['team']:
        return 1
    return -1

def compare_players(data1,data2):
    if data1['scorer']==data2['scorer']:
        return 0
    elif data1['scorer']>data2['scorer']:
        return 1
    return -1

def compare_matches(data1, data2):
    if data1['date']==data2['date'] and data1['home_team']==data2['home_team'] and data1['away_team']== data2['away_team']:
        return 0
    elif data1['date']>data2['date']:
        return 1
    elif data1['date']==data2['date'] and data1['home_team']<data2['home_team']:
        return 1
    elif data1['date']==data2['date'] and data1['home_team']==data2['home_team'] and data1['away_team']<data2['away_team']:
        return 1
    return -1

def compare_years(data1, data2):
    if data1['year'] == data2['year']:
        return 0
    elif data1['year']>data2['year']:
        return 1
    return -1

def cmp_partidos_by_fecha_y_pais (resultado1, resultado2):
    """
Devuelve verdadero (True) si la fecha del resultado1 es menor que en el resultado2,
 en caso de que sean iguales tenga el nombre de la ciudad en que se disputó el partido,
 de lo contrario devuelva falso (False).
Args:
Resultado1: información del primer registro de resultados FIFA que incluye 
 “date” y el “country” 
impuesto2: información del segundo registro de resultados FIFA que incluye 
 “date” y el “count
 """
    date1 = resultado1['date']
    date2= resultado2['date']
    if date1<date2:
        return True
    elif date1==date2 and resultado1['city']<resultado2['city']:
        return True
    return False

# Funciones de ordenamiento


def match_sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    

    date1 = data_1
    date2 = data_2
    if date1>date2:
        return True
    return False

def scores_sort_criteria(data_1, data_2):
    date1 = data_1
    date2 = data_2
    if date1>date2:
        return True
    return False

def penalties_sort_criteria(data_1, data_2):
    date1 = data_1
    date2 = data_2
    if date1>date2:
        return True
    return False

def req2_sort_criteria(data_1, data_2):
    date1 = data_1['date']
    date2 = data_2['date']
    if date1<date2:
        return True
    return False
def req3_sort_criteria(data_1, data_2):
    date_1, home_1, away1 = data_1['date'], data_1['home_team'], data_1['away_team']
    date_2, home_2, away2 = data_2['date'], data_2['home_team'], data_2['away_team']
    if date_1>date_2:
        return True
    elif date_1 == date_2:
        if home_1 > home_2:
            return True
        elif home_1 == home_2:
            if away1 > away2:
                return True 
    return False
def req4_sort_criteria(data_1, data_2):
    date1 = data_1['date']
    date2 = data_2['date']
    if date1>date2:
        return True
    elif date1==date2 and data_1['country']<data_2['country']:
        return True
    elif date1==date2 and data_1['country']==data_2['country'] and data_1['city']<data_2['city']:
        return True
    return False

def req6_sort_criteria(data1, data2):
    if data1['points']>data2['points']:
        return True
    elif data1['points']==data2['points'] and data1['score_dif']>data2['score_dif']:
        return True
    elif data1['points']==data2['points'] and data1['score_dif']==data2['score_dif'] and data1['penalties']>data2['penalties']:
        return True
    elif data1['points']==data2['points'] and data1['score_dif']==data2['score_dif'] and data1['penalties']==data2['penalties'] and data1['n_matches']<data2['n_matches']:
        return True
    elif data1['points']==data2['points'] and data1['score_dif']==data2['score_dif'] and data1['penalties']==data2['penalties'] and data1['n_matches']==data2['n_matches'] and data1['own_goals']<data2['own_goals']:
        return True
    return False

def req7_sort_criteria(data1,data2):
    if data1['total_points']>data2['total_points']:
        return True
    elif data1['total_points']==data2['total_points'] and data1['total_goals']>data2['total_goals']:
        return True
    elif data1['total_points']==data2['total_points'] and data1['total_goals']==data2['total_goals'] and data1['penalty_goals']>data2['penalty_goals']:
        return True
    elif data1['total_points']==data2['total_points'] and data1['total_goals']==data2['total_goals'] and data1['penalty_goals']==data2['penalty_goals'] and data1['own_goals']<data2['own_goals']:
        return True
    elif data1['total_points']==data2['total_points'] and data1['total_goals']==data2['total_goals'] and data1['penalty_goals']==data2['penalty_goals'] and data1['own_goals']==data2['own_goals'] and data1['avg_time']<data2['avg_time']:
        return True
    return False

def top_scorer_sort_criteria(data1, data2):
    if data1['goals']>data2['goals']:
        return True
    elif data1['goals']==data2['goals'] and lt.size(data1['matches'])>lt.size(data2['matches']):
        return True
    elif data1['goals']==data2['goals'] and lt.size(data1['matches'])==lt.size(data2['matches']) and data1['avg_time']<data2['avg_time']:
        return True
    return False

def match_sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    partidos = lt.newList('ARRAY_LIST')
    match_keys = data_structs['lista_match_results']
    quk.sort(match_keys, match_sort_criteria)
    if lt.size(match_keys) < 6:
        for key in lt.iterator(match_keys):
            valor = me.getValue(mp.get(data_structs['match_results'], key))
            lt.addLast(partidos,valor)
    else:
        sup = lt.subList(match_keys, 1, 3)
        inf = lt.subList(match_keys, lt.size(match_keys)-2, 3)
        for key in lt.iterator(sup):
            valor = me.getValue(mp.get(data_structs['match_results'], key))
            lt.addLast(partidos,valor)

        for key in lt.iterator(inf):
            valor = me.getValue(mp.get(data_structs['match_results'], key))
            lt.addLast(partidos,valor)

    return partidos

def scores_sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    scorers = lt.newList('ARRAY_LIST')
    score_keys = data_structs['lista_scores']
    quk.sort(score_keys, scores_sort_criteria)
    if lt.size(score_keys) < 6:
        for key in lt.iterator(score_keys):
            valor = me.getValue(mp.get(data_structs['scores'], key))
            lt.addLast(scorers,valor)
    else:
        sup = lt.subList(score_keys, 1, 3)
        inf = lt.subList(score_keys, lt.size(score_keys)-2, 3)
        for key in lt.iterator(sup):
            valor = me.getValue(mp.get(data_structs['scores'], key))
            lt.addLast(scorers,valor)

        for key in lt.iterator(inf):
            valor = me.getValue(mp.get(data_structs['scores'], key))
            lt.addLast(scorers,valor)

    return scorers

def penalties_sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    penaltys = lt.newList('ARRAY_LIST')
    penalty_keys = data_structs['lista_penalties']
    quk.sort(penalty_keys, penalties_sort_criteria)
    if lt.size(penalty_keys) < 6:
        for key in lt.iterator(penalty_keys):
            valor = me.getValue(mp.get(data_structs['penalties'], key))
            lt.addLast(penaltys,valor)
    else:
        sup = lt.subList(penalty_keys, 1, 3)
        inf = lt.subList(penalty_keys, lt.size(penalty_keys)-2, 3)
        for key in lt.iterator(sup):
            valor = me.getValue(mp.get(data_structs['penalties'], key))
            lt.addLast(penaltys,valor)

        for key in lt.iterator(inf):
            valor = me.getValue(mp.get(data_structs['penalties'], key))
            lt.addLast(penaltys,valor)

    return penaltys

def winner_determiner(data):
    #Retorna el ganador de un partido. Retorna draw si es empate.
    if data['home_score']> data['away_score']:
        return 'home'
    elif data['home_score']== data['away_score']:
        return 'draw'
    elif data['home_score']<data['away_score']:
        return 'away'

def scorer_team(data):
    if data['team']==data['home_team']:
        return 'home'
    elif data['team']==data['away_team']:
        return 'away'

def create_new_team(name):
    team = {'team':name, 
            'points':0, 
            'score_dif':0,
            'n_matches':0,
            'penalties':0,
            'own_goals':0,
            'victories':0,
            'draws':0,
            'defeats':0,
            'scores':0,
            'scores_received':0, 
            'top_scorer':lt.newList('ARRAY_LIST', cmpfunction=compare_players)}
    return team

def compare_goals_jugador_req2(data1, data2):
    if data1['date'] < data2['date']:
        return True
    return False

def compare_goals_jugador_req5(data1, data2):
    if data1['date'] > data2['date']:
        return True
    return False

def diccionarios_req_6():
    dicc = {
        "equipo":"",
        "partidos":0,
        "penalties":0,
        "autogoles":0,
        "victorias":0,
        "derrotas":0,
        "empates":0,
        "puntos":0,
        "goles_favor":0,
        "goles_contra":0,
        "jugador_mas_goles":{},
    }

    return dicc

def compare_equipos_req6(data1,data2):
    if data1["puntos"]>data2["puntos"]:
        return True
    elif data1["puntos"]==data2["puntos"]:
        if data1["goles_favor"]>data2["goles_favor"]:
            return True
        elif data1["goles_favor"]==data2["goles_favor"]:
            if data1["penalties"]>data2["penalties"]:
                return True
            elif data1["penalties"]==data2["penalties"]:
                if data1["partidos"]<data2["partidos"]:
                    return True
                elif data1["partidos"]==data2["partidos"]:
                    if data1["autogoles"]<data2["autogoles"]:
                        return True
    return False