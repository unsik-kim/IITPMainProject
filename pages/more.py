import dash_html_components as html
from utils import Header


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 6
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div('연구목표',  className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.P(
                                                "향후 의사 수를 예측하기 위해선 현재 국내 의사 수의 구조를 구체적으로 파악해야 한다. 하지만 현재 공개된 의사 수 데이터는 연도별/성별 의사 수만 존재하여 향후 의사수를 예측하기에 어려움이 있다.",style={'font-size':"13px"}
                                            ),
                                            html.P(
                                                "[사용 데이터]를 이용하여 연도별/성별/연령별 의사 수 데이터를 추론할 수 있는 모델을 설계하고 적용하여 과거, 현재 그리고 미래의 의사인력 구조를 추론하고 분석하고자 한다.",style={'font-size':"13px"}
                                            ),
                                        ],
                                    ),
                                ],
                                className="row",
                            ),
                            html.Div(
                                [
                                    html.Div('분석 프로세스',  className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.Li("분석 프로세스 기본 개념", style={'font-size':"14px"}),
                                            html.Img(src=app.get_asset_url("분석프로세스기본개념.PNG"), style={'padding-left': "6%",'padding-right': "6%",'margin-bottom': '3%','width': '100%', 'float':'left'}),
                                            html.Br([]),
                                            html.P(
                                                "N년도 활동 의사 수(Total(n))는 N년도 신규 면허 발급 의사 수(Input(n))와 N-1년도 활동 의사의 연령을 1세 증가시킨 값(Total(n-1))을 더하고, N년도 사망/은퇴 의사 수(Loss(n))을 뺀 값이다. 이 수치를 성별/연령별로 구체화하여 매년 성별/연령별 활동 의사 수를 추론하였다." ,style={'font-size':"13px"}
                                            ),
                                            html.Br([]),
                                            html.Br([]),
                                            html.Br([]),
                                            html.Li("N년도 의사 인력 도출 프로세스", style={'font-size':"14px"}),
                                            html.Br([]),
                                            html.Img(src=app.get_asset_url("n년도의사인력도출프로세스.png"), style={'padding-left': "6%",'padding-right': "6%", 'margin-bottom': '3%','width': '100%', 'float':'left'}),
                                            html.Br([]),
                                            html.P(
                                                "Total(n)은 연도별/성별로 구분된 의사 수 데이터를 포함한다. Input(n)을 Total(n)에 합산하기 위해서는 기존의 연도별/성별 합격자 수를 분류 모델을 사용하여 연도별/성별/연령별 합격자 수로 분류해야 한다." ,style={'font-size':"13px"}
                                            ),
                                            html.P(
                                                "Loss(n) 값은 Total(n-1)을 성별/연령별 사망 모델과 성별/연령별 은퇴 모델을 사용하여 도출할 수 있다. 이 과정에서 N년도 사망 의사수와 이탈 의사수를 도출할 수 있다.",style={'font-size':"13px"}
                                            ),
                                            html.Br([]),
                                            html.Br([]),
                                            html.Li("의사고시 합격자 분류 모형 도식화", style={'font-size':"14px"}),
                                            html.Img(src=app.get_asset_url("의사고시합격자분류모형도식화.png"), style={'padding-left': "6%",'padding-right': "6%", 'margin-bottom': '3%','width': '100%', 'float':'left'}),
                                            html.P(
                                                "연도별 의사고시 합격자 수를 연도별/성별/출신별 의사고시 합격자 수 데이터로 분류하기 전에 N년도 의사고시 응시자격자의 성별/출신별 비율은 N년도 의사고시 합격자 비율과 같다고 가정하였다. N년도 의사고시 자격자 비율은 N년도 의과대학 성별 졸업자 수 및 의학전문대학원 성별 졸업자 수와 N-1 연도 의사고시 성별 응시자격자 수의 비율을 통해 추정하였다.",style={'font-size':"13px"}
                                            )
                                        ],
                                        id="reviews-bullet-pts",
                                    ),
                                ],
                                className="row",
                            ),
                            html.Div(
                                [
                                    html.Div('결론',  className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.P(
                                                "분석 결과를 통해 적정 의학대학 정원의 수는 6,000에 가까운 값이라는 것을 알 수 있다. 하지만, 이 수치는 2029년부터 감소하는 우리나라의 인구 수의 특성을 반영하여 2020년부터 일시적으로 의대 인원을 6,000명으로 증가시켜 공급될 의사 인원을 증가시켜 해결해야한다.",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                "우리나라의 의료수요(환자의 외래진료 횟수 기준)는 2018년 기준으로 OECD평균보다 4배 높은데도 불구하고, 공급(신규의사 및 1,000명당 의사 수)은 OECD평균의 60% 정도로 낮은 것을 볼 수 있다. 이는 의사의 수요와 공급의 균형이 맞지 않다고 볼 수 있으며, 의료서비스의 질을 감소 키시고 장기적으로는 기대수명 증가에 악영향을 줄 수 있다.",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                "한국개발연구원에서 발간한 <인구 대비 의사 수 증가의 경제적 편익, 이철희 외 2명>에 따르면 인구 대비 의사 수와 기대수명 간에는 양의 상관관계가 존재하며 실제로 1990년부터 2010년까지의 의사 수 변화율이 높을수록 기대수명의 증가율이 높았다고 한다. 또한 인구 1,000명당 의사 수 1명의 증가는 기대수명을 0.72년 연장하고 인구 10만명당 잠재수명 손실연수를 300년 줄여 얻을 수 있는 경제적 편익은 약 48조원으로 추정할 수 있다고 한다.",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                "이러한 결과를 바탕으로, 정부는 현재 우리 사회에 이슈가 되고 있는 공공의대와 의대정원 확대의 효과를 본 연구의 결과를 근거로 제시할 수 있다. 즉, 기존보다 구체적인 자료를 근거로 한 의료인력 시뮬레이션을 통해 의사 공급 정책 개선에 활용할 수 있다. \
                                                의사 1명이 의학 대학에 입학하여 의사면허를 따는 기간은 기본 6년으로, 의료 공급정책은 단기간에 조정하기 어렵다는 특성을 가지고 있다. \
                                                그렇기에 정부는 의사수를 증원하였을 때 잠재수명 증가로 발생하는 경제적 편익 비용 기대치와 의사 1명 증원 당 발생하는 투자비용의 적절한 손익을 계산하고 이를 통해 도출될 수 있는 데이터를 근거로 보다 세부적이고 적절한 의료인력 증원 정책을 마련할 필요가 있다.",style={'font-size':"14px"}
                                            ),
                                        ],
                                        style={"color": "#7a7a7a"},
                                    ),
                                ],
                                className="row",
                            ),
                        ],
                        className="row ",
                    )
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
