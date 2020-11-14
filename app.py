# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc

import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import graphpkg.doctorGraph as dg
import iddModel.doctor as idoct
import base64
import os
from pages import (
    main,
    page1,
    page2,
    page3,
    page4,
    page5,
    more
)
#---데이터---
npBasicPopulation = np.zeros([22,4])
for i in range(22):
        npBasicPopulation[i] = np.array([3000,50,0.6,0.6])

tuningSetAgeRate = [[0.5, 0.5, 0.3, 0.8, 0.6, 0.6],[26,26,28,28,27,27],[40, 40, 40, 40, 40, 40]]
tuningSetRetireRate = [[1.2, 1.2],[30, 30],[5.6, 5.6]]

dfResultData = idoct.makeResultData(npBasicPopulation,[tuningSetAgeRate,tuningSetRetireRate])

dfTotalDoctor = [dfResultData[0],dfResultData[1],dfResultData[0]+dfResultData[1]] # 의사수
dfNewDoctor = [dfResultData[2],dfResultData[3],dfResultData[2]+dfResultData[3]]    # 신규의사수
dfDeadDoctor = [dfResultData[4],dfResultData[5],dfResultData[4]+dfResultData[5]]   # 사망자수
dfRetireDoctor = [dfResultData[6],dfResultData[7],dfResultData[6]+dfResultData[7]] # 은퇴자수
dfThousandPerDoctor = idoct.makeThousandPerDoctor(dfTotalDoctor, idoct.npPopulation) # 1000명당 의사수

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

#---app slider--
sliderMarks= {(i):{'label':str(i),'style':{'writing-mode': 'vertical-rl'}}for i in range(1955,2050,5)}
sliderMarks[1952]= {'label':'1952','style':{'writing-mode': 'vertical-rl'}}
sliderMarks[2047]= {'label':'2047','style':{'writing-mode': 'vertical-rl'}}

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash-financial-report/price-performance":
        return page1.create_layout(app)
    elif pathname == "/dash-financial-report/portfolio-management":
        return page2.create_layout(app)
    elif pathname == "/dash-financial-report/fees":
        return page3.create_layout(app)
    elif pathname == "/dash-financial-report/distributions":
        return page4.create_layout(app)
    elif pathname == "/dash-financial-report/news-and-reviews":
        return page5.create_layout(app)
    elif pathname == "/dash-financial-report/full-view":
        return (
            main.create_layout(app),
            page1.create_layout(app),
            page2.create_layout(app),
            page3.create_layout(app),
            page4.create_layout(app),
            page5.create_layout(app),
        )
    else:
        return main.create_layout(app)


#---app slider--
sliderMarks= {(i):{'label':str(i),'style':{'writing-mode': 'vertical-rl'}}for i in range(1955,2050,5)}
sliderMarks[1952]= {'label':'1952','style':{'writing-mode': 'vertical-rl'}}
sliderMarks[2047]= {'label':'2047','style':{'writing-mode': 'vertical-rl'}}

# submit 눌렀을때-> 받아온 값으로 새로 df만들고 return으로 값이 변화하는지 보여주기 
@app.callback(Output('output-state', 'children'),
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value'),
               State('input-3-state', 'value'),
               State('input-4-state', 'value')])
def changeParameter(n_clicks, input1, input2, input3, input4):
    global tuningSetAgeRate, tuningSetRetireRate, dfResultData, dfTotalDoctor, dfNewDoctor, dfDeadDoctor, dfRetireDoctor, dfThousandPerDoctor
    
    for i in range(22):
        npBasicPopulation[i] = np.array([input1,input2,input3,input4])

    dfResultData = idoct.makeResultData(npBasicPopulation,[tuningSetAgeRate,tuningSetRetireRate])

    dfTotalDoctor = [dfResultData[0],dfResultData[1],dfResultData[0]+dfResultData[1]] # 의사수
    dfNewDoctor = [dfResultData[2],dfResultData[3],dfResultData[2]+dfResultData[3]]    # 신규의사수
    dfDeadDoctor = [dfResultData[4],dfResultData[5],dfResultData[4]+dfResultData[5]]   # 사망자수
    dfRetireDoctor = [dfResultData[6],dfResultData[7],dfResultData[6]+dfResultData[7]] # 은퇴자수
    dfThousandPerDoctor = idoct.makeThousandPerDoctor(dfTotalDoctor, idoct.npPopulation) # 1000명당 의사수


# 전체 의사수 그래프 콜백함수
@app.callback(Output('td-graph', 'figure'),
              [Input('output-state', 'children'),Input('and-year-slider', 'value'),Input('submit-button-state', 'n_clicks')])
def makeTDGraph(input1, input2, input3):
    # use dfResultPerson
    global dfTotalDoctor
    fig = dg.makeANDFigure(dfTotalDoctor,input2)

    return fig

# 연간 전체 의사수 그래프 콜백함수
@app.callback(Output('tdy-graph', 'figure'),
              [Input('output-state', 'children')])
def makeTDYGraph(input1):
    # use dfResultPerson
    global dfTotalDoctor
    fig = dg.makeFigureSumDoc(dfTotalDoctor)

    return fig

# 신규 의사수 그래프 콜백함수
@app.callback(Output('nd-graph', 'figure'),
              [Input('output-state', 'children'),Input('nd-year-slider', 'value'),Input('submit-button-state', 'n_clicks')])
def makeNDGraph(input1, input2, input3):
    # use dfNewDoctor  
    global dfNewDoctor
    fig = dg.makeNDFigure(dfNewDoctor,input2)

    return fig

# 연간 신규 의사수 그래프 콜백함수
@app.callback(Output('ndy-graph', 'figure'),
              [Input('output-state', 'children')])
def makeNDYGraph(input1):
    # use dfNewDoctor  
    global dfNewDoctor
    fig = dg.makeFigureNewDoc(dfNewDoctor)

    return fig


# 사망 의사수 그래프 콜백함수
@app.callback(Output('dd-graph', 'figure'),
              [Input('output-state', 'children'),Input('dd-year-slider', 'value'),Input('submit-button-state', 'n_clicks')])
def makeDDGraph(input1, input2, input3):
    # use dfDeadDoctor
    global dfDeadDoctor
    fig = dg.makeDDFigure(dfDeadDoctor,input2)

    return fig

# 연간 사망 의사수 그래프 콜백함수
@app.callback(Output('ddy-graph', 'figure'),
              [Input('output-state', 'children')])
def makeDDYGraph(input1):
    # use dfDeadDoctor
    global dfDeadDoctor
    fig = dg.makeFigureDeadDoc(dfDeadDoctor)

    return fig

# 은퇴 의사수 그래프 콜백함수
@app.callback(Output('rd-graph', 'figure'),
              [Input('output-state', 'children'),Input('rd-year-slider', 'value'),Input('submit-button-state', 'n_clicks')])
def makeRDGraph(input, input2, input3):
    # use dfRetireDoctor
    global dfRetireDoctor
    fig = dg.makeRDFigure(dfRetireDoctor,input2)

    return fig

# 연간 은퇴 의사수 그래프 콜백함수
@app.callback(Output('rdy-graph', 'figure'),
              [Input('output-state', 'children')])
def makeRDYGraph(input):
    # use dfRetireDoctor
    global dfRetireDoctor
    fig = dg.makeFigureRetireDoc(dfRetireDoctor)

    return fig

# 1000명당 의사수 그래프 콜백함수
@app.callback(Output('tpd-graph', 'figure'),
              [Input('output-state', 'children')])
def makeTPDGraph(input):
    # use dfThousandPerDoctor
    global dfThousandPerDoctor
    fig = dg.makeFigureDocPer1000(dfThousandPerDoctor)

    return fig
if __name__ == '__main__':
    app.run_server(
        port=50006,
        host='0.0.0.0'
    )