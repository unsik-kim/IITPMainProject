import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import connectDB
import pandas as pd
import plotly.graph_objects as go

# DB 연결
myclient = connectDB.connectDB()

myDB = myclient['FriDB']
popCol = myDB['Population']
csdCol = myDB['CitySubjectDoc']

popDF = pd.DataFrame(popCol.find({}, {'_id': 0}))
csdDF = pd.DataFrame(csdCol.find({}, {'_id': 0}))


def makeFigure():

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
