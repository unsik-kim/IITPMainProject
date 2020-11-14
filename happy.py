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
                dbc.NavLink("1. 전체 의사 수", href="/page-1", id="page-1-link", style={'font-family':'Malgun Gothic', 'font-weight': 'bold', 'fontSize':20}),
                dbc.NavLink("2. 신규 의사 수", href="/page-2", id="page-2-link", style={'font-family':'Malgun Gothic', 'font-weight': 'bold', 'fontSize':20}),
                dbc.NavLink("3. 사망 의사 수", href="/page-3", id="page-3-link", style={'font-family':'Malgun Gothic', 'font-weight': 'bold', 'fontSize':20}),
                dbc.NavLink("4. 은퇴 의사 수", href="/page-4", id="page-4-link", style={'font-family':'Malgun Gothic', 'font-weight': 'bold', 'fontSize':20}),
                dbc.NavLink("5. 1000명당 의사 수", href="/page-5", id="page-5-link", style={'font-family':'Malgun Gothic', 'font-weight': 'bold', 'fontSize':20}),
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
        의대 입학 남성비율 {}%,
        의전원 입학 남성비율 {}%
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
                    html.Div('[의료 4대 정책과 의료 파업]',style={'margin-bottom':'2%','text-align': 'center', 'font-family':'Malgun Gothic', 'font-weight': 'bold', 'fontSize': 34}),
                    html.Div(
                        children=[
                            html.Img(src='https://img.khan.co.kr/news/2020/08/26/l_2020082701003030200243311.jpg', style={'margin-left': '3%','margin-right': '3%', 'margin-top': '1%','border-radius': '25px','width': '30%', 'height': '32%', 'float':'left'}),
                            html.Div(
                                children=[
                                    html.Div('최근 의료 4대 정책 중 하나인 의학대학 정원 확대 및 공공의대 설립에 대한의사협회 등 의사들이 반발하며 의료 파업이 발생되었다. 의료파업을 주장하고 실행했던 대한의사협회의 주장도 현재 인구 감소율과 의사 증가율을 고려하면 의사 수 충분하다며 데이터를 근거로 삼고있다. 그리고 정부 또한 OECD의사 수를 비교하였을 때 국내 의사 수는 부족하다고 데이터를 근거로 주장하고 있다. 이러한 갈등의 원인은 다양한 요인(고령화, 저출산 등의)을 정밀하게 두고 분석한 내용이 아니라 자신의 필요에 맞게 해석을 한 문제에서 시작되었다. 따라서 의료파업을 근본적으로 해결하는 방법은 의료정책에 대해 체계화된 데이터를 근거로 적절한 증원을 산정하는 것이다.',
                                     style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '1%','margin-top': '1%', 'fontSize': 20}),
                                     html.Div('과거 보건 의료 인력 데이터는 관리하는 기관이 수차례 바뀌어 데이터를 수집∙분류하는 기준이 다르고, 이탈하는 의사 수에 대한 집계가 명확하지 않아 보건 의료 인력의 세부적인 구조를 파악하기 어렵다. 이와 같은 문제로 향후 활동 의사 인력의 증원, 이탈되는 인력의 구체적인 수치를 추정하기 어려워 적절한 보건 의료 인력 수급 정책 마련에 어려움을 겪고 있다.',
                                     style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '1%','margin-top': '1%', 'fontSize': 20}),
                                     html.Div('즉, 의사인력의 공급정책을 결정하는 것에 있어서 증원하는 의사의 숫자만 중요한 것이 아니라 이탈되는 인력의 수, 우리나라 인구 분포 등의 다방면의 요인을 파악하고 반영하여 매해 적절한 의료 인력 수급에 맞는 정책을 세워야 한다는 것이 의료 인력 문제의 주요 골자이다.',
                                     style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '1%','margin-top': '1%', 'fontSize': 20}),
                                ]
                            )             
                        ],
                    ),
                    html.Div('[‘의사 생애 주기 모델’을 통한 현존 의사의 특성 파악 및 미래 의사 인력 예측]',style={'margin-top': '10%', 'margin-bottom':'2%','text-align': 'center', 'font-family':'Malgun Gothic', 'font-weight': 'bold', 'fontSize': 34}),
                    html.Div(
                        children=[
                            html.Img(src='https://github.com/unsik-kim/IITPMainProject/blob/master/pic2.PNG?raw=true', style={'margin-left': '3%','margin-right': '3%', 'margin-top': '1%','border-radius': '25px','width': '60%', 'height': '32%', 'float':'left'}),
                            html.Div(
                                children=[
                                    html.Div('본 연구에서는 현재 의료인력의 성별, 연령별 특성을 파악하고, 현재 의료인력의 실태를 설명하고자 한다. 그리고 의사 수 변동을 연도별로 반영하는 ‘의사 생애주기 모델’을 사용하여 미래 의사 인력 예측을 목표로 연구를 하였다.',
                                     style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '1%','margin-top': '1%', 'fontSize': 20}),
                                     html.Div('‘의사 생애 주기 모델’이란, 의사라는 직업의 시작부터 끝까지 추적하여 현존하는 의사 수를 추정하는 모델이다. 의사고시 합격부터 사망 또는 은퇴에 대한 확률모형을 통하여 매년 현직에 있는 의사 수를 추론하기 위해 사용한다.',
                                     style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '1%','margin-top': '1%', 'fontSize': 20}),
                                     html.Div('‘의사 생애 주기 모델’을 통해 정확한 현존 의사 인원을 파악하고, 증원해야 할 인원을 제시하고자 하였다. 각각의 단계에서 의료 인력의 변화를 보기 위해 매해 활동 의료 인력 수에 유입되고 유출되는 숫자를 가능하면 상세하게 추론했다.',
                                     style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '1%','margin-top': '1%', 'fontSize': 20}),
                                     html.Div('따라서, 본 연구에서는 앞에서 제시한 문제를 해결하고, 정부의 적절한 보건 의료 인력 수급 정책 마련에 도움이 되고자 ‘국내 의사 인력 추정을 위한 상세 모형 개발’을 주제로 선정하였다.',
                                     style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '1%','margin-top': '1%', 'fontSize': 20}),
                                ]
                            )                            
                        ],
                    ),
                    html.Div('[현재 의료인력 현황]',style={'margin-top': '10%', 'margin-bottom':'2%','text-align': 'center', 'font-family':'Malgun Gothic', 'font-weight': 'bold', 'fontSize': 34}),
                    html.Div(
                        children=[
                            html.Div(style={ 'text-align': 'center', 'border-radius': '15px', 'background': '#F2F2F2', 'padding': '3%', 'width': '30%', 'height': '10%', 'float':'left', 'margin-right':'3%'},
                                children=[
                                    html.H2('107928명',style={'font-family':'Malgun Gothic', 'font-weight': 'bold'}),
                                    html.P('우리나라 의사 수',style={'font-family':'Malgun Gothic', 'font-weight': 'bold'})                                
                                ]
                            ),
                            html.Div(style={'text-align': 'center', 'border-radius': '15px', 'background': '#F2F2F2', 'padding': '3%', 'width': '30%', 'height': '10%', 'float':'left', 'margin-right':'3%'},
                                children=[
                                    html.H2('2.08명',style={'font-family':'Malgun Gothic', 'font-weight': 'bold'}),
                                    html.P('우리나라 인구 1000명당 의사 수',style={'font-family':'Malgun Gothic', 'font-weight': 'bold'})
                                ]
                            ),
                            html.Div(style={'text-align': 'center', 'border-radius': '15px', 'background': '#F2F2F2', 'padding': '3%', 'width': '30%', 'height': '10%', 'float':'left', 'margin-right':'3%'},
                                children=[
                                    html.H2('3.65명', style={'font-family':'Malgun Gothic', 'font-weight': 'bold'}),
                                    html.P('OECD 회원국 인구 1000명당 의사 수', style={'font-family':'Malgun Gothic', 'font-weight': 'bold'}) 
                                ]
                            )
                        ]
                    ),
                    html.Div('Contact Us',style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-top': '20%','margin-bottom':'2%', 'font-weight': 'bold', 'fontSize': 34}),
                    html.Div(
                        children=[
                            html.Img(src='https://github.com/unsik-kim/IITPMainProject/blob/master/pic.PNG?raw=true', style={'margin-left': '5%', 'margin-top': '1%','border-radius': '25px','width': '30%', 'height': '32%', 'float':'left'}),
                            html.Div(
                                children=[
                                    html.Div('세종특별자치시 세종로 2511 고려대학교 과학기술대학 1관 HRD', style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '5%','margin-top': '5%', 'font-weight': 'bold', 'fontSize': 20}),
                                    html.Div('이대답 : 이슈에 데이터로 답하다.', style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '5%','margin-top': '1%', 'font-weight': 'bold', 'fontSize': 20}),
                                    html.Div('이예슬    email : 2exseul@iddtech.com', style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '5%','margin-top': '1%', 'font-weight': 'bold', 'fontSize': 20}),
                                    html.Div('김운식    email : fdw@iddtech.com', style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '5%','margin-top': '1%', 'font-weight': 'bold', 'fontSize': 20}),
                                    html.Div('배은형    email : kelly2111@iddtech.com', style={'text-align': 'center', 'font-family':'Malgun Gothic','margin-left': '5%','margin-top': '1%', 'font-weight': 'bold', 'fontSize': 20}),
                                ]
                            )                            
                        ],
                    ), 
                ],
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
                html.Div('[연간 은퇴 의사수]', style={'font-weight': 'bold', 'fontSize': 25}),
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
        port=50006,
        host='0.0.0.0'
    )