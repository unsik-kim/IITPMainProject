import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import plotly.graph_objects as go


def makeFigure():

    subject_doct = pd.read_excel(
        'data/시도별_전문과목별_전문의_현황_2005-2018_2.xlsx', thousands=',')
    subject_doct = subject_doct.fillna(0)
    subject_doct = subject_doct.replace('-', 0)

    dataList = []

    for i in subject_doct.index:
        for j in range(len(subject_doct.columns[2:])):
            subject = subject_doct.iloc[i, 0]
            year = subject_doct.iloc[i, 1]
            local = subject_doct.columns[j+2]
            value = subject_doct.iloc[i, j+2]
            if local == '계':
                continue
            if subject == '계':
                continue
            dataDict = {'과목': subject, '년도': year, '지역': local, '값': value}
            dataList.append(dataDict)

    dataDf = pd.DataFrame(dataList)

    fig = px.bar(dataDf,
                 x='값',
                 y='과목',
                 height=1000,
                 range_x=[0, 16000],
                 color='과목',
                 animation_frame='년도', animation_group='지역'
                 )

    return fig
