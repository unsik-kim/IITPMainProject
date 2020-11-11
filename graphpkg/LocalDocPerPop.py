import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import plotly.graph_objects as go


def makeFigure():

    # OECD 의료인력 평균
    # DB 연결
    myclient = MongoClient('218.150.247.209:2017',
                           username='unsik',
                           password='',
                           authSource='admin',
                           authMechanism='SCRAM-SHA-256')

    # DB 객체 불러오기 / DB가 없으면 생성
    newDB = myclient['FriDB']
    # 컬렉션 객체 불러오기 / 컬렉션이 없으면 생성
    newCollection = newDB['LocalDoct']
    # 국내 인구 1000명당 의사 수 데이터 정제
    LocalDoct = pd.DataFrame(newCollection.find())
    local_doc = LocalDoct[['년도', '시도', '값']]

    x_year = set(local_doc['년도'])
    x_year = list(x_year)
    x_year.sort()

    y_total = local_doc[local_doc['시도'] == '합계']
    y_total = y_total['값']
    y_seoul = local_doc[local_doc['시도'] == '서울']
    y_seoul = y_seoul['값']
    y_pusan = local_doc[local_doc['시도'] == '부산']
    y_pusan = y_pusan['값']
    y_daegu = local_doc[local_doc['시도'] == '대구']
    y_daegu = y_daegu['값']
    y_Incheon = local_doc[local_doc['시도'] == '인천']
    y_Incheon = y_Incheon['값']
    y_guangju = local_doc[local_doc['시도'] == '광주']
    y_guangju = y_guangju['값']
    y_daejoen = local_doc[local_doc['시도'] == '대전']
    y_daejoen = y_daejoen['값']
    y_ulsan = local_doc[local_doc['시도'] == '울산']
    y_ulsan = y_ulsan['값']
    y_sejong = local_doc[local_doc['시도'] == '세종']
    y_sejong = y_sejong['값']
    y_gyeonggi = local_doc[local_doc['시도'] == '경기']
    y_gyeonggi = y_gyeonggi['값']
    y_kangwon = local_doc[local_doc['시도'] == '강원']
    y_kangwon = y_kangwon['값']
    y_choungbuk = local_doc[local_doc['시도'] == '충북']
    y_choungbuk = y_choungbuk['값']
    y_choungnam = local_doc[local_doc['시도'] == '충남']
    y_choungnam = y_choungnam['값']
    y_jeonbuk = local_doc[local_doc['시도'] == '전북']
    y_jeonbuk = y_jeonbuk['값']
    y_jeonnam = local_doc[local_doc['시도'] == '전남']
    y_jeonnam = y_jeonnam['값']
    y_gyeongbuk = local_doc[local_doc['시도'] == '경북']
    y_gyeongbuk = y_gyeongbuk['값']
    y_gyeongnam = local_doc[local_doc['시도'] == '경남']
    y_gyeongnam = y_gyeongnam['값']
    y_jeju = local_doc[local_doc['시도'] == '제주']
    y_jeju = y_jeju['값']

    # OECD회원국의 인구 1000명당 의사 수 데이터 정제
    newCollection2 = newDB['OecdDoc']
    oecd_doc = pd.DataFrame(newCollection2.find(
        {'구분': '1000명당 의사수'}, {'_id': 0}))
    oecd_doc = oecd_doc.groupby(['년도']).mean()

    value = oecd_doc['값']

    year = oecd_doc.index
    year = np.array(year)
    year = year.reshape(-1, 1)
    year = year.flatten().tolist()

    # Create traces
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=year, y=value,
                             mode='lines+markers',
                             name='OECD 평균')),

    fig.add_trace(go.Scatter(x=x_year, y=y_total,
                             mode='lines+markers',
                             name='전국'))
    fig.add_trace(go.Scatter(x=x_year, y=y_seoul,
                             mode='lines+markers',
                             name='서울'))
    fig.add_trace(go.Scatter(x=x_year, y=y_pusan,
                             mode='lines+markers',
                             name='부산'))
    fig.add_trace(go.Scatter(x=x_year, y=y_daegu,
                             mode='lines+markers',
                             name='대구'))
    fig.add_trace(go.Scatter(x=x_year, y=y_Incheon,
                             mode='lines+markers',
                             name='인천'))
    fig.add_trace(go.Scatter(x=x_year, y=y_guangju,
                             mode='lines+markers',
                             name='광주'))

    fig.add_trace(go.Scatter(x=x_year, y=y_daejoen,
                             mode='lines+markers',
                             name='대전'))
    fig.add_trace(go.Scatter(x=x_year, y=y_ulsan,
                             mode='lines+markers',
                             name='울산'))
    fig.add_trace(go.Scatter(x=x_year, y=y_sejong,
                             mode='lines+markers',
                             name='세종'))

    fig.add_trace(go.Scatter(x=x_year, y=y_gyeonggi,
                             mode='lines+markers',
                             name='경기'))
    fig.add_trace(go.Scatter(x=x_year, y=y_kangwon,
                             mode='lines+markers',
                             name='강원'))
    fig.add_trace(go.Scatter(x=x_year, y=y_choungbuk,
                             mode='lines+markers',
                             name='충북'))

    fig.add_trace(go.Scatter(x=x_year, y=y_choungnam,
                             mode='lines+markers',
                             name='충남'))
    fig.add_trace(go.Scatter(x=x_year, y=y_jeonbuk,
                             mode='lines+markers',
                             name='전북'))
    fig.add_trace(go.Scatter(x=x_year, y=y_jeonnam,
                             mode='lines+markers',
                             name='전남'))

    fig.add_trace(go.Scatter(x=x_year, y=y_gyeongbuk,
                             mode='lines+markers',
                             name='경북'))
    fig.add_trace(go.Scatter(x=x_year, y=y_gyeongnam,
                             mode='lines+markers',
                             name='경남'))
    fig.add_trace(go.Scatter(x=x_year, y=y_jeju,
                             mode='lines+markers',
                             name='제주'))
    fig.update_layout(
        title_text="1000명당 의료 인력", height=650
    )

    return fig
