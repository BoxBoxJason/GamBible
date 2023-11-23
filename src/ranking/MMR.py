#-*- coding: utf-8 -*-
'''
Project : GamBible
Package: Ranking
Module:  MMR
Version: 2.0
Usage: Provides all MMR algorithm functionalities, allows for player ranking and games processing

Author: BoxBoxJason
Date: 13/10/2023
'''
from math import tanh,pi,sqrt
from copy import copy
import logging
from json import dump,load
from resources.utils import findZero
from resources.PathEnum import getDBPath
from ranking.general import orderGamesTable

# Player default skill value
START_SKILL = 1500
# Player default skill deviation (skill uncertainty)
START_DEVIATION = 350

def processGames(output_file_path,games_table,players_table,γ=0.5,β=0.5,ρ=1,commit=False):
    """
    Processes the entire history file and updates players dict with new games informations
    @param (dict) games_table : Database games table
    @param (dict) players_table : Database players_table
    @param (float) γ : Temporal diffusion [0,inf[
    @param (float) β : Performance deviation [0,inf[
    @param (float) ρ : 1/ρ Inverse momentum -> player ranking volatility in case of sudden level change
    @param (bool) commit : States if changes should be commited to database or not
    
    """
    logging.info('Processing new games')
    games_ordered_ids = orderGamesTable(games_table)

    total_processed_games = 0
    predicted_output = 0
    for game_id in games_ordered_ids:
        if not games_table[game_id]['PROCESSED']:
            total_processed_games += 1
            predicted_output += processGame(players_table,games_table[game_id],γ,β,ρ)

    if commit:
        with open(output_file_path,'w',encoding='utf-8') as output_file:
            dump({'GAMES':games_table,'PLAYERS':players_table},output_file)

    return predicted_output / total_processed_games


def processGame(players_table,game_dict,γ,β,ρ):
    """
    Updates all rankings according to game results
    @param (dict) playersDict : {playerId:Player}
    @param (str) gameId : unique game identifier
    @param (list) gameResults : list of players ids ranked by performance [playerIds]
    """
    # Adding unknown players to playersDict
    ranking_skills = [players_table[player_id]['SKILL'] - 3 * players_table[player_id]['SKILL_DEVIATION'] for player_id in game_dict['RANKING']]
    result_predicted = ranking_skills[0] == max(ranking_skills)

    for player_id in game_dict['RANKING']:
        diffuse(players_table[player_id],γ,ρ)
        players_table[player_id]['SKILL_DEVIATION'] = sqrt(players_table[player_id]['SKILL_DEVIATION'] ** 2 + β ** 2)

    new_dicts = []
    # Perform update in parallel
    for i in range(len(game_dict['RANKING'])):
        new_dicts.append(update([copy(players_table[player_id]) for player_id in game_dict['RANKING']],i,β))

    # Apply update
    for i,player_id in enumerate(game_dict['RANKING']):
        players_table[player_id] = new_dicts[i]

    game_dict['PROCESSED'] = True

    return result_predicted


def diffuse(player_dict,γ,ρ):
    """
    Updates changes in player skill
    @param (Player) player : player to update
    """
    ϰ = 1 / (1 + (γ / player_dict['SKILL_DEVIATION']) ** 2)
    wg = ϰ ** ρ * player_dict['PERF_WEIGHT'][0]
    wl = (1 - ϰ ** ρ) * sum(player_dict['PERF_WEIGHT'])

    player_dict['PERF_HISTORY'][0] = (wg * player_dict['PERF_HISTORY'][0] + wl * player_dict['SKILL']) / (wg + wl)
    player_dict['PERF_WEIGHT'][0] = ϰ * (wg + wl)

    for i in range(len(player_dict['PERF_WEIGHT'])):
        player_dict['PERF_WEIGHT'][i] *= ϰ ** (1 + ρ)
    player_dict['SKILL_DEVIATION'] /= sqrt(ϰ)


def update(players_ranking,selected_player_index,β):
    """
    Updates the player average skill evaluation
    @param (dict[]) players_ranking : list of player dicts, order corresponds to game outcome
    @param (int) selectedPlayerIndex
    """
    p = getPerfEstimation(players_ranking, selected_player_index)
    players_ranking[selected_player_index]['PERF_HISTORY'].append(p)
    players_ranking[selected_player_index]['PERF_WEIGHT'].append(1 / β ** 2)

    players_ranking[selected_player_index]['SKILL'] = getAverageSkillEstimation(players_ranking[selected_player_index],β)

    return players_ranking[selected_player_index]


def getAverageSkillEstimation(player_dict,β):
    """
    Returns the (unique) zero of the player average skill
    @return (float)
    """
    def estimationFunction(x):
        val = player_dict['PERF_WEIGHT'][0] * (x - player_dict['PERF_HISTORY'][0])
        for game_index,perf_weight in enumerate(player_dict['PERF_WEIGHT']):
            val += perf_weight * β / (sqrt(3) / pi) * tanh((x - player_dict['PERF_HISTORY'][game_index]) / (2 * sqrt(3) / pi * β))

        return val

    return findZero(estimationFunction)


def getPerfEstimation(players_ranking,selected_player_index):
    """
    Returns the (unique) 0 of the players average performance for a game
    @return (float)
    """
    def estimationFunction(x):
        val = 0
        for player_dict in players_ranking[0:selected_player_index+1]:
            val += 1 / player_dict['SKILL_DEVIATION'] * (tanh((x - player_dict['SKILL']) / (2 * sqrt(3) / pi * player_dict['SKILL_DEVIATION'])) - 1)

        for player_dict in players_ranking[selected_player_index:]:
            val += 1 / player_dict['SKILL_DEVIATION'] * (tanh((x - player_dict['SKILL']) / (2 * sqrt(3) / pi * player_dict['SKILL_DEVIATION'])) + 1)

        return val

    return findZero(estimationFunction)


def createGame(games_table,players_table,game_id,game_date,game_ranking):
    """
    @brief Creates a new game dict in the games table

    @param (dict) games_table : Database games table
    @param (dict) players_table : Database players table
    @param (str) game_id : game (unique) id
    @param (str) game_date : game date
    @param (int[]) game_ranking : list of player ids ranked (winner is first, loser is last)
    """
    games_table[game_id] = {
    'ID':game_id,
    'DATE':game_date,
    'RANKING':game_ranking,
    'PROCESSED':False
    }

    for player_id in game_ranking:
        players_table[player_id]['GAMES'].append(game_id)


def optimizeHyperparameters(sport,category):
    """
    @brief Hyperparemeter optimization algorithm, tests a large number of configurations and logs the succes rate into database

    @param (str) sport : sport name (must correspond to existing folder)
    @param (str) category : category name (must correspond to existing folder)
    """
    logging.info('Starting MMR algorithm hyperparameters optimization')

    config_path = getDBPath(sport,category,'configurationMMR.json')
    with open(config_path,'r',encoding='utf-8') as config_file:
        configurations_table = load(config_file)

    γ_range = [1]
    β_range = [0.001]
    ρ_range = [10000]

    for γ in γ_range:
        for β in β_range:
            for ρ in ρ_range:
                config_id = f"{γ}-{β}-{ρ}"
                if not config_id in configurations_table:

                    db_path = getDBPath(sport,category,'defaultMMR.json')
                    with open(db_path,'r',encoding='utf-8') as input_file:
                        gambible_db = load(input_file)
                    success_rate = processGames(db_path,gambible_db['GAMES'],gambible_db['PLAYERS'],γ,β,ρ)

                    configurations_table[config_id] = {
                        'TEMPORAL_DIFFUSION':γ,
                        'PERFORMANCE_DEVIATION':β,
                        'INVERSE_MOMENTUM':ρ,
                        'SUCCESS_RATE':success_rate
                    }
                    logging.debug(f"Success rate={success_rate} for TEMPORAL_DIFFUSION={γ}, PERFORMANCE_DEVIATION={β}, INVERSE_MOMENTUM={ρ}")
                    with open(config_path,'w',encoding='utf-8') as config_output:
                        dump(configurations_table,config_output)
