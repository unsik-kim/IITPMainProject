import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header, make_dash_table, setValue
import pandas as pd
import pathlib
import iddModel.doctor as idoct
import numpy as np



dfUseDataTable = pd.DataFrame([
    ['연도별 의사 국가시험 응시현황',
    '연도별 정기 면허신고 의사 수',
    '연도별 건강보험공단 신고 요양기관 활동 의사 수',
    '연도별 의학대학, 의학전문대학원 현황',
    '연도별 사망률 추계1',
    '연도별 사망률 추계2',
    '연도별 총 인구추계',
    '연도별 군의관 입영정보',
    '활동의사 연령분포표'],
    ['기준연도, 응시자수, 합격자수',
    '연도별, 성별 의사 수',
    '연도별 의사 수',
    '입학자수, 졸업자수, 재학생수',
    '연도별, 성별, 연령별(1세) 사망률',
    '연도별, 성별, 연령별(5세) 사망률',
    '연도별 총 인구수',
    '연도별 군의관 임관 수',
    '연도별, 성별, 연령별(10세) 의사 수'],
    ['한국보건의료인 국가시험원',
    '보건복지부 통계연감',
    '건강보험공단 심사평가원',
    '교육부 통계연감',
    '통계청',
    'United Nations',
    '통계청',
    '병무청 통계연감',
    '보건복지부 보건의료인력 실태조사'],
    ['1952년~ 2020년',
    '1955년~2019년',
    '2003년~2020년',
    '1977년~2019년',
    '1970년~2047년',
    '1950년~1970년',
    '1950년~2047년',
    '1998년~2019년',
    '2011년~2016년']]).T

dfUseDataTable.index = list(range(1,10))
dfUseDataTable.columns = ['데이터 명','데이터 항목','출처','비고']

def create_layout(app,valueSet):
    return html.Div(
        [
            Header(app),
            # page 5
            html.Div(
                [
                    # 사용 데이터
                    html.Div(
                        [
                            html.Div('사용 데이터',  className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                            html.Div(
                                [
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.Table(
                                                make_dash_table(dfUseDataTable),
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
                    

                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
    