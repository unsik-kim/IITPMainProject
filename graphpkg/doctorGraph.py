import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def makeDDFigure(dfDeadDoctor,year):
    year = str(year)

    exdfDeadPerson0 = dfDeadDoctor[0].iloc[:,26:]
    exdfDeadPerson0['성별']='Man'
    exdfDeadPerson1 = dfDeadDoctor[1].iloc[:,26:]
    exdfDeadPerson1['성별']='Woman'
    exdfDeadPerson = pd.concat([exdfDeadPerson0,exdfDeadPerson1])
    exdfDeadPerson = exdfDeadPerson.reset_index().rename(columns={"index": "연도"}).set_index('성별')

    deadPersonDict = {}

    for i in range(1952,2048):
        data = exdfDeadPerson[exdfDeadPerson['연도']==i]
        data.drop(['연도'], axis='columns', inplace=True)
        data = data.rename_axis(None).T
        data = data.reset_index().rename(columns={'index':'age'})
        deadPersonDict.setdefault(str(i), data)
    
    dead = deadPersonDict[year]
    trace3 = go.Bar(x=dead.age, y=dead.Man, name='남자',text=dead.Man,textposition='outside')
    trace4 = go.Bar(x=dead.age, y=dead.Woman, name='여자',text=dead.Woman,textposition='outside')

    data = [trace3, trace4]
    layout = go.Layout(title=year+'년 연령별 성별 사망 의사 수')
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
       # height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0),
        showlegend=True,
        yaxis=dict(range=[0,30])
       
    )
    return fig

def makeNDFigure(dfNewDoctor,year):
    year = str(year)

    exdfNewPerson0 = dfNewDoctor[0].iloc[:,26:40]
    exdfNewPerson0['성별']='Man'
    exdfNewPerson1 = dfNewDoctor[1].iloc[:,26:40]
    exdfNewPerson1['성별']='Woman'
    exdfNewPerson = pd.concat([exdfNewPerson0,exdfNewPerson1])
    exdfNewPerson = exdfNewPerson.reset_index().rename(columns={"index": "연도"}).set_index('성별')

    newPersonDict = {}

    for i in range(1952,2048):
        data = exdfNewPerson[exdfNewPerson['연도']==i]
        data.drop(['연도'], axis='columns', inplace=True)
        data = data.rename_axis(None).T
        data = data.reset_index().rename(columns={'index':'age'})
        newPersonDict.setdefault(str(i), data)
    
    new = newPersonDict[year]
    trace3 = go.Bar(x=new.age, y=new.Man, name='남자',text=new.Man,textposition='outside')
    trace4 = go.Bar(x=new.age, y=new.Woman, name='여자',text=new.Woman,textposition='outside')

    data = [trace3, trace4]
    layout = go.Layout(title=year+'년 연령별 성별 신규 의사 수')
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
       # height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0),
        showlegend=True,
        yaxis=dict(range=[0,2000]) 
    )
    return fig

def makeRDFigure(dfRetireDoctor,year):
    year = str(year)

    exdfRetirePerson0 = dfRetireDoctor[0].iloc[:,45:95]
    exdfRetirePerson0['성별']='Man'
    exdfRetirePerson1 = dfRetireDoctor[1].iloc[:,45:95]
    exdfRetirePerson1['성별']='Woman'
    exdfRetirePerson = pd.concat([exdfRetirePerson0,exdfRetirePerson1])
    exdfRetirePerson = exdfRetirePerson.reset_index().rename(columns={"index": "연도"}).set_index('성별')

    retirePersonDict = {}

    for i in range(1952,2048):
        data = exdfRetirePerson[exdfRetirePerson['연도']==i]
        data.drop(['연도'], axis='columns', inplace=True)
        data = data.rename_axis(None).T
        data = data.reset_index().rename(columns={'index':'age'})
        retirePersonDict.setdefault(str(i), data)
    
    retire = retirePersonDict[year]
    trace3 = go.Bar(x=retire.age, y=retire.Man, name='남자',text=retire.Man,textposition='outside')
    trace4 = go.Bar(x=retire.age, y=retire.Woman, name='여자',text=retire.Woman,textposition='outside')

    data = [trace3, trace4]
    layout = go.Layout(title=year+'년 연령별 성별 은퇴 의사 수')
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
       # height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0),
        showlegend=True,
        yaxis=dict(range=[0,150])
       
    )
    return fig

def getDataframe(dfResultPerson):
    #남성 의사 인력 DataFrame, 변수명 manDoc
    manDoc = dfResultPerson[0].iloc[:,20:90]
    index = list(range(1950,2048))
    manDoc = manDoc.set_index([index])
    
    #여성 의사 인력 DataFrame, 변수명 womDoc
    womDoc = dfResultPerson[1].iloc[:,20:90]
    index = list(range(1950,2048))
    womDoc = womDoc.set_index([index])

    #남여 의사 인력 DataFrame, 변수명 bothDoc
    bothDoc = dfResultPerson[2]
    index = list(range(1950,2048))
    bothDoc = bothDoc.set_index([index])
    return [manDoc, womDoc, bothDoc]

def slicingPerson(dfResultPerson, year):
    value = []
    bothDoc =getDataframe(dfResultPerson)
    value.append(bothDoc[0].iloc[year])
    value.append(bothDoc[1].iloc[year])
    return value

def makeANDFigure(dfResultPerson, year):
    yearValue = int(year)
    yearIndex = yearValue-1950

    womOfYear = pd.DataFrame(slicingPerson(dfResultPerson, yearIndex)[1])
    womOfYear = womOfYear.rename_axis('age').reset_index()
    numOfWom = womOfYear[yearValue].tolist()

    docManYear = pd.DataFrame(slicingPerson(dfResultPerson, yearIndex)[0])
    docManYear = docManYear.rename_axis('age').reset_index()
    numOfMan = docManYear[yearValue].tolist()
    text = docManYear[yearValue]
    
    trace3 = go.Bar(name='Man', x=list(docManYear['age']), y=list(docManYear[yearValue]))
    trace4 = go.Bar(name = 'Woman', x=list(womOfYear['age']), y=list(womOfYear[yearValue]))

    data = [trace3, trace4]
    layout = go.Layout(title=str(year)+'년 연령별 의사 수')
    fig = go.Figure(data=data, layout=layout)
    fig.update_traces(text=text, textposition='outside')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0),
        showlegend=True,
        yaxis=dict(range=[0,3000])
    )

    return fig

def thousandDocGet(dfThousandPerDoctor):
    docPer1000 = dfThousandPerDoctor
    docPer1000 = docPer1000.dropna(axis = 0, how = 'any')
    #index 변경
    index = list(range(1950,2048))
    docPer1000 = docPer1000.set_index([index])
    docPer1000.columns = ['docnum']
    return docPer1000

def OECDDocGet():
    OECDPer1000 = pd.read_excel('data/OECD의사수.xlsx')
    OECDPer1000 = OECDPer1000.groupby(['구분','년도']).mean()
    OECDPer1000 = OECDPer1000.iloc[0:60,:]
    OECDPer1000 = OECDPer1000.reset_index()
    return OECDPer1000

def makeFigureDocPer1000(dfThousandPerDoctor):
    fig = go.Figure()
    docPer1000 = thousandDocGet(dfThousandPerDoctor)
    years = list(docPer1000.index)  #연도
    docPerThousend = list(docPer1000['docnum'])  # 1000명당 국내 의사 수 
    OECDPer1000 = OECDDocGet()
    year=list(OECDPer1000['년도'])
    OECDValue = list(OECDPer1000['값'])
    
    fig.add_trace(go.Scatter(x=years, y=docPerThousend,
                        mode='lines',
                        name='KOREA'))
    fig.add_trace(go.Scatter(x=year, y=OECDValue,
                        mode='lines',
                        name='OECD'))

    return fig

# 연간 전체 의사수
def makeFigureSumDoc(dfResultPerson):
    fig = go.Figure()
    
    year = list(range(1950, 2048))
    docData =getDataframe(dfResultPerson)
    manSumDoc = list(docData[0].sum(axis=1))
    womSumDoc = list(docData[1].sum(axis=1))
    bothSumDoc = list(docData[2].sum(axis=1))
    
    fig.add_trace(go.Scatter(x=year, y=manSumDoc,
                        mode='lines',
                        name='MAN'))
    fig.add_trace(go.Scatter(x=year, y=womSumDoc,
                        mode='lines',
                        name='WOMAN'))
    fig.add_trace(go.Scatter(x=year, y=bothSumDoc,
                        mode='lines',
                        name='BOTH'))
    fig.update_layout(
        margin=dict(l=0,t=0.5,r=0),
        showlegend=True)
    return fig

# 연간 은퇴 의사수
def getDataframe2(dfRetirePerson):
    #남성 의사 인력 DataFrame, 변수명 manDoc
    manDoc = dfRetirePerson[0]
    index = list(range(1950,2048))
    manDoc = manDoc.set_index([index])

    #여성 의사 인력 DataFrame, 변수명 womDoc
    womDoc = dfRetirePerson[1]
    index = list(range(1950,2048))
    womDoc = womDoc.set_index([index])

    bothdoc = dfRetirePerson[2]
    index = list(range(1950,2048))
    bothdoc = bothdoc.set_index([index])
    return [manDoc, womDoc, bothdoc]

def makeFigureRetireDoc(dfRetirePerson):
    fig = go.Figure()
    
    year = list(range(1950, 2048))
    docData =getDataframe2(dfRetirePerson)
    manSumDoc = list(docData[0].sum(axis=1))
    womSumDoc = list(docData[1].sum(axis=1))
    bothSumDoc = list(docData[2].sum(axis=1))
    
    fig.add_trace(go.Scatter(x=year, y=manSumDoc,
                        mode='lines',
                        name='MAN'))
    fig.add_trace(go.Scatter(x=year, y=womSumDoc,
                        mode='lines',
                        name='WOMAN'))
    fig.add_trace(go.Scatter(x=year, y=bothSumDoc,
                        mode='lines',
                        name='BOTH'))

    return fig

# 연간 사망 의사수
def getDataframe3(dfDeadPerson):
    #남성 의사 인력 DataFrame, 변수명 manDoc
    manDoc = dfDeadPerson[0]
    index = list(range(1950,2048))
    manDoc = manDoc.set_index([index])
    
    #여성 의사 인력 DataFrame, 변수명 womDoc
    womDoc = dfDeadPerson[1]
    index = list(range(1950,2048))
    womDoc = womDoc.set_index([index])
    
    bothdoc = dfDeadPerson[2]
    index = list(range(1950,2048))
    bothdoc = bothdoc.set_index([index])
    return [manDoc, womDoc, bothdoc]

def makeFigureDeadDoc(dfDeadPerson):
    fig = go.Figure()
    
    year = list(range(1950, 2048))
    docData =getDataframe3(dfDeadPerson)
    manSumDoc = list(docData[0].sum(axis=1))
    womSumDoc = list(docData[1].sum(axis=1))
    bothSumDoc = list(docData[2].sum(axis=1))
    
    fig.add_trace(go.Scatter(x=year, y=manSumDoc,
                        mode='lines',
                        name='MAN'))
    fig.add_trace(go.Scatter(x=year, y=womSumDoc,
                        mode='lines',
                        name='WOMAN'))
    fig.add_trace(go.Scatter(x=year, y=bothSumDoc,
                        mode='lines',
                        name='BOTH'))

    return fig

# 연간 신규 의사수
def getDataframe4(dfNewPerson):
    #남성 의사 인력 DataFrame, 변수명 manDoc
    manDoc = dfNewPerson[0]
    index = list(range(1950,2048))
    manDoc = manDoc.set_index([index])
    
    #여성 의사 인력 DataFrame, 변수명 womDoc
    womDoc = dfNewPerson[1]
    index = list(range(1950,2048))
    womDoc = womDoc.set_index([index])
    
    bothdoc = dfNewPerson[2]
    index = list(range(1950,2048))
    bothdoc = bothdoc.set_index([index])
    return [manDoc, womDoc, bothdoc]

def makeFigureNewDoc(dfNewPerson):
    fig = go.Figure()
    
    year = list(range(1950, 2048))
    docData =getDataframe4(dfNewPerson)
    manSumDoc = list(docData[0].sum(axis=1))
    womSumDoc = list(docData[1].sum(axis=1))
    bothSumDoc = list(docData[2].sum(axis=1))
    
    fig.add_trace(go.Scatter(x=year, y=manSumDoc,
                        mode='lines',
                        name='MAN'))
    fig.add_trace(go.Scatter(x=year, y=womSumDoc,
                        mode='lines',
                        name='WOMAN'))
    fig.add_trace(go.Scatter(x=year, y=bothSumDoc,
                        mode='lines',
                        name='BOTH'))

    return fig