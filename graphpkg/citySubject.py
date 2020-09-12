import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import connectDB
import pandas as pd
import plotly.graph_objects as go


def conDB():
    # DB 연결
    myclient = connectDB.connectDB()

    myDB = myclient['FriDB']
    popCol = myDB['Population2']
    csdCol = myDB['CitySubjectDoc']

    popDF = pd.DataFrame(popCol.find({}, {'_id': 0}))
    csdDF = pd.DataFrame(csdCol.find({}, {'_id': 0}))

    return popDF, csdDF


def makeFigAb():
    popDF, csdDF = conDB()

    fig = px.bar(csdDF,
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
                                                       'quadratic-in-out'}}]}]}]
    )

    return fig


def makeFigRel():
    popDF, csdDF = conDB()

    popAllDF = popDF[popDF['행정기관'] == '전국']
    popAllDF = popDF[popDF['구분'] == '총인구수']

    resultDF = popAllDF.iloc[13:, 2:4]
    resultDF = pd.DataFrame.reset_index(resultDF).iloc[:, 1:]

    resultDF = csd

    fig = px.bar(csdDF,
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
                                                       'quadratic-in-out'}}]}]}]
    )

    return fig
