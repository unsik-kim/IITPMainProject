import pymongo
from pymongo import MongoClient
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


myclient = MongoClient('218.150.247.209:2017',
                       username='unsik',
                       password='',
                       authSource='admin',
                       authMechanism='SCRAM-SHA-256')

newDB = myclient['FriDB']
newCollection = newDB['CityDoct']
newCollection2 = newDB['DocPass']

def reduce_doc(doc):
    for i in range(0, 10):
        doc.iloc[i+1, 3] = doc.iloc[i+1, 1]-doc.iloc[i,1]-doc.iloc[i+1,2]
    return doc

def makeFigure():
    doc_tot = pd.DataFrame(newCollection.find({'시도':'계','의료인력':'의사'},{'_id':0}))
    doc_tot = doc_tot[['년도', '값']]
    doc_tot.columns = ['year', 'total']
    
    new_doc = pd.DataFrame(newCollection2.find({},{'_id':0}))
    new_doc = new_doc[::-1]
    new_doc['년도'] = [2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    new_doc.columns = ['year', 'apply','Pass','PassRate']
    doc = pd.merge(doc_tot, new_doc, on = 'year' , how='left')
    doc = doc[['year', 'total', 'Pass']]
    doc['reduce'] = np.nan
    doc = reduce_doc(doc)

    total = doc['total'].iloc[1:,]
    year = doc['year'].iloc[1:, ]
    doc_pass = doc['Pass'].iloc[1:,]
    y_value = doc['reduce'].iloc[1:,]
    inver_y_val = -y_value

    years = list(year)
    doc_pass = list(doc_pass)
    inver_y_val = list(inver_y_val)
    total = list(total)


    fig = go.Figure()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])


    fig.add_trace(go.Scatter(x=years, y=total,
                        mode='lines',    
                        name='의료 인력'), secondary_y=False)

    fig.add_trace(go.Bar(x=years, y = doc_pass,
                    base=0,
                    marker_color='crimson',
                    name='의료인력 증가'), secondary_y=True,)
    fig.add_trace(go.Bar(x= years, y=y_value,
                    base = inver_y_val,
                    marker_color='lightslategrey',    
                    name='이탈하는 의료 인력 수'), secondary_y=True,)

    # Add figure title
    fig.update_layout(
        title_text="의료인력 증감 그래프", height=650
    )

    # Set x-axis title
    fig.update_xaxes(title_text="년")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>매 년 의료 인력 수</b>", secondary_y=False, range=[50000,105000])
    fig.update_yaxes(title_text="<b>의료 인력 증감 수 </b>", secondary_y=True, range=[-3500,15000])

    return fig