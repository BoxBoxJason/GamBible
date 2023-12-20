# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: Ranking
Module:  general
Version: 2.0
Usage: Provides general functionalities for ranking algorithms, such as sorting by criteria and graph display.

Author: BoxBoxJason
Date: 20/11/2023
'''

from matplotlib.pyplot import savefig,figure,show,Normalize

def orderGamesTable(games_table):
    """
    Orders the Games table by dates and returns an ordered list of Games ids.

    :param dict games_table: Database Games table.

    :return: list[dict] - Games dictionaries list ordered by date.
    """
    games_table_list = list(games_table.values())

    games_table_list.sort(key = lambda x : x['DATE'])

    return [game_dict['ID'] for game_dict in games_table_list]


def orderConfigurationsTable(configurations_table):
    """
    Orders the configurations table by success rate and returns them.

    :param dict configurations_table: Database configurations table.

    :return: list[dict] - Configurations list ordered by success rate.
    """
    configurations_table_list = list(configurations_table.values())
    configurations_table_list.sort(key=lambda x: x['SUCCESS_RATE'])

    return configurations_table_list


def plotSuccessRate(config_table,X_key,Y_key):
    """
    Plots a 3D heatmap of success rates by parameters values.

    :param dict config_table: Database configurations table.
    :param str x_key: Config table x axis key.
    :param str y_key: Config table y axis key.
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
    ax.set_title('Success Rate Heatmap')
    savefig('heatmap.png')
    show()
