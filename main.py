import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import graphpkg.testGraph as gt
import graphpkg.citiSubject as gcs
import graphpkg.cityDoct as cd
import graphpkg.Docincrease as gd
import graphpkg.LocalDocPerPop as lp

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


fig1 = gt.makeTestFigure()

fig2 = gt.makeTestFigure()

fig3 = gt.makeTestFigure()

fig4 = gcs.makeFigure()

fig5 = cd.makeFigure()
fig6 = cd.makeFigure2()

fig7 = gd.makeFigure()

fig8 = lp.makeFigure()

app.layout = html.Div([
    html.H1('의료인력 데이터 분석'),

    html.H6('≫ 연도별 지역별 의사수 추이'),
    dcc.Graph(id='graph6', figure=fig6),

    html.H6('≫ 연도별 지역별 의사수'),
    dcc.Graph(id='graph5', figure=fig5),

    html.H6('≫ 연도별 지역, 과별 의사수'),
    dcc.Graph(id='graph4', figure=fig4),

    html.H6('≫ 연도별 의료인력 증감 추이'),
    dcc.Graph(id='graph7', figure=fig7),

    html.H6('≫ 인구 1000명당 지역별 의료인력'),
    dcc.Graph(id='graph8', figure=fig8)
])


if __name__ == '__main__':
    app.run_server(debug=False)
