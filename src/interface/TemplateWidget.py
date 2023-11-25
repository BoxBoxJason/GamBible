# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: interface
Module:  TemplateWidget
Version: 2.0
Usage: General template for GamBible MainWidget subwidgets

Author: BoxBoxJason
Date: 22/11/2023
'''
from PyQt6.QtWidgets import QWidget,QLabel,QGridLayout
from PyQt6.QtCore import Qt


class TemplatePageWidget(QWidget):
    """
    Template widget for GamBible pages.

    :ivar QLabel title_qlabel: Displayed title label.
    :ivar QLabel subtitle_qlabel: Displayed subtitle label.
    """
    def __init__(self,parent):
        super().__init__(parent)
        layout = QGridLayout(self)

        # Widget title
        self.title_qlabel = QLabel('',self)
        self.title_qlabel.setObjectName('h1')
        layout.addWidget(self.title_qlabel,0,0,1,2,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Widget subtitle
        self.subtitle_qlabel = QLabel('',self)
        self.subtitle_qlabel.setObjectName('h2')
        layout.addWidget(self.subtitle_qlabel,1,0,1,2,Qt.AlignmentFlag.AlignHCenter |Qt.AlignmentFlag.AlignTop)


    def setTitle(self,title):
        """
        Sets a new widget title.
        
        :param str title: New title value.
        """
        self.title_qlabel.setText(title)


    def setSubtitle(self,subtitle):
        """
        Sets a new widget subtitle.

        :param str subtitle: New subtitle value.
        """
        self.subtitle_qlabel.setText(subtitle)


    def clean(self):
        """
        Remove text from labels.
        """
        self.title_qlabel.clear()
        self.subtitle_qlabel.clear()
