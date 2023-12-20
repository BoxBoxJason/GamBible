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
    Paths enum, contains absolute paths to project resources.

    :cvar path GAMBIBLE: Absolute path to root folder.
    :cvar path RESULTS: Absolute path to results folder.
    :cvar path RESOURCES: Absolute path to resources folder.
    :cvar path IMAGES: Absolute path to images folder.
    :cvar path CONFIG: Absolute path to config.json file.
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
    :param str image_name: Requested image file name (with extension).
    
    :return: path - Absolute path to requested image.
    """
    return os.path.join(PathEnum.IMAGES,image_name)

def getDBPath(sport,category,db_name,create=True):
    """
    Returns absolute database path for requested sport, category and file name.
    If the path does not exist, it will be created.
    If the database does not exist, it will be created.

    :param str sport : Sport name.
    :param str category: Sport category.
    :param str db_name: Database file name.

    :return: path - Absolute path to database file.
    """
    db_path = os.path.join(PathEnum.RESULTS,sport,category,db_name)
    os.makedirs(os.path.dirname(db_path),777,True)
    if not os.path.exists(db_path) and create:
        dumpJsonObject({'GAMES':{},'PLAYERS':{}},db_path)
    return db_path


def getConfig():
    """
    Returns app configuration dictionary.

    :return: dict - Configuration dictionary.
    """
    return getJsonObject(PathEnum.CONFIG)


def getFontsPaths():
    """
    Returns the list of absolute app fonts files paths.
    :return: list[path] - List of absolute paths to font files.
    """
    fonts_path = os.path.join(PathEnum.RESOURCES,'fonts')
    return [os.path.join(fonts_path,file_name) for file_name in os.listdir(fonts_path)]


def getStyleSheet():
    """
    Returns the app stylesheet with template values filled.

    :return: str - App stylesheet.
    """
    with open(os.path.join(PathEnum.RESOURCES,'GamBible.qss'),'r',encoding='utf-8') as stylesheet_file:
        stylesheet = stylesheet_file.read()

    for placeholder,value in getStyleJson().items():
        stylesheet = stylesheet.replace(placeholder,value)

    return stylesheet


def getStyleJson():
    """
    Returns the app styles dictionary.

    :return: dict - App styles dictionary.
    """
    with open(os.path.join(PathEnum.RESOURCES,'styles.json'),'r',encoding='utf-8') as json_file:
        return load(json_file)


def getJsonObject(file_path):
    """
    Returns the content of a json file.

    :param path file_path: Absolute path to file.

    :return: JsonObject - .json file content parsed into a Python object.
    """
    os.makedirs(os.path.dirname(file_path),511,True)
    result = {}
    if os.path.exists(file_path):
        with open(file_path,'r',encoding='utf-8') as json_file:
            result = load(json_file)

    return result


def dumpJsonObject(json_object,file_path):
    """
    Overwrites json object to file_path.

    :param JsonObject json_object : JSON object to save in file.
    :param path file_path: Absolute path to destination file.
    """
    os.makedirs(os.path.dirname(file_path),511,True)
    with open(file_path,'w',encoding='utf-8') as json_file:
        dump(json_object,json_file)
