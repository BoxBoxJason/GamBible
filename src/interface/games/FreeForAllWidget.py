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
from interface.TemplateWidget import TemplatePageWidget

class FreeForAllWidget(TemplatePageWidget):

    def __init__(self,parent):
        super().__init__(parent)
        self.players_table = {}
