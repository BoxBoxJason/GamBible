# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: resources
Module:  utils
Version: 2.0
Usage: General utility functions

Author: BoxBoxJason
Date: 01/10/2023
'''

def getRankFromELO(ELO):
    """
    @param (float or int) ELO : player ELO
    
    @return (str) rank : rank corresponding to ELO
    """
    rank = ""
    if ELO == 'ELO':
        rank = "DIVISION"
    elif ELO < 500:
        rank = "BRONZE"
    elif ELO < 900:
        rank = "SILVER"
    elif ELO < 1300:
        rank = "GOLD"
    elif ELO < 1700:
        rank = "PLATINUM"
    elif ELO < 2100:
        rank = "DIAMOND"
    elif ELO < 2500:
        rank = "MASTER"
    else:
        rank = "GRANDMASTER"
    return rank


def findZero(f):
    Δ = 1
    ε = 1e-5
    a = -1e4
    b = 1e4
    while Δ > ε:
        m = (a + b) / 2
        Δ = abs(b - a)
        if f(m) == 0:
            a =  m
            break
        elif f(a) * f(m)  > 0:
            a = m
        else:
            b = m

    return a
