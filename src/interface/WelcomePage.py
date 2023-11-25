# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: interface
Module:  WelcomePage
Version: 2.0
Usage: GamBible welcome page, does not provide any functionality appart from display.

Author: BoxBoxJason
Date: 07/10/2023
'''
from PyQt6.QtGui import QPixmap
from interface.TemplateWidget import TemplatePageWidget
from resources.PathEnum import getImage

class WelcomePage(TemplatePageWidget):
    """
    GamBible Welcome page.
    """
    def __init__(self,parent):
        """
        Constructor for WelcomePage.
        
        :param QWidget parent: Parent widget.
        """
        super().__init__(parent)

        img = QPixmap(getImage('GamBible.png'))
        self.title_qlabel.setPixmap(img)

        self.subtitle_qlabel.setText('Please pick a sport !')
        self.subtitle_qlabel.setObjectName('p')
