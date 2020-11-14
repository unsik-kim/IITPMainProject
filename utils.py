import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A([
                        html.Img(
                            src="https://github.com/unsik-kim/IITPMainProject/blob/master/%EB%A1%9C%EA%B3%A0%20%ED%9A%8C%EC%8B%9D%20%EB%B0%94%ED%83%95.png?raw=true",
                            style={"width": "110px", "height": "70px","margin-top": "10px", "margin-left": "10px", "margin-right": "10px", "margin-bottom": "10px"}
                        )
                    ],href="/dash-financial-report/main"),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("의료인력 동태 분석 및 예측")],
                        className="seven columns main-title"
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/dash-financial-report/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Main",
                href="/dash-financial-report/main",
                className="tab first",
            ),
            dcc.Link(
                "1. 전체 의사 수",
                href="/dash-financial-report/price-performance",
                className="tab",
            ),
            dcc.Link(
                "2. 신규 의사 수",
                href="/dash-financial-report/portfolio-management",
                className="tab",
            ),
            dcc.Link(
                "3. 사망 의사 수", href="/dash-financial-report/fees", className="tab"
            ),
            dcc.Link(
                "4. 은퇴 의사 수",
                href="/dash-financial-report/distributions",
                className="tab",
            ),
            dcc.Link(
                "5. 1000명당 의사 수",
                href="/dash-financial-report/news-and-reviews",
                className="tab",
            ),
            dcc.Link(
                "More",
                href="/dash-financial-report/more",
                className="tab",
            ),            
        ],
        className="row all-tabs",
    )
    return menu


