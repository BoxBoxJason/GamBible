# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: interface
Module:  Toolbar
Version: 2.0
Usage: General toolbar for GamBible. Allows to change sports and navigate in GamBible.

Author: BoxBoxJason
Date: 05/10/2023
'''
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction, QIcon
from resources.PathEnum import getConfig,getImage

class TopNavBar(QMenuBar):
    """
    Top navigation toolbar for GamBible.
    """

    def __init__(self,parent):
        """
        Constructor for TopNavBar.

        :param QWidget parent: Parent widget.
        """
        super().__init__(parent)

        config_dict = getConfig()
        settings_menu = self.addMenu(QIcon(getImage('Gear.png')), 'Settings')

        for sport_name,sport_config_dict in config_dict['TOOLBAR'].items():
            self.__createMenuAndActions(sport_name, sport_config_dict['icon'],sport_config_dict['categories'],sport_config_dict['events'])


    def __createMenuAndActions(self,sport_name,sport_icon_name,categories,events):
        """
        Creates a sport menu with corresponding icon. Adds submenus for categories.

        :param str sport_name: Sport name.
        :param str sport_icon_name: Sport icon file name.
        :param list[str] categories: Iterable of categories available for that sport.
        :param list[str] events: Iterable of events available for that sport.
        """
        sport_menu = self.addMenu(QIcon(getImage(sport_icon_name)),'')
        self.__createCategoryMenu(sport_menu,sport_name,categories[0],events)
        for category in categories[1:]:
            sport_menu.addSeparator()
            self.__createCategoryMenu(sport_menu,sport_name,category,events)


    def __createCategoryMenu(self,base_menu,sport_name,category,events):
        """
        Creates a category menu and adds it to the sport menu. Creates all actions filling that menu.

        :param QMenu base_menu: Parent menu for the category.
        :param str sport_name: Sport name.
        :param str category: Category name.
        :param list[str] events: iterable of events available for that sport.
        """
        category_menu = base_menu.addMenu(category)
        self.__createAction(category_menu, sport_name,category,events[0],
                            lambda : self.parent().centralWidget().switchSelection(sport_name,category,events[0]))
        for event_name in events[1:]:
            category_menu.addSeparator()
            self.__createAction(category_menu, sport_name, category, event_name,
                                lambda : self.parent().centralWidget().switchSelection(sport_name,category,event_name))
        category_menu.addSeparator()
        self.__createAction(category_menu,sport_name,category,
                            'ranking',lambda : self.parent().centralWidget().switchSelection(sport_name,category,'ranking'))


    def __createAction(self,parent_menu,sport_name,category,event_name,action_call):
        """
        Creates an action with input values and adds it to the parent menu.

        :param QMenu parent_menu: Action parent menu.
        :param str sport_name: Sport name.
        :param str category: Category name.
        :param str event_name: Event name.
        :param function action_call: Function called on action trigger.
        """
        action = QAction(event_name.capitalize(),self)
        action.setToolTip(f"Open {sport_name} {category} {event_name} window")
        action.triggered.connect(action_call)
        parent_menu.addAction(action)
