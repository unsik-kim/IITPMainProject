import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pymongo
from pymongo import MongoClient

myclient = MongoClient('218.150.247.209:2017',
                    username='unsik',
                    password='',
                    authSource='admin',
                    authMechanism='SCRAM-SHA-256')
newDB = myclient['FriDB']
newCollection = newDB['CityDoct']

def makeFigure():
    dataDf = pd.DataFrame(newCollection.find({},{"_id":0}))
    spec_doct = pd.DataFrame(newCollection.find({"의료인력":"전문의"},{"_id":0}))
    doct = pd.DataFrame(newCollection.find({"의료인력":"의사"},{"_id":0}))

    dataDf = dataDf[dataDf['시도']!='계']
    spec_doct = spec_doct[spec_doct['시도']!='계']
    doct = doct[doct['시도']!='계']

    doct_Dict = {}
    for i in range(2008,2019):
        data = doct[doct['년도']==i]
        data.fillna(0)
        data.reset_index(drop=True)
        data.drop(['년도'], axis='columns', inplace=True)
        data.drop(['의료인력'],axis='columns', inplace=True)
        doct_Dict.setdefault(str(i), data)
        doct_Dict[str(i)] = doct_Dict[str(i)].fillna(0)
        doct_Dict[str(i)] = doct_Dict[str(i)].replace('-', 0)
    
    spec_doct_Dict = {}
    for i in range(2008,2019):
        data = spec_doct[spec_doct['년도']==i]
        data.fillna(0)
        data.reset_index(drop=True)
        data.drop(['년도'], axis='columns', inplace=True)
        data.drop(['의료인력'],axis='columns', inplace=True)
        spec_doct_Dict.setdefault(str(i), data)
        spec_doct_Dict[str(i)] = spec_doct_Dict[str(i)].fillna(0)
        spec_doct_Dict[str(i)] = spec_doct_Dict[str(i)].replace('-', 0)
    

    fig = make_subplots(rows=2, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}],[{'type':'domain'}, {'type':'domain'}]])
    year1 = '2008'
    year2 = '2018'

    fig.add_trace(
        go.Pie(labels=list(doct_Dict[year1].T.iloc[0]), values=list(doct_Dict[year1].T.iloc[1]),title=year1+'년 도시별 의사 수'),
        row=1, col=1
    )
    fig.add_trace(
        go.Pie(labels=list(doct_Dict[year2].T.iloc[0]), values=list(doct_Dict[year2].T.iloc[1]),title=year2+'년 도시별 의사 수'),
        row=1, col=2
    )
    fig.add_trace(
        go.Pie(labels=list(spec_doct_Dict[year1].T.iloc[0]), values=list(spec_doct_Dict[year1].T.iloc[1]),title=year1+'년 도시별 전문의 수'),
        row=2, col=1
    )
    fig.add_trace(
        go.Pie(labels=list(spec_doct_Dict[year2].T.iloc[0]), values=list(spec_doct_Dict[year2].T.iloc[1]),title=year2+'년 도시별 전문의 수'),
        row=2, col=2
    )

    fig.update_traces(textposition='inside')
    fig.update_layout(
        autosize=False,
        width=1300,
        height=1000)

    return fig

def makeFigure2():
    dataDf = pd.DataFrame(newCollection.find({},{"_id":0}))
    spec_doct = pd.DataFrame(newCollection.find({"의료인력":"전문의"},{"_id":0}))
    doct = pd.DataFrame(newCollection.find({"의료인력":"의사"},{"_id":0}))

    dataDf = dataDf[dataDf['시도']!='계']
    spec_doct = spec_doct[spec_doct['시도']!='계']
    doct = doct[doct['시도']!='계']

    doct_Dict = {}
    for i in range(2008,2019):
        data = doct[doct['년도']==i]
        data.fillna(0)
        data.reset_index(drop=True)
        data.drop(['년도'], axis='columns', inplace=True)
        data.drop(['의료인력'],axis='columns', inplace=True)
        doct_Dict.setdefault(str(i), data)
        doct_Dict[str(i)] = doct_Dict[str(i)].fillna(0)
        doct_Dict[str(i)] = doct_Dict[str(i)].replace('-', 0)
    
    spec_doct_Dict = {}
    for i in range(2008,2019):
        data = spec_doct[spec_doct['년도']==i]
        data.fillna(0)
        data.reset_index(drop=True)
        data.drop(['년도'], axis='columns', inplace=True)
        data.drop(['의료인력'],axis='columns', inplace=True)
        spec_doct_Dict.setdefault(str(i), data)
        spec_doct_Dict[str(i)] = spec_doct_Dict[str(i)].fillna(0)
        spec_doct_Dict[str(i)] = spec_doct_Dict[str(i)].replace('-', 0)
    fig = px.line(spec_doct, x=spec_doct['년도'], y=spec_doct['값'], color=spec_doct['시도'],title='시도별 전문의 수 통계')
    fig.update_layout(
        autosize=False,
        width=1300,
        height=800)

    return fig  