# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: Ranking
Module:  ELO
Version: 2.0
Usage: Provides general functionalities for ranking algorithms, such as sorting by criteria and graph display

Author: BoxBoxJason
Date: 20/11/2023
'''

from matplotlib.pyplot import savefig,figure,show,Normalize

def orderGamesTable(games_table):
    """
    @brief Orders the games table by dates and returns them

    @param (dict) games_table : Database games table

    @return (dict[]) games list ordered by date
    """
    games_table_list = []
    for game_dict in games_table.values():
        games_table_list.append(game_dict)

    games_table_list.sort(key = lambda x : x['DATE'])
    for i,game_dict in enumerate(games_table_list):
        games_table_list[i] = game_dict['ID']

    return games_table_list


def orderConfigurationsTable(configurations_table):
    """
    @brief Orders the configurations table by success rate and returns them

    @param (dict) configurations_table : Database configuration table

    @return (dict[]) configurations list ordered by success rate
    """
    configurations_table_list = []
    for configuration_dict in configurations_table.values():
        configurations_table_list.append(configuration_dict)

    configurations_table_list.sort(key=lambda x: x['SUCCESS_RATE'])

    return configurations_table_list

def plotSuccessRate(config_table,X_key,Y_key):
    """

    """
    X_ticks_list = []
    Y_ticks_list = []
    Z_ticks_list = []
    for config_dict in config_table.values():
        X_ticks_list.append(config_dict[X_key])
        Y_ticks_list.append(config_dict[Y_key])
        Z_ticks_list.append(config_dict['SUCCESS_RATE'])

    norm = Normalize(min(Z_ticks_list),max(Z_ticks_list))
    fig = figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.scatter(X_ticks_list,Y_ticks_list,Z_ticks_list,c=Z_ticks_list,cmap='coolwarm',marker='o',norm=norm)
    ax.set_xlabel(X_key)
    ax.set_ylabel(Y_key)
    ax.set_zlabel('SUCCES RATE')
    ax.set_title('Success rate heatmap')
    savefig('heatmap.png')
    show()
