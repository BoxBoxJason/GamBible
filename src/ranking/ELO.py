# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: Ranking
Module:  ELO
Version: 2.0
Usage: Provides all ELO algorithm functionalities, allows for player ranking and games processing.

Author: BoxBoxJason
Date: 01/10/2023
'''
import logging
from optuna import load_study,create_study
from resources.PathEnum import getDBPath,getJsonObject,dumpJsonObject
from ranking.general import orderGamesTable

START_ELO = 1500

def processGames(output_file_path,games_table,players_table,base_points,beginner_multiplier,low_elo_multiplier,commit=False,games_ordered_ids=None):
    """
    Process all unprocessed games in the database.

    :param str output_file_path: Absolute path to the database output file.
    :param list[dict] games_table: List of games.
    :param dict players_table: Dictionary of players.
    :param float base_points: ELO algorithm base points.
    :param float beginner_multiplier: ELO algorithm beginner multiplier.
    :param float low_elo_multiplier: ELO algorithm low_elo_multiplier.
    :param bool commit: States if changes made should be committed to the database or not (default True).

    :return: float - Correct game output predictions percentage.
    """

    total_number_games = 0
    correct_predictions = 0
    if games_ordered_ids is None:
        games_ordered_ids = orderGamesTable(games_table)

    for game_id in games_ordered_ids:
        game_dict = games_table[game_id]
        if not game_dict['PROCESSED']:
            total_number_games += 1
            correct_predictions += processGame(game_dict,players_table,base_points,beginner_multiplier,low_elo_multiplier)

    if commit:
        dumpJsonObject({'GAMES':games_table,'PLAYERS':players_table},output_file_path)

    success_rate = 0
    if total_number_games != 0:
        success_rate = correct_predictions / total_number_games
    return success_rate


def processGame(game_dict,players_table,base_points,beginner_multiplier,low_elo_multiplier):
    """
    Processes a game, updates the player ELO accordingly.

    :param dict game_dict: Game table dict.
    :param dict players_table: Database players table.
    :param float base_points: ELO algorithm base points.
    :param float beginner_multiplier: ELO algorithm beginner multiplier.
    :param float low_elo_multiplier: ELO algorithm low elo multiplier.

    :return: bool - ELO algorithm prediction was correct.
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
    Calculates the win factor for a game between two given ELO (ELO algorithm).

    :param float ELO1: First player ELO.
    :param float ELO2: Second player ELO.

    :return: float - Predicted win probability (for player 1).
    """
    elo_diff = ELO1 - ELO2
    # Formula used to compute win probability for player 1
    return 1 / (1 + 10 ** (-elo_diff / 400))


def getPlayerGrowthCoeff(player_games_count,base_points,beginner_multiplier,low_elo_multiplier):
    """
    Returns a player's growth coeff based on the ELO algorithm.

    :param int players_games_count: number of games played by a player.
    :param float base_points: ELO algorithm base points.
    :param float beginner_multiplier: ELO algorithm beginner multiplier.
    :param float low_elo_multiplier: ELO algorithm low elo multiplier.

    :return: float - Player's growth coefficient (ELO algorithm).
    """
    if player_games_count < 30: # Beginner
        K = base_points * beginner_multiplier
    elif player_games_count < 2400: # Low ELO
        K = base_points * low_elo_multiplier
    else: # Master
        K = base_points

    return K


def optimizeHyperparametersBayesian(sport,category):
    """
    Hyperparemeter optimization algorithm, tests a large number of configurations and logs the succes rate into database.

    :param str sport: Sport name (must correspond to existing folder).
    :param str category: Category name (must correspond to existing folder).
    """
    logging.info('Starting ELO algorithm hyperparameter optimization')

    db_path = getDBPath(sport,category,'defaultELO.json')
    games_ordered_ids = orderGamesTable(getJsonObject(db_path)['GAMES'])

    def objective(trial):
        base_points = trial.suggest_float('BASE_POINTS',1e-6,50)
        beginner_multiplier = trial.suggest_float('BEGINNER_MULTIPLIER',1e-6,15)
        low_elo_multiplier = trial.suggest_float('LOW_ELO_MULTIPLIER',1e-6,4)
        gambible_db = getJsonObject(db_path)
        success_rate = processGames(db_path,gambible_db['GAMES'],gambible_db['PLAYERS'],
                                    base_points,beginner_multiplier,low_elo_multiplier,False,games_ordered_ids)

        return success_rate

    study_name = f"{sport} MMR-{category} configuration"
    configuration_db_path = f"sqlite:///{getDBPath(sport,category,'configurationELO.db',False)}"

    try:
        study = load_study(study_name=study_name,storage=configuration_db_path)
    except:
        study = create_study(direction='maximize',study_name=study_name,storage=configuration_db_path)

    study.optimize(objective,n_trials=1000)
