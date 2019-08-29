#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    File: trade.py
    Author: Rose Jones
    Advanced Programming Project CUNY Data Science DATA602
"""


from buy import buy
from sell import sell


def trade(ledger, gdax):
    try:
        horizontal_line = "-------------------------"
        print("<< Menu >>")
        print(" >>1. Buy")
        print(" >>2. Sell")
        print(" >>3. Menu")
        print(horizontal_line * 2)
        select = input(">>>>> Please select number: \n>")
        if select == "1":
            buy(ledger, gdax)
        if select == "2":
            sell(ledger, gdax)
    except ValueError as e:
        print(e)
