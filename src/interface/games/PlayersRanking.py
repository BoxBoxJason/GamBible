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
from json import load
from PyQt6.QtWidgets import QWidget,QScrollArea, QVBoxLayout, QHBoxLayout,\
    QLabel, QLineEdit
from PyQt6.QtCore import Qt
from interface.TemplateWidget import TemplatePageWidget
from resources.utils import getRankFromELO

class PlayersRankingWidget(TemplatePageWidget):
    """
    Players ranking widget
    
    Layout:
    
                TITLE
              SUBTITLE

              SEARCH BAR
            SCROLL WIDGET
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
        self.__scrollLayout = QVBoxLayout()
        self.__scrollLayout.setContentsMargins(0,0,0,0)
        self.__scrollLayout.setSpacing(0)

        scroll_widget.setLayout(self.__scrollLayout)
        scroll_area.setWidget(scroll_widget)
        self.__scrollLayout.addWidget(RankingBadge(self,{'ELO':'ELO'},'RANK'),
                                      1,Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)



    def __filterPlayers(self,filter_txt):
        for player,player_badge in self.__players_badges.items():
            if filter_txt in player:
                player_badge.setHidden(False)
            else:
                player_badge.setHidden(True)


    def setDatabase(self,db_path):
        """
        Clears previous displayed ranking and displays selected one

        @param (path) db_path : Absolute path to new db
        """
        with open(db_path,'r',encoding='utf-8') as database_file:
            self.__players_table = load(database_file)['PLAYERS']

        sorted_players = sorted(self.__players_table.values(),key=lambda x: x['ELO'],reverse=True)

        logging.debug('Creating ranking badges')
        for index,player_dict in enumerate(sorted_players):
            new_badge = RankingBadge(self,player_dict,index)
            self.__players_badges[player_dict['ID']] = new_badge
            self.__scrollLayout.addWidget(new_badge,1,
                                          Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        logging.debug('Ranking badges done')


    def clean(self):
        """
        Cleans the widget from existing data
        """
        self.__players_table.clear()
        while self.__scrollLayout.count() > 1:
            self.__scrollLayout.itemAt(1).widget().setParent(None)


class RankingBadge(QWidget):
    """
    Ranking widget ranking badge
    LAYOUT:
            PLAYER NAME        PLAYER ELO        PLAYER RANK
    """

    __STYLESRANK = {
        "DIVISION":"RankingBadge { background-color: rgb(100,100,100);}",
        "BRONZE":"RankingBadge { background: qradialgradient(cx: 0.8, cy: 0.1, radius: 1, fx: 0.5, fy: 0.5, stop: 0 #efa678, stop: 0.4 #8c4d37, stop: 0.5 #603620, stop: 0.6 #b77b56, stop: 1 #603620); border-top: 1px solid #5a3320;}",
        "SILVER":"RankingBadge { background: qradialgradient(cx: 0.8, cy: 0.1, radius: 1, fx: 0.5, fy: 0.5, stop: 0 #ededed, stop: 0.4 #b0b0b0, stop: 0.5 #727272, stop: 0.6 #999999, stop: 1 #727272); border-top: 1px solid #555555;}",
        "GOLD":"RankingBadge { background: qradialgradient(cx: 0.8, cy: 0.1, radius: 1, fx: 0.5, fy: 0.5, stop: 0 #f5ec70, stop: 0.4 #a88e2a, stop: 0.5 #92741c, stop: 0.6 #a88e2a, stop: 1 #92741c); border-top: 1px solid #5e5010;}",
        "PLATINUM":"RankingBadge { background: qradialgradient(cx: 0.8, cy: 0.1, radius: 1, fx: 0.5, fy: 0.5, stop: 0 #125c84, stop: 0.4 #E5E4E2, stop: 0.5 #58949c, stop: 0.6 #125384, stop: 1 #157bb3); border-top: 1px solid #0c3d57;}",
        "DIAMOND":"RankingBadge { background: qradialgradient(cx: 0.8, cy: 0.1, radius: 1, fx: 0.5, fy: 0.5, stop: 0 #9bd4e1, stop: 0.4 #aae3f0, stop: 0.5 #b9f2ff, stop: 0.6 #aae3f0, stop: 1 #9bd4e1); border-top: 1px solid #9bd4e1;}",
        "MASTER":"RankingBadge { background: qradialgradient(cx: 0.8, cy: 0.1, radius: 1, fx: 0.5, fy: 0.5, stop: 0 #fa71cd, stop: 0.4 #b256e8, stop: 0.5 #c471f5, stop: 0.6 #b256e8, stop: 1 #c471f5); border-top: 1px solid #a15dc9;}",
        "GRANDMASTER":"RankingBadge { background: qradialgradient(cx: 0.8, cy: 0.1, radius: 1, fx: 0.5, fy: 0.5, stop: 0 #b54e4e, stop: 0.4 #db7f7f, stop: 0.5 #d3d3d3, stop: 0.6 #cf2525, stop: 1 #8f8989); border-top: 1px solid #5e5010;}"
    }

    def __init__(self,parent,player_dict,index_player):
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
        division = getRankFromELO(player_dict.get('ELO'))
        self.setStyleSheet(RankingBadge.__STYLESRANK[division])
        tier_label = QLabel(division,self)
        tier_label.setFixedSize(100,22)
        layout.addWidget(tier_label,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # ELO label
        elotxt = player_dict.get('ELO')
        if elotxt is None:
            elotxt = player_dict.get('SKILL',0) - 3 * player_dict.get('SKILL_DEVIATION',0)
        if not isinstance(elotxt,str):
            elotxt = "{:.2f}".format(elotxt)
        elo_label = QLabel(elotxt,self)
        elo_label.setFixedSize(55,22)
        layout.addWidget(elo_label,1,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        for label in rank_label,player_label,tier_label,elo_label:
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            label.setObjectName('p')

        self.setLayout(layout)
