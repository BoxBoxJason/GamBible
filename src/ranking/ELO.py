# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: Ranking
Module:  ELO
Version: 2.0
Usage: Provides all ELO algorithm functionalities, allows for player ranking and games processing

Author: BoxBoxJason
Date: 01/10/2023
'''
import logging
from json import load,dump
from numpy import linspace
from resources.PathEnum import getDBPath
from ranking.general import orderGamesTable

START_ELO = 1500

def processGames(output_file_path,games_table,players_table,base_points,beginner_multiplier,low_elo_multiplier,commit=False):
    """
    @brief Processes all unprocessed game in the database

    @param (path) output_file_path : Absolute path to database output file
    @param (dict[]) games_table : list of games
    @param (dict) players_table : dict of players
    @param (float) base_points : ELO algorithm base points
    @param (float) beginner_multiplier : ELO algorithm beginner multiplier
    @param (float) low_elo_multiplier : ELO algorithm low_elo_multiplier
    @param (bool) commit : states if changes made should be commited to database or not

    @return (float) Correct game output predictions %
    """

    total_number_games = 0
    correct_predictions = 0
    games_ordered_ids = orderGamesTable(games_table)

    for game_id in games_ordered_ids:
        game_dict = games_table[game_id]
        if not game_dict['PROCESSED']:
            total_number_games += 1
            correct_predictions += processGame(game_dict,players_table,base_points,beginner_multiplier,low_elo_multiplier)

    if commit:
        with open(output_file_path,'w',encoding='utf-8') as db_file:
            dump({'GAMES':games_table,'PLAYERS':players_table},db_file)

    success_rate = 0
    if total_number_games != 0:
        success_rate = correct_predictions / total_number_games
    return success_rate


def processGame(game_dict,players_table,base_points,beginner_multiplier,low_elo_multiplier):
    """
    @brief Processes a game, updates the player ELO accordingly

    @param (Game row) game : Game exinsting row object
    """
    winner_dict = players_table[game_dict['WINNER_ID']]
    loser_dict = players_table[game_dict['LOSER_ID']]
    ### Variables ### (Could optimize but would lose clarity)
    # Predicted probability of player 1 winning
    probWin1 = determineWinProbability(winner_dict['ELO'], loser_dict['ELO'])
    # Predicted probability of player 2 winning
    probWin2 = 1 - probWin1
    # Difference between expected and reality for player 1
    gameDiff1 = 1 - probWin1
    # Difference between expected and reality for player 2
    gameDiff2 = - probWin2

    ### New evaluation ###
    winner_dict['ELO'] += getPlayerGrowthCoeff(len(winner_dict['GAMES']),base_points,beginner_multiplier,low_elo_multiplier) * gameDiff1
    winner_dict['GAMES'].append(game_dict['ID'])
    loser_dict['ELO'] += getPlayerGrowthCoeff(len(loser_dict['GAMES']),base_points,beginner_multiplier,low_elo_multiplier) * gameDiff2
    loser_dict['GAMES'].append(game_dict['ID'])

    terrain = game_dict.get('TERRAIN')

    if terrain:
        winner_terrains = winner_dict['FAV_TERRAIN']
        if terrain in winner_terrains:
            winner_terrains[terrain]['WIN'] += 1
        else:
            winner_terrains[terrain] = {'WIN':1,'LOSS':0,'DRAW':0}

        loser_terrains = loser_dict['FAV_TERRAIN']
        if terrain in loser_terrains:
            loser_terrains[terrain]['LOSS'] += 1
        else:
            loser_terrains[terrain] = {'LOSS':1,'WIN':0,'DRAW':0}

    game_dict['PROCESSED'] = True
    return probWin1 > probWin2


def determineWinProbability(ELO1,ELO2):
    """
    @brief Calculates the win factor for a game between two given ELO (ELO algorithm)

    @param (float) ELO1 : first player ELO
    @param (float) ELO2 : second player ELO

    @return (float) Predicted win probability (for player 1)
    """
    elo_diff = ELO1 - ELO2
    # Formula used to compute win probability for player 1
    return 1 / (1 + 10 ** (-elo_diff / 400))


def getPlayerGrowthCoeff(player_games_count,base_points,beginner_multiplier,low_elo_multiplier):
    """
    @brief Returns a player's growth coeff based on the ELO algorithm

    @param (Player row) player : Player database row
    @param (float) base_points : default player growth coeff (ELO algorithm)
    @param (float) beginner_multiplier : beginner player growth coeff multiplier (ELO algorithm)
    @param (float) low_elo_multiplier : multiplier for non beginner low elo players (ELO algorithm)

    @return (float) player's growth coefficient (ELO algorithm)
    """
    if player_games_count < 30: # Beginner
        K = base_points * beginner_multiplier
    elif player_games_count < 2400: # Low ELO
        K = base_points * low_elo_multiplier
    else: # Master
        K = base_points

    return K


def optimizeGrowthCoeff(sport,category):
    """
    @brief Hyperparemeter optimization algorithm, tests a large number of configurations and logs the succes rate into database

    @param (str) sport : sport name (must correspond to existing folder)
    @param (str) category : category name (must correspond to existing folder)
    """
    logging.info('Starting ELO algorithm hyperparameter optimization')

    config_path = getDBPath(sport,category,'configurationELO.json')
    with open(config_path,'r',encoding='utf-8') as config_file:
        configurations_table = load(config_file)

    base_points_range = linspace(30,40)
    beginner_multiplier_range = linspace(0.1,10)
    #low_elo_multiplier_range = linspace(1,10)
    low_elo_multiplier = 1

    for base_points in base_points_range:
        for beginner_multiplier in beginner_multiplier_range:
            config_id = f"{base_points}-{beginner_multiplier}-{low_elo_multiplier}"
            if not config_id in configurations_table:

                db_path = getDBPath(sport,category,'defaultELO.json')
                with open(db_path,'r',encoding='utf-8') as input_file:
                    gambible_db = load(input_file)
                success_rate = processGames(db_path,gambible_db['GAMES'],gambible_db['PLAYERS'],base_points,beginner_multiplier,low_elo_multiplier)
                
                configurations_table[config_id] = {
                    'BASE_POINTS':base_points,
                    'BEGINNER_MULTIPLIER':beginner_multiplier,
                    'LOW_ELO_MULTIPLIER':low_elo_multiplier,
                    'SUCCESS_RATE':success_rate
                }
                logging.debug(f"Success rate={success_rate} for base_points={base_points}, beginner_multiplier={beginner_multiplier}, low_elo_multiplier={low_elo_multiplier}")
                with open(config_path,'w',encoding='utf-8') as config_output:
                    dump(configurations_table,config_output)
