import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import graphpkg.testGraph as gt
import graphpkg.citiSubject as gcs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


fig1 = gt.makeTestFigure()

fig2 = gt.makeTestFigure()

fig3 = gt.makeTestFigure()

fig4 = gcs.makeFigure()

app.layout = html.Div([

    html.H1('■ 현재 의료인력 분석'),
    html.H6('≫ 연도별 전체 의사수'),
    dcc.Graph(id='graph1', figure=fig1),

    html.H6('≫ 연도별 지역 의사수'),
    dcc.Graph(id='graph2', figure=fig2),

    html.H6('≫ 연도별 과별 의사수'),
    dcc.Graph(id='graph3', figure=fig3),

    html.H6('≫ 연도별 지역, 과별 의사수'),
    dcc.Graph(id='graph4', figure=fig4)
])


if __name__ == '__main__':
    app.run_server(debug=False)
