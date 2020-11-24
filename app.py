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
    fullmain,
    page1,
    page2,
    page3,
    page4,
    page5,
    more,
    data
)
#---데이터---
valueSet = [3000,50,0.6,0.6]

npBasicPopulation = np.zeros([21,4])
for i in range(21):
        npBasicPopulation[i] = np.array([3000,50,0.6,0.6])

tuningSetAgeRate = [[0.5, 0.5, 0.3, 0.8, 0.6, 0.6],[26,26,28,28,27,27],[40, 40, 40, 40, 40, 40]]
tuningSetRetireRate = [[1.2, 1.2],[30, 30],[5.6, 5.6]]

npRealDoctor = idoct.npRealDoctor
npRealWorkDoctor = idoct.npRealWorkDoctor
dfResultData = idoct.makeResultData(npBasicPopulation,[tuningSetAgeRate,tuningSetRetireRate])
dfTotalDoctor = [dfResultData[0],dfResultData[1],dfResultData[0]+dfResultData[1]] # 의사수
dfNewDoctor = [dfResultData[2],dfResultData[3],dfResultData[2]+dfResultData[3]]    # 신규의사수
dfDeadDoctor = [dfResultData[4],dfResultData[5],dfResultData[4]+dfResultData[5]]   # 사망자수
dfRetireDoctor = [dfResultData[6],dfResultData[7],dfResultData[6]+dfResultData[7]] # 은퇴자수
dfThousandPerDoctor = idoct.makeThousandPerDoctor(dfTotalDoctor, idoct.npPopulation) # 1000명당 의사수
dfPopulation = pd.DataFrame(np.around(idoct.npPopulation))
dfPopulation.index = range(1950, 2048)
npDoctorNum = np.around(np.array(dfThousandPerDoctor.iloc[60:]).T[0],2)
npVisitDay = np.array(idoct.dfVisitDays['국내내원일수'])
npVisitNumYear = (npVisitDay*1000)/npDoctorNum # 국내의사 1인당 외래진료수
npVisitNumYearOECD = np.array(idoct.dfVisitDays['OECD1인당연간외래진료수'])
dfVisitNumYear = pd.DataFrame(np.array([npVisitNumYear,npVisitNumYearOECD]).T)
dfVisitNumYear.index = range(2010,2048)
dfVisitNumYear.columns = ['대한민국','OECD평균']

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/idd-doctor-report/page1":
        return page1.create_layout(app,valueSet)
    elif pathname == "/idd-doctor-report/page2":
        return page2.create_layout(app,valueSet)
    elif pathname == "/idd-doctor-report/page3":
        return page3.create_layout(app,valueSet)
    elif pathname == "/idd-doctor-report/page4":
        return page4.create_layout(app,valueSet)
    elif pathname == "/idd-doctor-report/page5":
        return page5.create_layout(app,valueSet)
    elif pathname == "/idd-doctor-report/more":
        return more.create_layout(app)
    elif pathname == "/idd-doctor-report/data":
        return data.create_layout(app,valueSet)
    elif pathname == "/idd-doctor-report/full-view":
        return (
            fullmain.create_layout(app),         
            page1.create_layout(app,valueSet),
            page2.create_layout(app,valueSet),
            page3.create_layout(app,valueSet),
            page4.create_layout(app,valueSet),
            page5.create_layout(app,valueSet),
            more.create_layout(app),
            data.create_layout(app,valueSet)
        )
    else:
        return main.create_layout(app)

# submit 눌렀을때-> 받아온 값으로 새로 df만들고 return으로 값이 변화하는지 보여주기 
@app.callback(Output('output-state', 'children'),
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value'),
               State('input-3-state', 'value'),
               State('input-4-state', 'value')])
def changeParameter(n_clicks, input1, input2, input3, input4):
    global tuningSetAgeRate, tuningSetRetireRate, dfResultData, dfTotalDoctor, dfNewDoctor, dfDeadDoctor, dfRetireDoctor, dfThousandPerDoctor, dfPopulation, npVisitNumYear, npVisitNumYearOECD, valueSet
    valueSet = [input1,input2,input3,input4]
    for i in range(21):
        npBasicPopulation[i] = np.array([input1,input2,input3,input4])

    dfResultData = idoct.makeResultData(npBasicPopulation,[tuningSetAgeRate,tuningSetRetireRate])

    dfTotalDoctor = [dfResultData[0],dfResultData[1],dfResultData[0]+dfResultData[1]] # 의사수
    dfNewDoctor = [dfResultData[2],dfResultData[3],dfResultData[2]+dfResultData[3]]    # 신규의사수
    dfDeadDoctor = [dfResultData[4],dfResultData[5],dfResultData[4]+dfResultData[5]]   # 사망자수
    dfRetireDoctor = [dfResultData[6],dfResultData[7],dfResultData[6]+dfResultData[7]] # 은퇴자수
    dfThousandPerDoctor = idoct.makeThousandPerDoctor(dfTotalDoctor, idoct.npPopulation) # 1000명당 의사수
    npDoctorNum = np.around(np.array(dfThousandPerDoctor.iloc[60:]).T[0],2)
    npVisitDay = np.array(idoct.dfVisitDays['국내내원일수'])
    npVisitNumYear = (npVisitDay*1000)/npDoctorNum # 국내의사 1인당 외래진료수
    npVisitNumYearOECD = np.array(idoct.dfVisitDays['OECD1인당연간외래진료수'])
    dfVisitNumYear = pd.DataFrame(np.array([npVisitNumYear,npVisitNumYearOECD]).T)

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
    global dfTotalDoctor, dfPopulation, npRealDoctor, npRealWorkDoctor
    fig = dg.makeFigureSumDoc(dfTotalDoctor,dfPopulation,npRealDoctor, npRealWorkDoctor)

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

# 의사 1명당 연간 진료수 그래프 콜백함수
@app.callback(Output('dpd-graph', 'figure'),
              [Input('output-state', 'children')])
def makeOPDGraph(input):
    # use dfThousandPerDoctor
    global npVisitNumYear, npVisitNumYearOECD
    fig = dg.makeFigureVisitDoctor([npVisitNumYear,npVisitNumYearOECD])

    return fig

if __name__ == '__main__':
    app.run_server(
        port=50001,
        host='0.0.0.0'
    )