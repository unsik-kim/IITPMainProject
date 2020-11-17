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
                    ],href="/idd-doctor-report/main"),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("의료인력 동태 분석 및 예측", style={'font-weight': 'bold'})],
                        className="seven columns main-title"
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/idd-doctor-report/full-view",
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
                href="/idd-doctor-report/main",
                className="tab first",
            ),
            dcc.Link(
                "1. 전체 의사 수",
                href="/idd-doctor-report/page1",
                className="tab",
            ),
            dcc.Link(
                "2. 신규 의사 수",
                href="/idd-doctor-report/page2",
                className="tab",
            ),
            dcc.Link(
                "3. 사망 의사 수", href="/idd-doctor-report/page3", className="tab"
            ),
            dcc.Link(
                "4. 은퇴 의사 수",
                href="/idd-doctor-report/page4",
                className="tab",
            ),
            dcc.Link(
                "5. 1000명당 의사 수",
                href="/idd-doctor-report/page5",
                className="tab",
            ),
            dcc.Link(
                "More",
                href="/idd-doctor-report/more",
                className="tab",
            ), 
            dcc.Link(
                "Data",
                href="/idd-doctor-report/data",
                className="tab",
            ),           
        ],
        className="row all-tabs",
    )
    return menu

def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

