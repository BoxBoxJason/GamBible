# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: interface.games
Module:  TeamWidget
Version: 2.0
Usage: 

Author: BoxBoxJason
Date: 09/10/2023
'''
from interface.TemplateWidget import TemplatePageWidget


class TeamWidget(TemplatePageWidget):
    """
    Team game outcome prediction widget.
    """
    def __init__(self,parent):
        """
        Constructor for TeamWidget.

        :param QWidget parent: Parent widget.
        """
        super().__init__(parent)
