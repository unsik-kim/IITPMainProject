import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import graphpkg.testGraph as gt
import graphpkg.citySubject as gcs
import graphpkg.cityDoct as cd
import graphpkg.cityDoct2 as cd2
import graphpkg.Docincrease as gd
import graphpkg.LocalDocPerPop as gldp
import graphpkg.OECDfig as oecdfig


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


fig1 = gt.makeTestFigure()

fig2 = gt.makeTestFigure()

fig3 = gt.makeTestFigure()

fig4 = gcs.makeFigAb()

fig5 = cd.makeFigure()
fig6 = cd.makeFigure2()

fig7 = gd.makeFigure()

fig8 = gcs.makeFigRel()

fig9 = oecdfig.makeFigure()

fig10 = gldp.makeFigure()

fig11 = cd2.makeFigure()


app.layout = html.Div([
    html.H1('의료인력 데이터 분석'),

    html.H3('▶우리나라 의사 인력 분석'),
    html.H6('≫ 연도별 의료인력 증감 추이'),
    html.Div('(1) 해마다 의료인력은 3000명 가량 증가'),
    html.Div('(2) 이탈하는 의료인력 수는 해마다 불균형'),
    html.Div('(3) 이탈하는 의료 인력 수 = <(N)년 의사 수> - <(N-1)년 의사수> - <의료인력 증가수> '),
    dcc.Graph(id='graph7', figure=fig7),
    html.Div('.'),

    html.H3('▶지역별 의사 인력 분석'),

    html.H6('≫ 연도별 지역별 전문의 추이'),
    html.Div('(1) 절대적인 수치로 보았을 때 서울, 경기권에 전문의수가 편중되어 있음 '),
    dcc.Graph(id='graph6', figure=fig6),
    html.Div('.'),

    html.H6('≫ 연도별 지역별 의사수'),
    html.Div('(1) 절대적인 수치로 보았을 때 서울, 경기권에 전문의수가 편중되어 있음 '),
    dcc.Graph(id='graph5', figure=fig5),
    html.Div('.'),
    

    html.H6('≫ 우리나라 지역별 1000명당 의사수 + OECD회원국 1000명당 의사수'),
    html.Div('(1) 인구 1000명당 지역별 의사수로 상대적인 수치표현'),
    html.Div('(2) 서울의 의료인력이 가장 많고 세종의 의료인력이 가장부족함'),
    html.Div('(3) 평균보다 높은 지역 - 서울, 광주, 대전, 대구, 부산'),
    html.Div('(4) 평균에 근접한 지역 - 전북'),
    html.Div('(5) 평균보다 낮은 지역 - 강원, 제주, 인천, 전남, 경남, 경기, 충북, 울산, 충남, 경북, 세종'),
    dcc.Graph(id='graph10', figure=fig10),
    html.Div('.'),

    html.H3('▶지역별 의사 전공과목 분석'),

    html.H6('≫ 연도별 지역, 과별 의사수'),
    html.Div('(1) 2005년도에는 산부인과 외과 소아과가 상위권에 위치 했지만 현재는 가정의학과, 정형외과에 밀림'),
    dcc.Graph(id='graph4', figure=fig4),
    html.Div('.'),

    html.H6('≫ 연도별 지역, 과별 의사수, 상대적 수치'),
    html.Div('(1) 상대적인 수치로 비교해보아도 전체적인 과별 전문의 비율은 비슷함'),
    html.Div('(2) 시간이 갈수록 산부인과, 소아과 전문의 수의 순위가 떨어짐'),
    html.Div('(3) 시간이 갈수록  가정의학과 정형외과 전문의 수의 순위가 높아짐'),
    html.Div('(4) 고령화 사회로 갈 수록 고령화사회에서 수요가 낮은 과들의 의료인력은 줄어들고'),
    html.Div('    고령화사회에서 수요가 높은 과들의 의료인력은 늘어날것으로 예상됨'),
    dcc.Graph(id='graph8', figure=fig8),
    html.Div('.'),


    # html.H6('≫ 우리나라 지역별 1000명당 의사수'),
    # dcc.Graph(id='graph8', figure=fig8),

    # html.H6('≫ 우리나라 지역별 1000명당 의사수 + OECD회원국 1000명당 의사수'),
    # dcc.Graph(id='graph10', figure=fig10),


    html.H3('▶OECD 의사 증가율 회귀 분석'),
    html.H6('≫ OECD 국가별 의사 수와 추이 예측'),
    html.Div('(1) 회기분석 결과 OECD 기준 인구 1000명당 의사수는 점차 높아지고 있음'),
    html.Div('(2) 유럽권 국가들의 1000명당 의사수가 높은편이고 그 외 국가들은 낮은편'),
    html.Div('(3) OECD에 속한 국가 중 한국의 1000명당 의사수가 두번째로 낮음'),
    dcc.Graph(id='graph9', figure=fig9),
    html.Div('.'),


    html.H3('▶국내 의사 증가율 회귀 분석'),
    html.H6('≫ 국내 의사 수와 추이 예측'),
    html.Div('(1) 국내 인구 1000명당 의사 수 회기분석 결과 OECD 평균과의 격차는 좁아지고 있음'),
    html.Div('(2) 국내 인구수가 점차 줄어들면 격차는 더 줄어들 것으로 보임'),
    html.Div('(3) 이 현상을 유지했을 때 OECD 평균에 도달하기까지는 많은 시간이 필요함'),
    html.Div('(4) 현재 OECD 평균값에는 2046년에 도달 가능함'),
    dcc.Graph(id='graph11', figure=fig11),
    html.Div('.'),
])


if __name__ == '__main__':
    app.run_server(debug=False)
