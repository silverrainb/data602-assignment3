#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    File: pl_display.py
    Author: Rose Jones
    Advanced Programming Project CUNY Data Science DATA602
"""


import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='silverrainb', api_key='DmYtIA1DTo0aC6AC5z1e')


def pl_display(pl_data):
    vwap = go.Scatter(x=pl_data['Timestamp'], y=pl_data['VWAP'], mode='lines+markers', name='VWAP')
    executedprice = go.Scatter(x=pl_data['Timestamp'], y=pl_data['ExecutedPrice'], mode='lines+markers',
                               name='ExecutedPrice')
    totalpl = go.Scatter(x=pl_data['Timestamp'], y=pl_data['Total_PL'], mode='lines+markers', name='Total_PL')
    cash = go.Scatter(x=pl_data['Timestamp'], y=pl_data['Cash'], mode='lines+markers', name='Cash')
    data = [vwap, executedprice, totalpl, cash]
    py.plot(data, filename='basic-line')
    # https://plot.ly/~silverrainb/10