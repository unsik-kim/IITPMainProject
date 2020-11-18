import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header,setValue
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
                            html.Div('연도별, 성별 전체 의사수',  className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                            html.Br(),
                            html.Div(id='output-state', style={'font-weight': 'bold', 'fontSize': 20}),
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
                            html.Br([]),
                            html.Div('1) 의사수 - 본 연구를 통해 도출된 추정 연도별/성별/연령별 활동 의사수', style={'fontSize': 12}),
                            html.Br([]), html.Br([]),html.Br([]),html.Br([]),
                            html.Div('연간 전체 의사수', className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                            html.Br([]),
                            html.Div('* 범례 클릭 시 해당 데이터가 활성화됩니다.', style={'fontSize': 12}),
                            html.Br([]),
                            dcc.Graph(id='tdy-graph'),
                            html.Br([]),
                            html.Div('1) 추정 활동 의사수 - 본 연구를 통해 도출된 추정 활동 의사수', style={'fontSize': 12}),
                            html.Div('2) 실제 활동 의사수 - 건강보험공단에 신고된 요양기관에서 활동중인 의사수 / 출처-보건복지부', style={'fontSize': 12}),
                            html.Div('3) 실제 신고 의사수 - 보건복지부 면허관리시스템에 등록된 면허의사수 / 출처-보건복지부', style={'fontSize': 12}),
                            html.Br([]),
                        ]),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
 