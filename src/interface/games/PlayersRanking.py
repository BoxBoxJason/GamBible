# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: interface.games
Module:  PlayersRanking
Version: 2.0
Usage: Displays global ranking of players

Author: BoxBoxJason
Date: 09/10/2023
'''
import logging
from PyQt6.QtWidgets import QWidget,QScrollArea, QVBoxLayout, QHBoxLayout,\
    QLabel, QLineEdit
from PyQt6.QtCore import Qt
from interface.TemplateWidget import TemplatePageWidget
from resources.utils import getRankFromELO
from resources.PathEnum import getJsonObject

class PlayersRankingWidget(TemplatePageWidget):
    """
    Displays the database players ranking.

    :ivar dict __players_table: Database Players table.
    :ivar dict __players_badges: Dictionary of ranking badge widget for each player {player_id:RankingBadge}.
    :ivar QVBoxLayout __scroll_layout: Layout used for scrollable area.
    """
    def __init__(self,parent):
        super().__init__(parent)
        self.__players_table = {}
        self.__players_badges = {}

        # Search bar label
        filter_qlabel = QLabel('Filter players',self)
        filter_qlabel.setObjectName('h3')
        self.layout().addWidget(filter_qlabel,2,0,1,2,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        # Search bar
        search_bar = QLineEdit(self)
        search_bar.textChanged.connect(self.__filterPlayers)
        self.layout().addWidget(search_bar,3,0,1,2,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Ranking scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(445)
        scroll_area.setMinimumHeight(400)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.layout().addWidget(scroll_area,4,0,1,2,Qt.AlignmentFlag.AlignHCenter)

        # Scroll widget and layout
        scroll_widget = QWidget(self)
        self.__scroll_layout = QVBoxLayout(scroll_widget)
        self.__scroll_layout.setContentsMargins(0,0,0,0)
        self.__scroll_layout.setSpacing(0)

        scroll_area.setWidget(scroll_widget)
        self.__scroll_layout.addWidget(RankingBadge(self,{'ELO':'ELO'},'RANK'),
                                      1,Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)



    def __filterPlayers(self,filter_txt):
        """
        Filters displayed players ranking badges.

        :param str filter_txt: Text in the search bar.
        """
        for player,player_badge in self.__players_badges.items():
            if filter_txt in player:
                player_badge.setHidden(False)
            else:
                player_badge.setHidden(True)


    def setDatabase(self,database_path):
        """
        Sets the widget database, changes the pickable players in corresponding widgets.

        :param path database_path: Absolute path to database file.
        """
        database = getJsonObject(database_path)
        self.__players_table = database['PLAYERS']
        test_row = self.__players_table.popitem()
        if 'ELO' in test_row[1]:
            sorted_players = sorted(self.__players_table.values(),key=lambda x: x['ELO'],reverse=True)
        else:
            sorted_players = sorted(self.__players_table.values(),key=lambda x: x['SKILL'] - 3 * x['SKILL_DEVIATION'],reverse=True)

        logging.debug('Creating ranking badges')
        for index,player_dict in enumerate(sorted_players):
            new_badge = RankingBadge(self,player_dict,index)
            self.__players_badges[player_dict['ID']] = new_badge
            self.__scroll_layout.addWidget(new_badge,1,
                                          Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        logging.debug('Ranking badges done')


    def clean(self):
        """
        Cleans the widget from existing data
        """
        self.__players_table.clear()
        while self.__scroll_layout.count() > 1:
            self.__scroll_layout.itemAt(1).widget().setParent(None)


class RankingBadge(QWidget):
    """
    Ranking widget ranking badge. Used for user ranking display.
    """
    def __init__(self,parent,player_dict,index_player):
        """
        Constructor for RankingBadge.
        
        :param QWidget parent: Parent widget.
        :param dict player_dict: Database Players table row.
        :param int index_player: Global ranking of the player. (first is 0)
        """
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground,True)
        layout = QHBoxLayout()

        if isinstance(index_player,int):
            index_player = str(index_player+1)

        # Rank label
        rank_label = QLabel(index_player,self)
        rank_label.setFixedSize(50,22)
        layout.addWidget(rank_label,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Player label
        player_label = QLabel(player_dict.get('ID','ID'),self)
        player_label.setFixedSize(200,22)
        layout.addWidget(player_label,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Tier label
        elo = player_dict.get('ELO')
        if elo is None:
            elo = player_dict.get('SKILL',0) - 3 * player_dict.get('SKILL_DEVIATION',0)
        division = getRankFromELO(elo)
        self.setObjectName(division)
        tier_label = QLabel(division,self)
        tier_label.setFixedSize(100,22)
        layout.addWidget(tier_label,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # ELO label
        elotxt = elo
        if not isinstance(elo,str):
            elotxt = "{:.2f}".format(elo)
        elo_label = QLabel(elotxt,self)
        elo_label.setFixedSize(55,22)
        layout.addWidget(elo_label,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        for label in rank_label,player_label,tier_label,elo_label:
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            label.setObjectName('p')

        self.setLayout(layout)
