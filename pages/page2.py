import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

#---app slider--
sliderMarks= {(i):{'label':str(i),'style':{'writing-mode': 'vertical-rl'}}for i in range(1955,2050,5)}
sliderMarks[1952]= {'label':'1952','style':{'writing-mode': 'vertical-rl'}}
sliderMarks[2047]= {'label':'2047','style':{'writing-mode': 'vertical-rl'}}

def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 2
            html.Div(
                [
                    html.Div(
                        children=[
                            html.Div('연도별, 성별 신규 의사수',  className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                            html.Br(),
                            html.Div('<값 조절>', style={'fontSize': 13}),
                            dcc.Input(id='input-1-state', type='number', value=3000, min=0, step=100),
                            dcc.Input(id='input-2-state', type='number', value=50, min=0, step=50),
                            dcc.Input(id='input-3-state', type='number', value=0.6, step=0.1, min=0, max=1),
                            dcc.Input(id='input-4-state', type='number', value=0.6, step=0.1, min=0, max=1),
                            html.Button(id='submit-button-state', n_clicks=0, children='변경'),
                            html.Br(),
                            html.Div(id='output-state', style={'font-weight': 'bold','fontSize': 18}),
                            html.Br(),
                            html.Br(),
                            dcc.Graph(id='nd-graph'),
                            dcc.Slider(
                                id='nd-year-slider',
                                min=1952,
                                max=2047,
                                value=2018,
                                marks = sliderMarks,
                                step=1,
                                updatemode='drag'
                            ),
                            html.Br(), html.Br(),
                            html.Div('연간 신규 의사수', className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                            dcc.Graph(id='ndy-graph')
                        ]),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
 