import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

import pymongo
from pymongo import MongoClient

myclient = MongoClient('218.150.247.209:2017',
                       username='unsik',
                       password='',
                       authSource='admin',
                       authMechanism='SCRAM-SHA-256')
DB = myclient['newDB']
Collection = DB['DocPopData']
aDataDF = pd.DataFrame(Collection.find({'데이터구분': '천명당인원수'}, {'_id': 0}))

myDB = myclient['FriDB']
myCollection = myDB['OecdDoc']
OECD = pd.DataFrame(myCollection.find({}, {"_id": 0}))


def makeFigure():
    aDataJobDF = aDataDF.groupby(['행정구분', '년도', '데이터구분']).sum()
    aDataJobDF = aDataJobDF.reset_index()
    aDataJobLoclaDF = aDataJobDF.groupby(['년도', '데이터구분']).mean()

    yearList = []
    for i in aDataDF.groupby('년도').mean().index:
        yearList.append(int(i))
    yearList = np.array(yearList)

    year = yearList
    y_all = list(round(aDataJobLoclaDF['값'], 3))
    year = year.reshape(-1, 1)
    line_fitter = LinearRegression()
    X = year
    y = y_all
    line_fitter.fit(X, y)
    y_predicted = line_fitter.predict(X)
    gradient = line_fitter.coef_  # 기울기
    gradient = gradient[0]
    a = X.T
    a = a[0]
    a = list(a)
    y_predicted = list(y_predicted)

    for i in range(2020, 2060):
        a.append(str(i))
        y_predicted.append(float(line_fitter.predict([[i]])))

    fig = px.scatter(aDataJobDF, x='년도', y='값', color='행정구분',
                     title='국내 인구 1000명당 의사 수와 예측',
                     width=2000,
                     height=1000,
                     labels={
                         "년도": "",
                         "값": "의사 수",
                         "지역": "          지역"
                     })

    oecdX, oecdY = returnOECD()

    fig.add_trace(go.Scatter(x=a, y=y_predicted,
                             mode='lines+markers',
                             name='korea regression'))

    fig.add_trace(go.Scatter(x=oecdX, y=oecdY,
                             mode='lines+markers',
                             name='OECD regression'))

    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=10),
        font_family='Malgun Gothic',
        font_size=15,
        title_font_family='Malgun Gothic',
        title_font_color="red",
        title_font_size=25
    )

    return fig


def returnOECD():
    OECD_rel = OECD[OECD['구분'] == "1000명당 의사수"]
    OECD_rel.drop(['구분'], axis='columns', inplace=True)
    OECD_mean = OECD_rel.groupby(['년도']).mean()
    OECD_mean.reset_index(inplace=True)
    year = np.array(OECD_mean['년도'])
    y2 = np.array(OECD_mean['값'])
    year = year.reshape(-1, 1)
    line_fitter = LinearRegression()
    X = year
    y = y2
    line_fitter.fit(X, y)
    y_predicted = line_fitter.predict(X)
    gradient = line_fitter.coef_  # 기울기
    gradient = gradient[0]
    a = X.T
    a = a[0]
    a = list(a)
    y_predicted = list(y_predicted)

    for i in range(2020, 2060):
        a.append(str(i))
        y_predicted.append(float(line_fitter.predict([[i]])))

    return a, y_predicted
