import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header, make_dash_table
import pandas as pd
import pathlib
import iddModel.doctor as idoct
import numpy as np

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
dfPopulation = pd.DataFrame(np.around(idoct.npPopulation))
dfPopulation.index = range(1950, 2048)
dfPopulation


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 5
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Distributions"], className="subtitle padded"
                                    ),
                                    html.P(
                                        [
                                            "Distributions for this fund are scheduled quaterly"
                                        ],
                                        style={"color": "#7a7a7a"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.H6(
                                        ["Dividend and capital gains distributions"],
                                        className="subtitle tiny-header padded",
                                    ),
                                    html.Div(
                                        [
                                            html.Table(
                                                make_dash_table(dfNewDoctor[1]),
                                                className="tiny-header",
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Realized/unrealized gains as of 01/31/2018"],
                                        className="subtitle tiny-header padded",
                                    )
                                ],
                                className=" twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 4
                    html.Div(
                        #[
                        #    html.Div(
                        #        [html.Table(make_dash_table(df_realized))],
                        #        className="six columns",
                        #    ),
                        #    html.Div(
                        #        [html.Table(make_dash_table(df_unrealized))],
                        #        className="six columns",
                        #    ),
                        #],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
    