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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

npBasicPopulation = np.zeros([22,4])
for i in range(22):
        npBasicPopulation[i] = np.array([3000,50,0.6,0.6])

tuningSetAgeRate =  [[25,40,25,1.1],
                    [25,40,27,1.1],
                    [25,40,25,1.1],
                    [25,40,25,1.1],
                    [25,40,27,1.1],
                    [25,40,25,1.1]]
                      
tuningSetRetireRate = [[1.1,35,1],[1.1,35,1]]

dfResultData = idoct.makeResultData(npBasicPopulation,[tuningSetAgeRate,tuningSetRetireRate])

dfTotalDoctor = [dfResultData[0],dfResultData[1],dfResultData[0]+dfResultData[1]] # 의사수
dfNewDoctor = [dfResultData[2],dfResultData[3],dfResultData[2]+dfResultData[3]]    # 신규의사수
dfDeadDoctor = [dfResultData[4],dfResultData[5],dfResultData[4]+dfResultData[5]]   # 사망자수
dfRetireDoctor = [dfResultData[6],dfResultData[7],dfResultData[6]+dfResultData[7]] # 은퇴자수
dfThousandPerDoctor = idoct.makeThousandPerDoctor(dfTotalDoctor, idoct.npPopulation) # 1000명당 의사수
dfPopulation = pd.DataFrame(np.around(idoct.npPopulation))
dfPopulation.index = range(1950, 2048)
dfPopulation


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

sliderMarks= {(i):{'label':str(i),'style':{'writing-mode': 'vertical-rl'}}for i in range(1955,2050,5)}
sliderMarks[1952]= {'label':'1952','style':{'writing-mode': 'vertical-rl'}}
sliderMarks[2047]= {'label':'2047','style':{'writing-mode': 'vertical-rl'}}

app.layout = html.Div([
    dcc.Input(id='input-1-state', type='number', value=3000),
    dcc.Input(id='input-2-state', type='number', value=50),
    dcc.Input(id='input-3-state', type='number', value=0.6),
    dcc.Input(id='input-4-state', type='number', value=0.6),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),

    html.Div(id='output-state'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('전체 의사수'),
    html.H3('연도별, 성별 전체 의사수'),
    dcc.Graph(id='td-graph'),
    dcc.Slider(
        id='and-year-slider',
        min=1952,
        max=2047,
        value=2018,
        marks = sliderMarks,
        step=1,
        updatemode='drag'
    ),
    html.H1('.'),
    html.H3('연간 전체 의사수'),
    dcc.Graph(id='tdy-graph'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('신규 의사수'),
    html.H3('연도별, 성별 신규 의사수'),
    dcc.Graph(id='nd-graph'),
    dcc.Slider(
        id='nd-year-slider',
        min=1952,
        max=2047,
        value=2018,
        marks=sliderMarks,
        step=1
    ),
    html.H1('.'),
    html.H3('연간 신규 의사수'),
    dcc.Graph(id='ndy-graph'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('사망 의사수'),
    html.H3('연도별, 성별 사망 의사수'),
    dcc.Graph(id='dd-graph'),
    dcc.Slider(
        id='dd-year-slider',
        min=1952,
        max=2047,
        value=2018,
        marks=sliderMarks,
        step=1
    ),
    html.H1('.'),
    html.H3('연간 사망 의사수'),
    dcc.Graph(id='ddy-graph'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('은퇴 의사수'),
    html.H3('연도별, 성별 은퇴 의사수'),
    dcc.Graph(id='rd-graph'),
    dcc.Slider(
        id='rd-year-slider',
        min=1952,
        max=2047,
        value=2018,
        marks=sliderMarks,
        step=1
    ),
    html.H1('.'),
    html.H3('연간 은퇴 의사수'),
    dcc.Graph(id='rdy-graph'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('1000명당 의사수'),
    dcc.Graph(id='tpd-graph'),
])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value'),
               State('input-3-state', 'value'),
               State('input-4-state', 'value')])
def changeParameter(n_clicks, input1, input2, input3, input4):
    global tuningSetAgeRate, tuningSetRetireRate, dfResultData, dfTotalDoctor, dfNewDoctor, dfDeadDoctor, dfRetireDoctor, dfThousandPerDoctor, dfPopulation
    
    for i in range(22):
        npBasicPopulation[i] = np.array([input1,input2,input3,input4])

    dfResultData = idoct.makeResultData(npBasicPopulation,[tuningSetAgeRate,tuningSetRetireRate])

    dfTotalDoctor = [dfResultData[0],dfResultData[1],dfResultData[0]+dfResultData[1]] # 의사수
    dfNewDoctor = [dfResultData[2],dfResultData[3],dfResultData[2]+dfResultData[3]]    # 신규의사수
    dfDeadDoctor = [dfResultData[4],dfResultData[5],dfResultData[4]+dfResultData[5]]   # 사망자수
    dfRetireDoctor = [dfResultData[6],dfResultData[7],dfResultData[6]+dfResultData[7]] # 은퇴자수
    dfThousandPerDoctor = idoct.makeThousandPerDoctor(dfTotalDoctor, idoct.npPopulation) # 1000명당 의사수


    return u'''
        2025년부터 의사고시 합격자 중 의대졸업인원 {}명,
        의전원졸업 {}명,
        의대졸업인원 남성비율 {}%,
        의대졸업인원 여성비율 {}%
    '''.format(input1, input2, input3*100, input4*100)


# 전체 의사수 그래프 콜백함수
@app.callback(Output('td-graph', 'figure'),
              [Input('output-state', 'children'),Input('and-year-slider', 'value')])
def makeTDGraph(input1, input2):
    # use dfResultPerson
    global dfTotalDoctor
    fig = dg.makeANDFigure(dfTotalDoctor,input2)

    return fig

# 연간 전체 의사수 그래프 콜백함수
@app.callback(Output('tdy-graph', 'figure'),
              [Input('output-state', 'children')])
def makeTDYGraph(input1):
    # use dfResultPerson
    global dfTotalDoctor, dfPopulation
    fig = dg.makeFigureSumDoc(dfTotalDoctor, dfPopulation)

    return fig

# 신규 의사수 그래프 콜백함수
@app.callback(Output('nd-graph', 'figure'),
              [Input('output-state', 'children'),Input('nd-year-slider', 'value')])
def makeNDGraph(input1, input2):
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
              [Input('output-state', 'children'),Input('dd-year-slider', 'value')])
def makeDDGraph(input1, input2):
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
              [Input('output-state', 'children'),Input('rd-year-slider', 'value')])
def makeRDGraph(input, input2):
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
        port=50008,
        host='0.0.0.0'
    )