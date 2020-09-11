import pymongo
from pymongo import MongoClient
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import plotly.graph_objects as go

# DB 연결
myclient = MongoClient('218.150.247.209:2017',
                       username='unsik',
                       password='next1004',
                       authSource='admin',
                       authMechanism='SCRAM-SHA-256')

myDB = myclient['FriDB']
collection = myDB['Population']


def makeFigure():

    subject_doct = pd.read_excel(
        'data/시도별_전문과목별_전문의_현황_2005-2018_2.xlsx', thousands=',')
    subject_doct = subject_doct.fillna(0)
    subject_doct = subject_doct.replace('-', 0)

    dataList = []

    for i in subject_doct.index:
        for j in range(len(subject_doct.columns[2:])):
            subject = subject_doct.iloc[i, 0]
            year = subject_doct.iloc[i, 1]
            local = subject_doct.columns[j+2]
            value = subject_doct.iloc[i, j+2]
            if local == '계':
                continue
            if subject == '계':
                continue
            dataDict = {'과목': subject, '년도': year, '지역': local, '값': value}
            dataList.append(dataDict)

    dataDf = pd.DataFrame(dataList)

    fig = px.bar(dataDf,
                 x='값',
                 y='과목',
                 height=1000,
                 range_x=[0, 16000],
                 orientation='h',
                 color='지역',
                 animation_frame='년도'

                 )
    fig.update_layout(
        margin=dict(l=0, r=0, t=100, b=0),
        font=dict(family='Malgun Gothic', size=13, color='rgb(67, 67, 67)'),
        yaxis=dict(categoryorder='total ascending'),
        updatemenus=[{'buttons': [{'args': [None, {'frame': {'duration':
                                                             1000, 'redraw': True}, 'mode':
                                                   'immediate', 'fromcurrent':
                                                   True, 'transition':
                                                   {'duration': 1000, 'easing':
                                                       'quadratic-in-out'}}],
                                   'label': '&#9654;',
                                   'method': 'animate'},
                                  {'args': [[None], {'frame':
                                                     {'duration': 0, 'redraw':
                                                      True}, 'mode': 'immediate',
                                                     'fromcurrent': True,
                                                     'transition': {'duration': 0,
                                                                    'easing': 'linear'}}],
                                   'label': '&#9724;',
                                      'method': 'animate'}],
                      'direction': 'left',
                      'pad': {'r': 10, 't': 70},
                      'showactive': False,
                      'type': 'buttons',
                      'x': 0.1,
                      'xanchor': 'right',
                      'y': 0,
                      'yanchor': 'top'}]
    )

    return fig
