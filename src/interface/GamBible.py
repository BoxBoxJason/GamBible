# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: interface
Module:  GamBible
Version: 2.0
Usage: Main module of GamBible interface. Contains GamBible main window and main widget

Author: BoxBoxJason
Date: 03/10/2023
'''
import logging
from PyQt6.QtWidgets import QMainWindow,QWidget,QVBoxLayout,QStackedLayout
from PyQt6.QtGui import QIcon,QFontDatabase
from PyQt6.QtCore import Qt
from interface.Toolbar import TopNavBar
from resources.PathEnum import getImage,getDBPath,getFontsPaths,getConfig
from interface.WelcomePage import WelcomePage
from interface.SettingsWidget import SettingsWidget
from interface.games.OneVOneWidget import OneVOneWidget
from interface.games.FreeForAllWidget import FreeForAllWidget
from interface.games.TeamWidget import TeamWidget
from interface.games.PlayersRanking import PlayersRankingWidget

class GamBible(QMainWindow):
    """
    GamBible main window
    
    GRIDLAYOUT:
                TITLE
              SUBTITLE
              
              MESSAGE
              
        P1 WIDGET    P2 WIDGET
        
        GAME INFORMATION WIDGET
        
                SUBMIT
    """
    def __init__(self):
        logging.debug('Setting up Collector main window')
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.setWindowTitle('GamBible')
        self.setWindowIcon(QIcon(getImage('GamBible.png')))

        self.setMenuBar(TopNavBar(self))
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.setCentralWidget(MainWidget(self))

        logging.debug('GamBible main window build successful')


class MainWidget(QWidget):
    """
    GamBible main widget
    Contains all displayable windows
    """

    __INDEXBYEVENT = {"welcome":0,"settings":1,"1v1 game":2,"free for all game":3,"team game":4,"ranking":5}
    __DBNAMEBYEVENT = {"1v1 game":"defaultELO.json","free for all game":"defaultMMR-FFA.json","team game":"defaultMMR-Team.json"}

    def __init__(self,parent):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.__stacked_layout = QStackedLayout()
        self.__stacked_layout.addWidget(WelcomePage(self))
        self.__stacked_layout.addWidget(SettingsWidget(self))
        self.__stacked_layout.addWidget(OneVOneWidget(self))
        self.__stacked_layout.addWidget(FreeForAllWidget(self))
        self.__stacked_layout.addWidget(TeamWidget(self))
        self.__stacked_layout.addWidget(PlayersRankingWidget(self))

        layout.addLayout(self.__stacked_layout,1)
        self.setLayout(layout)


    def switchSelection(self,sport,category,event):
        """
        Changes displayed page and updates with corresponding players database

        @param (str) sport : Selected sport
        @param (str) category : Selected category
        @param (str) event : Selected event
        """
        config_dict = getConfig()
        db_name = MainWidget.__DBNAMEBYEVENT.get(event,config_dict['TOOLBAR'][sport]['database'])

        self.__stacked_layout.widget(MainWidget.__INDEXBYEVENT[event]).clean()
        self.__stacked_layout.widget(MainWidget.__INDEXBYEVENT[event]).setTitle(sport.capitalize())
        self.__stacked_layout.widget(MainWidget.__INDEXBYEVENT[event]).setSubtitle(f"{category.capitalize()} {event}")
        self.__stacked_layout.widget(MainWidget.__INDEXBYEVENT[event]).setDatabase(getDBPath(sport,category,db_name))
        self.__stacked_layout.setCurrentIndex(MainWidget.__INDEXBYEVENT[event])


    def clean(self,index=None):
        """
        Cleans the requested widget

        @param (int) index : Index of the widget to clean
        """
        if index is not None:
            self.__stacked_layout.currentWidget().clean()
        else:
            self.__stacked_layout.widget(index).clean()


def addFonts():
    """
    Adds all available fonts to QFontDatabase
    """
    for font_path in getFontsPaths():
        QFontDatabase.addApplicationFont(font_path)
