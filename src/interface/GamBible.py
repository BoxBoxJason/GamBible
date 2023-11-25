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
    GamBible main window. Contains the app MainWidget that manages all app functionalities and the toolbar for app navigation.
    """
    def __init__(self):
        """
        Constructor for GamBible.
        """
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
    GamBible main widget. Hosts and operates all functionalities.
    Contains all displayable windows and orchestrates them.

    :cvar dict __INDEXBYEVENT: Contains the index of the corresponding window depending on the event.
    :cvar dict __DBNAMEBYEVENT: Contains the database default file names for each event.
    """

    __INDEXBYEVENT = {"welcome":0,"settings":1,"1v1 game":2,"free for all game":3,"team game":4,"ranking":5}
    __DBNAMEBYEVENT = {"1v1 game":"defaultELO.json","free for all game":"defaultMMR-FFA.json","team game":"defaultMMR-Team.json"}

    def __init__(self,parent):
        """
        Constructor for MainWidget.

        :param QWidget parent: Parent widget.
        """
        super().__init__(parent)

        stacked_layout = QStackedLayout(self)
        stacked_layout.addWidget(WelcomePage(self))
        stacked_layout.addWidget(SettingsWidget(self))
        stacked_layout.addWidget(OneVOneWidget(self))
        stacked_layout.addWidget(FreeForAllWidget(self))
        stacked_layout.addWidget(TeamWidget(self))
        stacked_layout.addWidget(PlayersRankingWidget(self))


    def switchSelection(self,sport,category,event):
        """
        Changes displayed page and updates with corresponding players database.

        :param str sport: Selected sport name.
        :param str category: Selected category name.
        :param str event: Selected event name.
        """
        config_dict = getConfig()
        db_name = MainWidget.__DBNAMEBYEVENT.get(event,config_dict['TOOLBAR'][sport]['database'])

        self.layout().widget(MainWidget.__INDEXBYEVENT[event]).clean()
        self.layout().widget(MainWidget.__INDEXBYEVENT[event]).setTitle(sport.capitalize())
        self.layout().widget(MainWidget.__INDEXBYEVENT[event]).setSubtitle(f"{category.capitalize()} {event}")
        self.layout().widget(MainWidget.__INDEXBYEVENT[event]).setDatabase(getDBPath(sport,category,db_name))
        self.layout().setCurrentIndex(MainWidget.__INDEXBYEVENT[event])


    def clean(self,index=None):
        """
        Cleans the requested widget, if no widget is requested, cleans currently displayed widget.

        :param int index: Index of the widget to clean.
        """
        if index is not None:
            self.layout().currentWidget().clean()
        else:
            self.layout().widget(index).clean()


def addFonts():
    """
    Adds all available fonts to QFontDatabase.
    """
    for font_path in getFontsPaths():
        QFontDatabase.addApplicationFont(font_path)
