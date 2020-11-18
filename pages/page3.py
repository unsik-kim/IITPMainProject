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
                            html.Div('연도별, 성별 사망 의사수',  className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                            html.Br(),
                            html.Div(id='output-state', style={'font-weight': 'bold','fontSize': 18}),
                             dcc.Graph(id='dd-graph'),
                            dcc.Slider(
                                id='dd-year-slider',
                                min=1952,
                                max=2047,
                                value=2018,
                                marks = sliderMarks,
                                step=1,
                                updatemode='drag'
                            ),
                            html.Br([]),
                            html.Div('1) 사망 의사수 - 본 연구를 통해 도출된 추정 연도별/성별/연령별 사망 의사수', style={'fontSize': 12}),
                            html.Br([]), html.Br([]),html.Br([]),html.Br([]),
                            html.Div('연간 사망 의사수', className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                            html.Br(), html.Br(),
                            dcc.Graph(id='ddy-graph'),
                            html.Br([]),
                            html.Div('1) 사망 의사수 - 본 연구를 통해 도출된 추정 연도별/성별 사망 의사수', style={'fontSize': 12}),
                            html.Br([]),
                        ]),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
 