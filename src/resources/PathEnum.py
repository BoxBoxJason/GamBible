# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: resources
Module:  PathEnum
Version: 2.0
Usage: Contains project useful paths and path / files related functions

Author: BoxBoxJason
Date: 05/10/2023
'''
import os
from json import dump,load

class PathEnum:
    """
    Paths enum, contains absolute paths to project resources
    """
    # Project root folder path
    GAMBIBLE = os.getenv("GAMBIBLE")
    # Results path
    RESULTS = os.path.join(GAMBIBLE,"results")
    # Project resources folder path
    RESOURCES = os.path.join(GAMBIBLE,"src","resources")
    # Project images folder path
    IMAGES = os.path.join(RESOURCES,"images")
    # Config file path
    CONFIG = os.path.join(RESOURCES,"config","config.json")

def getImage(image_name):
    """
    @param (str) image_name : name of the image to get
    
    @return (path) Absolute path to the requested image
    """
    return os.path.join(PathEnum.IMAGES,image_name)

def getDBPath(sport,category,db_name):
    """
    @param (str) sport : sport name
    @param (str) category : sport category
    @param (str) db_name : database file name


    """
    db_path = os.path.join(PathEnum.RESULTS,sport,category,db_name)
    os.makedirs(os.path.dirname(db_path),777,True)
    if not os.path.exists(db_path):
        with open(db_path,'w',encoding='utf-8') as db_file:
            dump({'GAMES':{},'PLAYERS':{}},db_file)
    return db_path


def getConfig():
    """
    @return (dict) configuration dict
    """
    with open(PathEnum.CONFIG,'r',encoding='utf-8') as config_file:
        config_dict = load(config_file)
    return config_dict


def getFontsPaths():
    """    
    @return (path[]) absolute paths to font files
    """
    fonts_path = os.path.join(PathEnum.RESOURCES,'fonts')
    return [os.path.join(fonts_path,file_name) for file_name in os.listdir(fonts_path)]


def getStyleSheet():
    with open(os.path.join(PathEnum.RESOURCES,'GamBible.qss'),'r',encoding='utf-8') as stylesheet_file:
        stylesheet = stylesheet_file.read()

    for placeholder,value in getStyleJson().items():
        stylesheet = stylesheet.replace(placeholder,value)

    return stylesheet


def getStyleJson():
    with open(os.path.join(PathEnum.RESOURCES,'styles.json'),'r',encoding='utf-8') as json_file:
        return load(json_file)
