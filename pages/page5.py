import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header, setValue
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

#---app slider--
sliderMarks= {(i):{'label':str(i),'style':{'writing-mode': 'vertical-rl'}}for i in range(1955,2050,5)}
sliderMarks[1952]= {'label':'1952','style':{'writing-mode': 'vertical-rl'}}
sliderMarks[2047]= {'label':'2047','style':{'writing-mode': 'vertical-rl'}}

def create_layout(app,valueSet):
    return html.Div(
        [
            Header(app),
            setValue(valueSet),
            # page 2
            html.Div(
                [
                    html.Div(
                        children=[
                            html.Div('인구 1000명당 의사수',  className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                            html.Br(),
                            html.Div(id='output-state', style={'font-weight': 'bold', 'fontSize': 20}),
                            dcc.Graph(id='tpd-graph'),
                            html.Br([]),
                            html.Div('1) OECD평균(1960~2019) - OECD 가입 국가의 평균 "인구 1000명당 의사수" / 출처-OECD Health Statistics 2020', style={'fontSize': 12}),
                            html.Div('2) OECD평균(2020~2047) - 1) OECD평균(1960~2019) 데이터를 사용한 선형회귀 도출 값', style={'fontSize': 12}),
                            html.Div('3) 대한민국 - 본 연구를 통해 도출된 추정 연도별 1000명당 의사수', style={'fontSize': 12}),
                            html.Br([]), html.Br([]),html.Br([]),html.Br([]),
                            html.Div('의사 1명당 연간 진료수',  className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                            html.Br(),html.Br(),
                            dcc.Graph(id='dpd-graph'),
                            html.Br([]),
                            html.Div('1) OECD평균(2010~2019) - OECD 가입 국가의 평균 "인구 1명당 연간 진료수" / 출처-OECD Health Statistics 2020', style={'fontSize': 12}),
                            html.Div('2) OECD평균(2020~2047) - 1) OECD평균(2010~2019) 데이터를 사용한 선형회귀 도출 값', style={'fontSize': 12}),
                            html.Div('3) 대한민국 - 본 연구를 통해 도출된 추정 연도별 인구 1명당 연간 진료수', style={'fontSize': 12}),
                            html.Br([]),
                        ]),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
 