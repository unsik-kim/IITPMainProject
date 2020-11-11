import dash
import dash_bootstrap_components as dbc
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

#---Style----
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
sidebar = html.Div(
    [
        html.Div([html.A('IDD', href='/')], className="display-4",style={'font-weight': 'bold', 'fontSize': 50}),
        html.Hr(),
        html.P(
            "이슈에 데이터로 답하다", className="lead",
        ),
        dbc.Nav(
            [
                dbc.NavLink("1. 전체 의사 수", href="/page-1", id="page-1-link", style={'font-weight': 'bold', 'fontSize':20}),
                dbc.NavLink("2. 신규 의사 수", href="/page-2", id="page-2-link", style={'font-weight': 'bold', 'fontSize':20}),
                dbc.NavLink("3. 사망 의사 수", href="/page-3", id="page-3-link", style={'font-weight': 'bold', 'fontSize':20}),
                dbc.NavLink("4. 은퇴 의사 수", href="/page-4", id="page-4-link", style={'font-weight': 'bold', 'fontSize':20}),
                dbc.NavLink("5. 1000명당 의사 수", href="/page-5", id="page-5-link", style={'font-weight': 'bold', 'fontSize':20}),
                dbc.NavLink("Page 6", href="/page-6", id="page-6-link"),
                dbc.NavLink("Page 7", href="/page-7", id="page-7-link"),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
NUM_BOX_STYLE = {
    "margin-left": "18rem",
    "margin-right": "0.5rem"}
content = html.Div(id="page-content", style=CONTENT_STYLE)


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



#--app--
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#---app slider--
sliderMarks= {(i):{'label':str(i),'style':{'writing-mode': 'vertical-rl'}}for i in range(1955,2050,5)}
sliderMarks[1952]= {'label':'1952','style':{'writing-mode': 'vertical-rl'}}
sliderMarks[2047]= {'label':'2047','style':{'writing-mode': 'vertical-rl'}}

app.layout = html.Div([dcc.Location(id="url"), sidebar,content
])

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

    return u'''
        의대 입학 정원수 {}명,
        의전원 입학 정원수 {}명,
        의대졸업인원 남성비율 {}%,
        의전원졸업인원 남성비율 {}%
    '''.format(input1, input2, input3*100, input4*100)



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


#navbar 채우기 색
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 8)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 8)]

# navbar 변경할때 (페이지 주소 바뀔때)
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(

            children=[
                html.Div('[의료 4대 정책과 의료 파업]'),
                html.Img(src='222.239.90.78:52022/root/project/doctorPrj/IITPMainProject/pic.PNG'),
                html.Div(
                    children=[
                        html.Div(style={'border-radius': '25px 50px', 'background': '#F2F2F2', 'padding': '3%', 'width': '22%', 'height': '20%', 'float':'left', 'margin-right':'3%'},
                            children=[
                                html.H2('우리나라 의사 수',style={'font-family':'Nanum Gothic', 'font-weight': 'bold'}),
                                html.P('107928명')
                            ]
                        ),
                        html.Div(style={'border-radius': '25px 50px', 'background': '#F2F2F2', 'padding': '3%', 'width': '22%', 'height': '20%', 'float':'left', 'margin-right':'3%'},
                            children=[
                                html.H2('우리나라 인구 1000명당 의사 수',style={'font-family':'Nanum Gothic', 'font-weight': 'bold'}),
                                html.P('2.08명')
                            ]
                        ),
                        html.Div(style={'border-radius': '25px 50px', 'background': '#F2F2F2', 'padding': '3%', 'width': '22%', 'height': '20%', 'float':'left', 'margin-right':'3%'},
                            children=[
                                html.H2('OECD 회원국 인구 1000명당 의사 수',style={'font-family':'Nanum Gothic', 'font-weight': 'bold'}),
                                html.P('3.65명 19년기준')
                            ]
                        )
                    ]
                )
                
            ]
        )
    elif pathname == "/page-1":
        return html.Div(
            children=[
                html.Div('1. 전체 의사 수', style={'font-weight': 'bold',  'color': 'blue', 'fontSize': 34}),
                html.Br(),
                html.Div('<값 조절>', style={'font-weight': 'bold', 'fontSize': 20}),
                dcc.Input(id='input-1-state', type='number', value=3000, min=0, step=100),
                dcc.Input(id='input-2-state', type='number', value=50, min=0, step=50),
                dcc.Input(id='input-3-state', type='number', value=0.6, step=0.1, min=0, max=1),
                dcc.Input(id='input-4-state', type='number', value=0.6, step=0.1, min=0, max=1),
                html.Button(id='submit-button-state', n_clicks=0, children='변경'),
                html.Br(),
                html.Div(id='output-state', style={'font-weight': 'bold', 'fontSize': 20}),
                html.Br(),
                html.Br(),
                html.Div('[연도별, 성별 전체 의사수]', style={'font-weight': 'bold', 'fontSize': 25}),
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
                html.Br(), html.Br(),
                html.Div('[연간 전체 의사수]', style={'font-weight': 'bold', 'fontSize': 25}),
                dcc.Graph(id='tdy-graph')
            ])  
    elif pathname == "/page-2":
        return html.Div(
            children=[
                html.Div('2. 신규 의사 수', style={'font-weight': 'bold',  'color': 'blue', 'fontSize': 34}),
                html.Br(),
                html.Div('<값 조절>', style={'font-weight': 'bold', 'fontSize': 20}),
                dcc.Input(id='input-1-state', type='number', value=3000, min=0, step=100),
                dcc.Input(id='input-2-state', type='number', value=50, min=0, step=50),
                dcc.Input(id='input-3-state', type='number', value=0.6, step=0.1, min=0, max=1),
                dcc.Input(id='input-4-state', type='number', value=0.6, step=0.1, min=0, max=1),
                html.Button(id='submit-button-state', n_clicks=0, children='변경'),
                html.Br(),
                html.Div(id='output-state', style={'font-weight': 'bold', 'fontSize': 20}),
                html.Div('[연도별, 성별 신규 의사수]', style={'font-weight': 'bold', 'fontSize': 25}),
                dcc.Graph(id='nd-graph'),
                dcc.Slider(
                    id='nd-year-slider',
                    min=1952,
                    max=2047,
                    value=2018,
                    marks=sliderMarks,
                    step=1
                ),
                html.Br(), html.Br(),
                html.Div('[연간 신규 의사수]', style={'font-weight': 'bold', 'fontSize': 25}),
                dcc.Graph(id='ndy-graph')
            ])
    elif pathname == "/page-3":
        return html.Div(
            children=[
                html.Div('3. 사망 의사 수', style={'font-weight': 'bold',  'color': 'blue', 'fontSize': 34}),
                html.Br(),
                html.Div('<값 조절>', style={'font-weight': 'bold', 'fontSize': 20}),
                dcc.Input(id='input-1-state', type='number', value=3000, min=0, step=100),
                dcc.Input(id='input-2-state', type='number', value=50, min=0, step=50),
                dcc.Input(id='input-3-state', type='number', value=0.6, step=0.1, min=0, max=1),
                dcc.Input(id='input-4-state', type='number', value=0.6, step=0.1, min=0, max=1),
                html.Button(id='submit-button-state', n_clicks=0, children='변경'),
                html.Br(),
                html.Div(id='output-state', style={'font-weight': 'bold', 'fontSize': 20}),
                html.Div('[연도별, 성별 사망 의사수]', style={'font-weight': 'bold', 'fontSize': 25}),
                dcc.Graph(id='dd-graph'),
                dcc.Slider(
                    id='dd-year-slider',
                    min=1952,
                    max=2047,
                    value=2018,
                    marks=sliderMarks,
                    step=1
                ),
                html.Br(), html.Br(),
                html.Div('[연간 사망 의사수]', style={'font-weight': 'bold', 'fontSize': 25}),
                dcc.Graph(id='ddy-graph'),
            ])
    elif pathname == "/page-4":
        return html.Div(
            children=[
                html.Div('4. 은퇴 의사 수', style={'font-weight': 'bold',  'color': 'blue', 'fontSize': 34}),
                html.Br(),
                html.Div('<값 조절>', style={'font-weight': 'bold', 'fontSize': 20}),
                dcc.Input(id='input-1-state', type='number', value=3000, min=0, step=100),
                dcc.Input(id='input-2-state', type='number', value=50, min=0, step=50),
                dcc.Input(id='input-3-state', type='number', value=0.6, step=0.1, min=0, max=1),
                dcc.Input(id='input-4-state', type='number', value=0.6, step=0.1, min=0, max=1),
                html.Button(id='submit-button-state', n_clicks=0, children='변경'),
                html.Br(),
                html.Div(id='output-state', style={'font-weight': 'bold', 'fontSize': 20}),
                html.Div('[연도별, 성별 은퇴 의사수]', style={'font-weight': 'bold', 'fontSize': 25}),
                dcc.Graph(id='rd-graph'),
                dcc.Slider(
                    id='rd-year-slider',
                    min=1952,
                    max=2047,
                    value=2018,
                    marks=sliderMarks,
                    step=1
                ),
                html.Br(), html.Br(),
                html.Div('[연간 사망 의사수]', style={'font-weight': 'bold', 'fontSize': 25}),
                dcc.Graph(id='rdy-graph')
            ])
    elif pathname == "/page-5":
        return html.Div(
            children=[
                html.Div('5. 1000명당 의사 수', style={'font-weight': 'bold',  'color': 'blue', 'fontSize': 34}),
                html.Br(),
                html.Div('<값 조절>', style={'font-weight': 'bold', 'fontSize': 20}),
                dcc.Input(id='input-1-state', type='number', value=3000, min=0, step=100),
                dcc.Input(id='input-2-state', type='number', value=50, min=0, step=50),
                dcc.Input(id='input-3-state', type='number', value=0.6, step=0.1, min=0, max=1),
                dcc.Input(id='input-4-state', type='number', value=0.6, step=0.1, min=0, max=1),
                html.Button(id='submit-button-state', n_clicks=0, children='변경'),
                html.Br(),
                html.Div(id='output-state', style={'font-weight': 'bold', 'fontSize': 20}),
                dcc.Graph(id='tpd-graph'),
            ])
    elif pathname == "/page-6":
        return html.P("?? 의사")
    elif pathname == "/page-7":
        return html.P("?? 의사")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == '__main__':
    app.run_server(
        port=50001,
        host='0.0.0.0'
    )