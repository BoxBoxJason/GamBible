# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: interface.games
Module:  FreeForAllWidget
Version: 2.0
Usage: Free for all game prediction widget, allows to pick several players and predict the game outcome (with a confidence rate)

Author: BoxBoxJason
Date: 09/10/2023
'''
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QLabel,QListWidget,QLineEdit,QHBoxLayout,QMenu,QPushButton,\
QCompleter,QListWidgetItem,QInputDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QStringListModel,Qt
from resources.PathEnum import getJsonObject,dumpJsonObject
from ranking.MMR import processGames
from interface.TemplateWidget import TemplatePageWidget

class FreeForAllWidget(TemplatePageWidget):
    """
    Free for all game outcome prediction widget.

    :ivar dict players_table: Database Players table.
    :ivar RankingWidget __ranking_widget: Game players ranking widget (see RankingWidget documentation).
    :ivar QLabel __prediction_confidence_rate_qlabel: Label used to display prediction confidence rate.
    """
    def __init__(self,parent):
        """
        Constructor for FreeForAllWidget

        :param QWidget parent: Parent widget.
        """
        super().__init__(parent)
        self.players_table = {}

        # Ranking widget
        self.__ranking_widget = RankingWidget(self)
        self.layout().addWidget(self.__ranking_widget,2,0,1,2,Qt.AlignmentFlag.AlignHCenter)

        # Confidence rate label
        self.__prediction_confidence_rate_qlabel = QLabel(self)
        self.__prediction_confidence_rate_qlabel.setObjectName('p')
        self.layout().addWidget(self.__prediction_confidence_rate_qlabel,3,0,1,2,Qt.AlignmentFlag.AlignHCenter)

        # Predict button
        predict_button = QPushButton('PREDICT',self)
        predict_button.setObjectName('submit')
        predict_button.clicked.connect(self.__predictOutcome)
        self.layout().addWidget(predict_button,4,0,1,2,Qt.AlignmentFlag.AlignHCenter)


    def setDatabase(self,database_path):
        """
        Sets the widget database, changes the pickable players in corresponding widgets.

        :param path database_path: Absolute path to database file.
        """
        database = getJsonObject(database_path)
        self.players_table = database['PLAYERS']
        print(processGames(database_path,database['GAMES'],self.players_table,20,1,1,True))
        self.__ranking_widget.updatePlayersList(self.players_table)
        dumpJsonObject(database,database_path)


    def __predictOutcome(self):
        """
        Predicts the outcome of the game and displays prediction confidence rate
        """
        players_ids_list = self.__ranking_widget.getNames()
        if len(players_ids_list) > 1:
            players_dicts = [self.players_table[player_id] for player_id in players_ids_list]
            players_dicts.sort(key= lambda x : x['SKILL'] - 3 * x['SKILL_DEVIATION'])


    def clean(self):
        """
        Cleans widget
        """
        self.__ranking_widget.clean()
        self.__prediction_confidence_rate_qlabel.clear()


WRONG_INPUT_STYLE = "QLineEdit {background-color: #edab9f; border: 2px ridge #bf1d00; padding: 5px 10px;}"
CORRECT_INPUT_STYLE = "QLineEdit {background-color: #b3f5a4;border: 2px ridge #229608;padding: 5px 10px;}"

class RankingWidget(QWidget):
    """
    Players list ranking widget with add button and search bar

    :ivar set __players_set: Contains players names that were added to the game.
    :ivar QListWidget __list_widget: Displays game players names.
    :ivar QLineEdit __search_bar: Player search bar, used to add players to game.
    :ivar QCompleter __completer: Search bar completer.
    """

    def __init__(self,parent,top_label='Players'):
        """
        Constructor for RankingWidget.

        :param QWidget parent: Parent widget.
        :param str top_label: Displayed widget header label.
        """
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.__players_set = set()
        # Title label
        players_qlabel = QLabel(top_label,self)
        players_qlabel.setObjectName('h3')
        layout.addWidget(players_qlabel,0,Qt.AlignmentFlag.AlignHCenter)

        # List widget
        self.__list_widget = QListWidget(self)
        self.__list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.__list_widget.customContextMenuRequested.connect(self.__openMenu)
        self.__list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        layout.addWidget(self.__list_widget,0,Qt.AlignmentFlag.AlignHCenter)

        search_widget = QWidget(self)
        search_bar_layout = QHBoxLayout(search_widget)
        # Player search bar
        self.__search_bar = QLineEdit(self)
        self.__search_bar.setStyleSheet(CORRECT_INPUT_STYLE)
        self.__search_bar.textChanged.connect(self.__updateBgColor)
        search_bar_layout.addWidget(self.__search_bar,0,Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        # Add button
        add_button = QPushButton('<<',self)
        add_button.clicked.connect(self.__addPlayerIdToList)
        add_button.setObjectName('submit-small')
        search_bar_layout.addWidget(add_button,0,Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(search_widget,0,Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Search bar completer
        self.__completer = QCompleter(self)
        self.__completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        self.__search_bar.setCompleter(self.__completer)


    def __addPlayerIdToList(self):
        """
        Adds a player id to the list of game participants if name is valid, registered in the database and not already there.
        """
        player_id = self.__search_bar.text().strip()
        if player_id in self.parent().players_table and not player_id in self.__players_set:
            self.__list_widget.addItem(QListWidgetItem(player_id))
            self.__players_set.add(player_id)


    def __updateBgColor(self,text):
        """
        Updates search bar background color depending if the player is known in database or not.

        :param str text: Text in the search bar.
        """
        if text.strip() in self.parent().players_table and not text.strip() in self.__players_set:
            self.__search_bar.setStyleSheet(CORRECT_INPUT_STYLE)
        else:
            self.__search_bar.setStyleSheet(WRONG_INPUT_STYLE)


    def __openMenu(self,position):
        """
        Triggered on context menu request. Opens a menu if there is a selected widget.
        """
        item = self.__list_widget.itemAt(position)
        if item is not None:
            menu = QMenu()
            edit_action = QAction("Edit", self)
            delete_action = QAction("Delete", self)

            edit_action.triggered.connect(lambda: self.__editItem(item))
            delete_action.triggered.connect(lambda: self.__deleteItem(item))

            menu.addAction(edit_action)
            menu.addAction(delete_action)

            menu.exec(self.mapToGlobal(position))


    def __deleteItem(self,item):
        """
        Deletes a widget from the QListWidget.

        :param QListWidgetItem item: widget to delete.
        """
        self.__players_set.remove(item.text())
        self.__list_widget.takeItem(self.row(item))


    def __editItem(self, item):
        """
        Edits a widget from the QListWidget.

        :param QListWidgetItem item: widget to edit.
        """
        text, ok = QInputDialog.getText(self, "Edit Item", "Enter new text:", text=item.text())
        if ok:
            item.setText(text)


    def updatePlayersList(self,players_ids):
        """
        Updates players list in the completer.

        :param list[str] players_ids: List of players ids.
        """
        self.__completer.setModel(QStringListModel(players_ids, self.__completer))


    def getNames(self):
        """
        Returns the ids in the QListWidget.

        :return: list[str] - List of players ids
        """
        return [self.__list_widget.item(i).text() for i in range(self.__list_widget.count())]


    def clean(self):
        """
        Cleans the widget
        """
        self.__list_widget.clear()
        self.__search_bar.clear()
