import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import Header

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P("의료 4대 정책과 의료 파업",style={'font-size':"2.5rem",'font-weight': 'bold'}),
                                    html.Br([]),
                                    html.P(
                                        "최근 의료 4대 정책 중 하나인 의과대학 정원 확대 및 공공 의대 설립에 대한의사협회 등 의사들이 반발하며 의료 파업이 발생하였다. 의료파업을 주장하고 실행했던 대한의사협회의 주장도 “현재 인구 감소율과 의사 증가율을 고려하면 의사 수 충분하다”라며 데이터를 근거로 삼고 있다. 그리고 정부 또한 OECD 의사 수를 비교하였을 때 국내 의사 수는 부족하다고 데이터를 근거로 주장하고 있다. 이러한 갈등의 원인은 자신의 필요에 맞게 데이터 분석을 한 문제에서 시작되었다. 따라서 의료파업을 근본적으로 해결하는 방법은 의료정책에 대해 체계화된 데이터를 근거로 적절한 증원을 산정하는 것이다. ",style={'font-size':"16px"},className="row",
                                    ),
                                    html.P(
                                        "의료파업을 주장하고 실행했던 대한의사협회의 주장도 “현재 인구 감소율과 의사 증가율을 고려하면 의사 수 충분하다”라며 데이터를 근거로 삼고 있다. 그리고 정부 또한 OECD 의사 수를 비교하였을 때 국내 의사 수는 부족하다고 데이터를 근거로 주장하고 있다.",style={'font-size':"16px"},className="row",
                                    ),
                                    html.P(
                                        "이러한 갈등의 원인은 자신의 필요에 맞게 데이터 분석을 한 문제에서 시작되었다. 따라서 의료파업을 근본적으로 해결하는 방법은 의료정책에 대해 체계화된 데이터를 근거로 적절한 증원을 산정하는 것이다. ",style={'font-size':"16px"},className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P("‘의사 생애 주기 모델’을 통한",style={'font-size':"2.5rem",'font-weight': 'bold', "color": "#222"}),
                                    html.P("현존 의사의 특성 파악 및 미래 의사 인력 예측",style={'font-size':"2.5rem",'font-weight': 'bold', "color": "#222"}),
                                    html.Br([]),
                                    html.P(
                                        "\
                                        본 연구에서는 현재 의료인력의 성별, 연령별 특성을 파악하고, 현재 의료인력의 실태를 설명하고자 한다. 그리고 의사 수 변동을 연도별로 반영하는 ‘의사 생애주기 모델’을 사용하여 미래 의사 인력 예측을 목표로 연구를 하였다.",style={'font-size':"16px", "color": "#222"},
                                        className="row",
                                    ),
                                    html.Img(src=app.get_asset_url("분석프로세스기본개념.PNG"), style={'margin-top': "3%",'margin-bottom': "3%",'width': '100%', 'float':'left'}),
                                    html.P("‘의사 생애 주기 모델’이란, 의사라는 직업의 시작부터 끝까지 추적하여 현존하는 의사 수를 추정하는 모델이다. 의사고시 합격부터 사망 또는 은퇴에 대한 확률모형을 통하여 매년 현직에 있는 의사 수를 추론하기 위해 사용한다.",style={'font-size':"16px", "color": "#222"},
                                        className="row",
                                    ),
                                    html.P("‘의사 생애 주기 모델’을 통해 정확한 현존 의사 인원을 파악하고, 증원해야 할 인원을 제시하고자 하였다. 각각의 단계에서 의료 인력의 변화를 보기 위해 매해 활동 의료 인력 수에 유입되고 유출되는 숫자를 가능하면 상세하게 추론했다.",style={'font-size':"16px", "color": "#222"},
                                        className="row",
                                    ),
                                ],
                                style={"background-color": "#f9f9f9"},
                                className="product",
                            ),
                        ],
                        className="row",
                    ),
 
            #--about us
                html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(["About us"], className="subtitle"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.Img(src=app.get_asset_url("aboutus.jpg"), style={'margin-left': '5%', 'margin-top': '5%','border-radius': '10%','width': '50%', 'float':'left'}),
                                            html.Div(
                                                [
                                                    html.P(
                                                        ["이대답"],
                                                        style={"font-size": "2.425rem", "color": "#515151", 'font-weight': 'bold', "margib-top":"5%", "margin-left":"10%", "text-align": "center"},
                                                    ),
                                                    html.P(
                                                        ['이슈에 데이터로 답하다.'],
                                                        style={'font-size':"13px",'font-weight': 'bold', "color": "#515151", "margin-left":"11%","text-align": "center"},
                                                    ),
                                                    html.P(
                                                        ["이예슬"],                                                        
                                                        style={'font-size':"14px", "color": "#515151","margin-top":"5%","margin-left":"13%", "text-align": "center"},
                                                    ),
                                                    html.P(
                                                        ["email : 2exseul@iddtech.com"],
                                                        style={"color": "#7a7a7a","margin-left":"13%","text-align": "center"},
                                                    ),
                                                    html.P(
                                                        ["김운식"],
                                                        style={'font-size':"14px", "color": "#515151","margin-top":"5%","margin-left":"13%", "text-align": "center"},
                                                    ),
                                                    html.P(
                                                        ["email : fdw@iddtech.com"],
                                                        style={"color": "#7a7a7a","margin-left":"13%","text-align": "center"},
                                                    ),
                                                    html.P(
                                                        ["배은형"],
                                                        style={'font-size':"14px", "color": "#515151","margin-top":"5%","margin-left":"13%", "text-align": "center"},
                                                    ),
                                                    html.P(
                                                        ["email : kelly2111@iddtech.com"],
                                                        style={"color": "#7a7a7a","margin-left":"13%","text-align": "center"},
                                                    ),
                                                                                
                                                ],
                                                className="five columns",
                                                style={"margin-top":"7%",'float':'left'}
                                            ),    
                                        ]
                                    ),                                    
                                    html.Div(
                                        [
                                            html.Div(
                                                [    
                                                    html.Br([]),                            
                                                    html.P(
                                                        [
                                                            "세종특별자치시 세종로 2511 고려대학교 과학기술대학 1관 HRD"
                                                        ],
                                                        style={"color": "#7a7a7a", "text-align": "center"},
                                                    ),
                                                    html.P(
                                                        [
                                                            "혁신성장 청년인재 집중양성 빅데이터 분석가 양성 과정"
                                                        ],
                                                        style={"color": "#7a7a7a", "text-align": "center"},
                                                    ),
                                                ],
                                                className="twelve columns",
                                            ),
                                        ],
                                        className="row",
                                        style={
                                            "background-color": "#f9f9f9",
                                            "padding-top": "0.5cm",
                                            "padding-bottom": "0.5cm",
                                            'justify-content':'center','align-items':'center'
                                        },
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
