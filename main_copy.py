import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import graphpkg.testGraph as gt
import graphpkg.citySubject as gcs
import graphpkg.cityDoct as cd
import graphpkg.cityDoct2 as cd2
import graphpkg.Docincrease as gd
import graphpkg.LocalDocPerPop as gldp
import graphpkg.OECDfig as oecdfig
import iddModel.doctor as idoct

def makeDDFigure(dfDeadDoctor,year):
    year = str(year)

    exdfDeadPerson0 = dfDeadDoctor[0].iloc[:,26:]
    exdfDeadPerson0['성별']='Man'
    exdfDeadPerson1 = dfDeadDoctor[1].iloc[:,26:]
    exdfDeadPerson1['성별']='Woman'
    exdfDeadPerson = pd.concat([exdfDeadPerson0,exdfDeadPerson1])
    exdfDeadPerson = exdfDeadPerson.reset_index().rename(columns={"index": "연도"}).set_index('성별')

    deadPersonDict = {}

    for i in range(1952,2048):
        data = exdfDeadPerson[exdfDeadPerson['연도']==i]
        data.drop(['연도'], axis='columns', inplace=True)
        data = data.rename_axis(None).T
        data = data.reset_index().rename(columns={'index':'age'})
        deadPersonDict.setdefault(str(i), data)
    
    dead = deadPersonDict[year]
    trace3 = go.Bar(x=dead.age, y=dead.Man, name='남자',text=dead.Man,textposition='outside')
    trace4 = go.Bar(x=dead.age, y=dead.Woman, name='여자',text=dead.Woman,textposition='outside')

    data = [trace3, trace4]
    layout = go.Layout(title=year+'년 연령별 성별 사망 의사 수')
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
       # height=500,
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=0),
        showlegend=True,
        yaxis=dict(range=[0,20])
       
    )
    return fig

def makeNDFigure(dfNewDoctor,year):
    year = str(year)

    exdfNewPerson0 = dfNewDoctor[0].iloc[:,26:40]
    exdfNewPerson0['성별']='Man'
    exdfNewPerson1 = dfNewDoctor[1].iloc[:,26:40]
    exdfNewPerson1['성별']='Woman'
    exdfNewPerson = pd.concat([exdfNewPerson0,exdfNewPerson1])
    exdfNewPerson = exdfNewPerson.reset_index().rename(columns={"index": "연도"}).set_index('성별')

    newPersonDict = {}

    for i in range(1952,2048):
        data = exdfNewPerson[exdfNewPerson['연도']==i]
        data.drop(['연도'], axis='columns', inplace=True)
        data = data.rename_axis(None).T
        data = data.reset_index().rename(columns={'index':'age'})
        newPersonDict.setdefault(str(i), data)
    
    new = newPersonDict[year]
    trace3 = go.Bar(x=new.age, y=new.Man, name='남자',text=new.Man,textposition='outside')
    trace4 = go.Bar(x=new.age, y=new.Woman, name='여자',text=new.Woman,textposition='outside')

    data = [trace3, trace4]
    layout = go.Layout(title=year+'년 연령별 성별 신규 의사 수')
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
       # height=500,
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=0),
        showlegend=True,
        yaxis=dict(range=[0,1600])
       
    )
    return fig

def makeRDFigure(dfRetireDoctor,year):
    year = str(year)

    exdfRetirePerson0 = dfRetireDoctor[0].iloc[:,26:]
    exdfRetirePerson0['성별']='Man'
    exdfRetirePerson1 = dfRetireDoctor[1].iloc[:,26:]
    exdfRetirePerson1['성별']='Woman'
    exdfRetirePerson = pd.concat([exdfRetirePerson0,exdfRetirePerson1])
    exdfRetirePerson = exdfRetirePerson.reset_index().rename(columns={"index": "연도"}).set_index('성별')

    retirePersonDict = {}

    for i in range(1952,2048):
        data = exdfRetirePerson[exdfRetirePerson['연도']==i]
        data.drop(['연도'], axis='columns', inplace=True)
        data = data.rename_axis(None).T
        data = data.reset_index().rename(columns={'index':'age'})
        retirePersonDict.setdefault(str(i), data)
    
    retire = retirePersonDict[year]
    trace3 = go.Bar(x=retire.age, y=retire.Man, name='남자',text=retire.Man,textposition='outside')
    trace4 = go.Bar(x=retire.age, y=retire.Woman, name='여자',text=retire.Woman,textposition='outside')

    data = [trace3, trace4]
    layout = go.Layout(title=year+'년 연령별 성별 은퇴 의사 수')
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
       # height=500,
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=0),
        showlegend=True,
        yaxis=dict(range=[0,80])
       
    )
    return fig

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

npBasicPopulation = np.zeros([22,4])
for i in range(22):
        npBasicPopulation[i] = np.array([3000,50,0.6,0.6])

tuningSetAgeRate = [[0.8, 0.1, 0.1, 0.25, 0.1, 0.15],[26,26,28,28,27,27],[40, 40, 40, 40, 40, 40]]
tuningSetRetireRate = [[1.1, 1.05],[30, 30],[1.0, 1.0]]

dfResultData = idoct.makeResultData(npBasicPopulation,[tuningSetAgeRate,tuningSetRetireRate])

dfTotalDoctor = [dfResultData[0],dfResultData[1],dfResultData[0]+dfResultData[1]] # 의사수
dfNewDoctor = [dfResultData[2],dfResultData[3],dfResultData[2]+dfResultData[3]]    # 신규의사수
dfDeadDoctor = [dfResultData[4],dfResultData[5],dfResultData[4]+dfResultData[5]]   # 사망자수
dfRetireDoctor = [dfResultData[6],dfResultData[7],dfResultData[6]+dfResultData[7]] # 은퇴자수
dfThousandPerDoctor = idoct.makeThousandPerDoctor(dfTotalDoctor, idoct.npPopulation) # 1000명당 의사수


BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
app = dash.Dash(__name__, external_stylesheets=[BS])


colors = {
    'background': '#F2F2F2',
    'text': '#151515'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    dcc.Input(id='input-1-state', type='number', value=3000, step=100),
    dcc.Input(id='input-2-state', type='number', value=50, step=50),
    dcc.Input(id='input-3-state', type='number', value=0.6, step=0.1, max=1),
    dcc.Input(id='input-4-state', type='number', value=0.6, step=0.1, max=1),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),

    html.Div(id='output-state'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.Div(children='전체 의사수', style={'textAlign': 'center','color': colors['text']}),
    #dcc.Graph(id='td-graph'),

    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('신규 의사수'),
    dcc.Graph(id='nd-graph'),
    dcc.Slider(
        id='nd-year-slider',
        min=1952,
        max=2047,
        value=2018,
        marks={i: '{}'.format(i) for i in range(1952,2047)},
        step=1
    ),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('사망 의사수'),
    dcc.Graph(id='dd-graph'),
    dcc.Slider(
        id='dd-year-slider',
        min=1952,
        max=2047,
        value=2018,
        marks={i: '{}'.format(i) for i in range(1952,2047)},
        step=1
    ),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('은퇴 의사수'),
    dcc.Graph(id='rd-graph'),
    dcc.Slider(
        id='rd-year-slider',
        min=1952,
        max=2047,
        value=2018,
        marks={i: '{}'.format(i) for i in range(1952,2047)},
        step=1
    ),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('─────────────────────────────────────────────────────────────'),
    html.H1('1000명당 의사수'),
    #dcc.Graph(id='tpd-graph'),
])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value'),
               State('input-3-state', 'value'),
               State('input-4-state', 'value')])
def changeParameter(n_clicks, input1, input2, input3, input4):
    global tuningSetAgeRate, tuningSetRetireRate, dfResultData, dfResultPerson, dfNewPerson, dfDeadPerson, dfRetirePerson, dfThousandPerDoctor
    
    for i in range(22):
        npBasicPopulation[i] = np.array([input1,input2,input3,input4])

    tuningSetAgeRate = [[0.8, 0.1, 0.1, 0.25, 0.1, 0.15],[26,26,28,28,27,27],[40, 40, 40, 40, 40, 40]]
    tuningSetRetireRate = [[1.1, 1.05],[30, 30],[1.0, 1.0]]

    dfResultData = idoct.makeResultData(npBasicPopulation,[tuningSetAgeRate,tuningSetRetireRate])

    dfTotalDoctor = [dfResultData[0],dfResultData[1],dfResultData[0]+dfResultData[1]] # 의사수
    dfNewDoctor = [dfResultData[2],dfResultData[3],dfResultData[2]+dfResultData[3]]    # 신규의사수
    dfDeadDoctor = [dfResultData[4],dfResultData[5],dfResultData[4]+dfResultData[5]]   # 사망자수
    dfRetireDoctor = [dfResultData[6],dfResultData[7],dfResultData[6]+dfResultData[7]] # 은퇴자수
    dfThousandPerDoctor = idoct.makeThousandPerDoctor(dfTotalDoctor, idoct.npPopulation) # 1000명당 의사수

    return u'''
        의사고시 합격자 중 의대졸업인원 {}명,
        의전원졸업 {}명,
        의대졸업인원 남성비율 {}%,
        의대졸업인원 여성비율 {}%
    '''.format(input1, input2, input3*100, input4*100)


# 전체 의사수 그래프 콜백함수
@app.callback(Output('td-graph', 'figure'),
              [Input('output-state', 'children')])
def makeTDGraph(input):
    # use dfResultPerson
    global dfResultPerson
    fig = gcs.makeFigAb()

    return fig

# 신규 의사수 그래프 콜백함수
@app.callback(Output('nd-graph', 'figure'),
              [Input('output-state', 'children'),Input('nd-year-slider', 'value')])
def makeNDGraph(input1, input2):
    # use dfNewDoctor  
    global dfNewDoctor
    fig = makeNDFigure(dfNewDoctor,input2)
    print(input1)
    return fig

# 사망 의사수 그래프 콜백함수
@app.callback(Output('dd-graph', 'figure'),
              [Input('output-state', 'children'),Input('dd-year-slider', 'value')])
def makeDDGraph(input1, input2):
    # use dfDeadDoctor
    global dfDeadDoctor
    fig = makeDDFigure(dfDeadDoctor,input2)

    return fig

# 은퇴 의사수 그래프 콜백함수
@app.callback(Output('rd-graph', 'figure'),
              [Input('output-state', 'children'),Input('rd-year-slider', 'value')])
def makeRDGraph(input, input2):
    # use dfRetireDoctor
    global dfRetireDoctor
    fig = makeRDFigure(dfRetireDoctor,input2)

    return fig

# 1000명당 의사수 그래프 콜백함수
@app.callback(Output('tpd-graph', 'figure'),
              [Input('output-state', 'children')])
def makeTPDGraph(input):
    # use dfThousandPerDoctor
    global dfThousandPerDoctor
    fig = gcs.makeFigAb()

    return fig

if __name__ == '__main__':
    app.run_server(
        port=50003,
        host='0.0.0.0'
    )