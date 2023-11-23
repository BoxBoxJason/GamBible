# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: interface.games
Module:  OneVOneWidget
Version: 2.0
Usage: 1v1 game prediction widget, allows to pick two players and predict the game outcome (with a confidence rate)

Author: BoxBoxJason
Date: 09/10/2023
'''
from json import load
from PyQt6.QtWidgets import QWidget,QLabel,QPushButton,QVBoxLayout,QLineEdit,QCompleter
from PyQt6.QtCore import Qt,QStringListModel
from interface.TemplateWidget import TemplatePageWidget
from ranking.ELO import determineWinProbability,processGames

class OneVOneWidget(TemplatePageWidget):
    """
    1v1 games widget,
    Allows to pick players and predict the outcome of a game between them
    """
    def __init__(self,parent):
        super().__init__(parent)
        self.players_table = {}
        self.layout()
        self.__player1_widget = PlayerWidget(self,1)
        self.__player2_widget = PlayerWidget(self,2)
        self.layout().addWidget(self.__player1_widget,2,0,1,1,Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.__player2_widget,2,1,1,1,Qt.AlignmentFlag.AlignCenter)

        # Predict button
        predict_button = QPushButton('PREDICT',self)
        predict_button.setObjectName('submit')
        predict_button.clicked.connect(self.__predictGameOutput)
        self.layout().addWidget(predict_button,5,0,1,2,Qt.AlignmentFlag.AlignCenter)


    def setDatabase(self,database_path):
        """
        Sets the widget database, changes the pickable players in corresponding widgets

        @param (path) database_path : Absolute path to database file
        """
        with open(database_path,'r',encoding='utf-8') as database_file:
            database = load(database_file)
        games_table = database['GAMES']
        self.players_table = database['PLAYERS']
        processGames(database_path,games_table,self.players_table,28.163265306122447,3.33265306122449,1,True)
        self.__player1_widget.updatePlayersList(self.players_table)
        self.__player2_widget.updatePlayersList(self.players_table)


    def __predictGameOutput(self):
        player1_id = self.__player1_widget.search_bar.text()
        player2_id = self.__player2_widget.search_bar.text()
        if player1_id in self.players_table and player2_id in self.players_table:
            player1_winrate = determineWinProbability(self.players_table[player1_id]['ELO'],self.players_table[player2_id]['ELO'])
            player2_winrate = 1 - player1_winrate

            self.__player1_widget.player_winrate_qlabel.setText(f"{player1_winrate*100}%")
            self.__player2_widget.player_winrate_qlabel.setText(f"{player2_winrate*100}%")


    def clean(self):
        """
        Cleans the widget
        """
        super().clean()
        self.players_table.clear()
        self.__player1_widget.clean()
        self.__player2_widget.clean()

WRONG_INPUT_STYLE = "QLineEdit {background-color: #edab9f; border: 2px ridge #bf1d00; padding: 5px 10px;}"
CORRECT_INPUT_STYLE = "QLineEdit {background-color: #b3f5a4;border: 2px ridge #229608;padding: 5px 10px;}"

class PlayerWidget(QWidget):
    """
    Player picker widget
    """
    def __init__(self,parent,player_index):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        # Player title label
        title_qlabel = QLabel(f"Player {player_index}",self)
        title_qlabel.setObjectName('h3')
        layout.addWidget(title_qlabel,0,Qt.AlignmentFlag.AlignHCenter)

        # Player search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setStyleSheet(CORRECT_INPUT_STYLE)
        self.search_bar.textChanged.connect(self.__updateSuggestions)
        layout.addWidget(self.search_bar,0,Qt.AlignmentFlag.AlignHCenter)

        # Search bar completer
        self.completer = QCompleter(self)
        self.completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        self.search_bar.setCompleter(self.completer)

        # Player winrate
        self.player_winrate_qlabel = QLabel(self)
        self.player_winrate_qlabel.setObjectName('p')
        layout.addWidget(self.player_winrate_qlabel,0,Qt.AlignmentFlag.AlignHCenter)


    def __updateSuggestions(self,text):
        first_suitable_element = None
        for player_id in self.parent().players_table:
            if text in player_id:
                first_suitable_element = player_id
                break
        
        if first_suitable_element is not None:
            self.search_bar.setStyleSheet(CORRECT_INPUT_STYLE)
        else:
            self.search_bar.setStyleSheet(WRONG_INPUT_STYLE)


    def clean(self):
        """
        Cleans the widget
        """
        for i in range(1,3):
            self.layout().itemAt(i).widget().clear()


    def updatePlayersList(self, players_ids):
        self.completer.setModel(QStringListModel(players_ids, self.completer))
