# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: 
Module:  __main__
Version: 2.0
Usage: GamBible main module, adds fonts, creates GamBible window and runs the app.

Author: BoxBoxJason
Date: 01/10/2023
@copyright: Created by BoxBoxJason, All Rights Reserved
'''


import logging
from os.path import join,dirname
from os import environ
import sys
from PyQt6.QtWidgets import QApplication
root_dir_path = dirname(dirname(__file__))
environ['GAMBIBLE'] = root_dir_path

from resources.PathEnum import getStyleSheet
from interface.GamBible import GamBible,addFonts
from ranking.ELO import optimizeHyperparametersBayesian


##----------Logging setup----------##
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(join(root_dir_path,"logging.log")),
        logging.StreamHandler(sys.stdout)
    ]
)

optimizeHyperparametersBayesian('Tennis','Men')
exit()

logging.info('Starting GamBible V2.0')

app = QApplication(sys.argv)
addFonts()
app.setStyleSheet(getStyleSheet())
gambible = GamBible()
gambible.show()

app.exec()

logging.info('Closing GamBible V2.0, See you later !')
