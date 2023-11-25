# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: interface
Module:  SettingsWidget
Version: 2.0
Usage: Settings widget for GamBible. Allows to change app settings.

Author: BoxBoxJason
Date: 09/10/2023
'''
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

class SettingsWidget(QWidget):
    """
    Settings widget. Allows user to change settings.
    """
    def __init__(self,parent):
        """
        Constructor for SettingsWidget.

        :param QWidget parent: Parent Widget.
        """
        super().__init__(parent)
        layout = QGridLayout(self)

        layout.addWidget(QLabel('Settings Widget',self))
