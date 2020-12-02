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
                                                " 향후 의사 수를 예측하기 위해선 현재 국내 의사 수의 구조를 구체적으로 파악해야 한다. 하지만 현재 공개된 의사 수 데이터는 연도별/성별 의사 수만 존재하여 향후 의사수를 예측하기에 어려움이 있다.",style={'font-size':"13px"}
                                            ),
                                            html.P(
                                                " [사용 데이터]를 이용하여 연도별/성별/연령별 의사 수 데이터를 추론할 수 있는 모델을 설계하고 적용하여 과거, 현재 그리고 미래의 의사인력 구조를 추론하고 분석하고자 한다.",style={'font-size':"13px"}
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
                                                " N년도 활동 의사 수(Total(n))는 N년도 신규 면허 발급 의사 수(Input(n))와 N-1년도 활동 의사의 연령을 1세 증가시킨 값(Total(n-1))을 더하고, N년도 사망/은퇴 의사 수(Loss(n))을 뺀 값이다. 이 수치를 성별/연령별로 구체화하여 매년 성별/연령별 활동 의사 수를 추론하였다." ,style={'font-size':"13px"}
                                            ),
                                            html.Br([]),
                                            html.Br([]),
                                            html.Br([]),
                                            html.Li("N년도 의사 인력 도출 프로세스", style={'font-size':"14px"}),
                                            html.Br([]),
                                            html.Img(src=app.get_asset_url("n년도의사인력도출프로세스.png"), style={'padding-left': "6%",'padding-right': "6%", 'margin-bottom': '3%','width': '100%', 'float':'left'}),
                                            html.Br([]),
                                            html.P(
                                                " Total(n)은 연도별/성별로 구분된 의사 수 데이터를 포함한다. Input(n)을 Total(n)에 합산하기 위해서는 기존의 연도별/성별 합격자 수를 분류 모델을 사용하여 연도별/성별/연령별 합격자 수로 분류해야 한다." ,style={'font-size':"13px"}
                                            ),
                                            html.P(
                                                " Loss(n) 값은 Total(n-1)을 성별/연령별 사망 모델과 성별/연령별 은퇴 모델을 사용하여 도출할 수 있다. 이 과정에서 N년도 사망 의사수와 이탈 의사수를 도출할 수 있다.",style={'font-size':"13px"}
                                            ),
                                            html.Br([]),
                                            html.Br([]),
                                            html.Li("의사고시 합격자 분류 모형 도식화", style={'font-size':"14px"}),
                                            html.Img(src=app.get_asset_url("의사고시합격자분류모형도식화.png"), style={'padding-left': "6%",'padding-right': "6%", 'margin-bottom': '3%','width': '100%', 'float':'left'}),
                                            html.P(
                                                " 연도별 의사고시 합격자 수를 연도별/성별/출신별 의사고시 합격자 수 데이터로 분류하기 전에 N년도 의사고시 응시자격자의 성별/출신별 비율은 N년도 의사고시 합격자 비율과 같다고 가정하였다. N년도 의사고시 자격자 비율은 N년도 의과대학 성별 졸업자 수 및 의학전문대학원 성별 졸업자 수와 N-1 연도 의사고시 성별 응시자격자 수의 비율을 통해 추정하였다.",style={'font-size':"13px"}
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
                                                "이번 의료인력분석을 하면서. 다음과 같은 결론을 내렸다.",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                "1. 의사 인력은 부족한 상태로, 증원이 필요하다.",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                " 정부에서 주장한 OECD 평균을 기준으로 한다면 현재의 두배인 약 6000명을 늘려야만 따라잡을 수 있다. 현재 정부의 정책대로 400명을 증원시켜도, 현상태와 비교하여 큰 폭의 변화가 없다.",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                " 우리나라는 OECD 회원국 중 의사의 수는 밑에서 두 번째이며, 인구 1명당 내원 일수는 OECD국가 중 첫 번째이다. 절대적인 의사의 숫자가 문제가 아니라 우리나라의 환자의 외래 진료 횟수는 2018년 기준으로 OECD평균보다 4배 높음에도 불구하고 의사수는 OECD 평균의 60%정도로 낮다.  ",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                " 현재는 의료 시스템의 체계가 잘 잡혀있어, 의료진들의 노동의 강도가 강하더라도 현 상태가 유지된다. 하지만 의료수요가 폭발적으로 증가하는 긴급상황이 된다면 잉여 의료 인력의 부재로, 의료 체계가 무너질 가능성이 있다. 그렇게 된다면 의료 수요를 감당하더라도 의료의 질을 확신할 수 없으며, 의사 수를 증원해야 한다.",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                "2.	미래를 위한 대비가 필요하다. ",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                " 의사 1명이 의학 대학에 입학하여 의사면허를 따는 기간은 기본 6년으로, 의료 공급정책은 단기간에 조정하기 어렵다는 특성을 가지고 있다. 그렇기에 정부는 의사수를 증원하였을 때 잠재수명 증가로 발생하는 경제적 편익 비용 기대치와 의사 1명 증원 당 발생하는 투자비용의 적절한 손익을 계산하고 이를 통해 도출될 수 있는 데이터를 근거로 보다 세부적이고 적절한 의료인력 증원 정책을 마련할 필요가 있다.",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                "3.	기존보다 구체적인 자료를 근거로 한 의료인력 시뮬레이션을 통해 의사 공급 정책 개선에 활용할 수 있다",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                " 목표에서 밝혔듯이 우리는 의사인력의 데이터를 체계적으로 구축하기 위해 정규화된 데이터 포멧을 제시했다. 이러한 방법으로 데이터를 축적해 나간다면 앞으로 의료인력의 증감 정책을 세울 때, 도움이 될 것으로 기대한다. ",style={'font-size':"14px"}
                                            ),
                                            html.P(
                                                " 이와 더불어, 다양한 시나리오를 추가하여 의료정책이 변화될 때의 경우의 수를 추가한다면 의료인력의 공급을 더 세부적으로 파악할 수 있고, 국내 인구 추세를 반영하여 앞으로의 의료인력 정책을 장기적으로 계획하고 추정하는 것에 도움이 될 것이다.",style={'font-size':"14px"}
                                            ),
                                        ],
                                    ),
                                ],
                                className="row",
                            ),
                            html.Div(
                                [
                                    html.Div('보고서 다운로드',  className="subtitle padded", style={'font-weight': 'bold','fontSize': 18}),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.P(
                                                "보고서를 통해서 더 자세한 내용을 확인하실 수 있습니다.",style={'font-size':"14px"}
                                            ),
                                            html.A("보고서 다운로드", href=app.get_asset_url("의사인력분석프로젝트.pdf")),    
                                        ],
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
