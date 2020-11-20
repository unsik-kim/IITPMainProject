import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots


# 연도별, 성별 사망의사수 그래프
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
    trace3 = go.Bar(x=dead.age, y=dead.Man, name='남성',text=dead.Man,textposition='outside')
    trace4 = go.Bar(x=dead.age, y=dead.Woman, name='여성',text=dead.Woman,textposition='outside')

    data = [trace3, trace4]
    layout = go.Layout(title=year+'년 연령별 성별 사망 의사수')
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
       # height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0),
        showlegend=True,
        yaxis=dict(range=[0,30])
       
    )

    fig.update_yaxes(title_text="사망 의사수")
    fig.update_xaxes(title_text="연령") 

    return fig

# 연도별, 성별 신규의사수
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
    trace3 = go.Bar(x=new.age, y=new.Man, name='남성',text=new.Man,textposition='outside')
    trace4 = go.Bar(x=new.age, y=new.Woman, name='여성',text=new.Woman,textposition='outside')

    data = [trace3, trace4]
    layout = go.Layout(title=year+'년 연령별 성별 신규 의사수')
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
       # height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0),
        showlegend=True,
        yaxis=dict(range=[0,2000]) 
    )

    fig.update_yaxes(title_text="신규 의사수")
    fig.update_xaxes(title_text="연령") 
    return fig

# 연도별, 성별 은퇴의사수
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
    trace3 = go.Bar(x=retire.age, y=retire.Man, name='남성',text=retire.Man,textposition='outside')
    trace4 = go.Bar(x=retire.age, y=retire.Woman, name='여성',text=retire.Woman,textposition='outside')

    data = [trace3, trace4]
    layout = go.Layout(title=year+'년 연령별 성별 은퇴 의사수')
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
       # height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0),
        showlegend=True,
        yaxis=dict(range=[0,120])
       
    )
    fig.update_yaxes(title_text="은퇴 의사수")
    fig.update_xaxes(title_text="연령") 
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

# 연도별, 성별 전체의사수 그래프
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
    
    trace3 = go.Bar(name='남성', x=list(docManYear['age']), y=list(docManYear[yearValue]))
    trace4 = go.Bar(name = '여성', x=list(womOfYear['age']), y=list(womOfYear[yearValue]))

    data = [trace3, trace4]
    layout = go.Layout(title=str(year)+'년 연령별 의사수')
    fig = go.Figure(data=data, layout=layout)
    fig.update_traces(text=text, textposition='outside')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0),
        showlegend=True,
        yaxis=dict(range=[0,3000])
    )

    fig.update_yaxes(title_text="의사수")
    fig.update_xaxes(title_text="연령")

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
    OECDPer1000.columns = ['Division', 'Country', 'Year', 'Value']
    OECDPer1000Mean = OECDPer1000.groupby(['Division','Year']).mean()
    OECDPer1000Mean = OECDPer1000Mean.iloc[0:60,:]
    OECDPer1000Mean = OECDPer1000Mean.reset_index()
    year=list(OECDPer1000Mean['Year'])
    OECDValue = list(OECDPer1000Mean['Value'])
    mask = (OECDPer1000.Year > 2019) & (OECDPer1000.Division == '1000명당 의사수')
    OECDPer1000Regression = OECDPer1000.loc[mask, :]
    OECDPer1000Regression = OECDPer1000Regression[['Division','Year','Value']]
    OECDPer1000RegressionYear = list(OECDPer1000Regression['Year'])
    OECDPer1000RegressionValue = list(OECDPer1000Regression['Value'])
    year = year+OECDPer1000RegressionYear
    OECDValue = np.around(np.array(OECDValue+OECDPer1000RegressionValue),2)

    return OECDValue


# 1000명당 국내 의사수 그래프
def makeFigureDocPer1000(dfThousandPerDoctor):
    fig = go.Figure()

    docPer1000 = thousandDocGet(dfThousandPerDoctor)
    docPerThousend = list(docPer1000['docnum'])  # 1000명당 국내 의사 수 
    OECDPerData = OECDDocGet()

    fig.add_trace(go.Scatter(x=np.array(range(1950,2048)), y=docPerThousend,
                        mode='lines',
                        name='대한민국'))
    fig.add_trace(go.Scatter(x=np.array(range(1960,2048)), y=OECDPerData,
                        mode='lines',
                        name='OECD평균'))

    fig.update_layout(margin=dict(l=0,r=0,t=1,b=0),    
        showlegend=True,
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    fig.update_yaxes(title_text="인구 1000명당 의사수")
    fig.update_xaxes(title_text="연도")                    

    return fig

# 의사 1명당 연간 외래진료수 그래프
def makeFigureVisitDoctor(npVisitData):
    npVisitData = np.around(npVisitData,2)
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=np.array(range(2010,2048)), y=npVisitData[0],
                        mode='lines',
                        name='대한민국'))
    fig.add_trace(go.Scatter(x=np.array(range(2010,2048)), y=npVisitData[1],
                        mode='lines',
                        name='OECD평균'))

    fig.update_layout(margin=dict(l=0,r=0,t=1,b=0),    
        showlegend=True,
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    fig.update_yaxes(title_text="의사 1명당 연간 외래진료 수")
    fig.update_xaxes(title_text="연도")                    

    return fig

# 연간 전체 의사수
def makeFigureSumDoc(dfResultPerson,dfPopulation,npRealDoctor, npRealWorkDoctor):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    year = list(range(1950, 2048))
    docData =getDataframe(dfResultPerson)
    manSumDoc = list(docData[0].sum(axis=1))
    womSumDoc = list(docData[1].sum(axis=1))
    bothSumDoc = list(docData[2].sum(axis=1))
    popDoc = list(np.array(dfPopulation.T)[0])
    
    fig.add_trace(go.Scatter(x=year, y=manSumDoc,
                        mode='lines',
                        name='A-추정 남성 활동 의사수'), secondary_y=False)
    fig.add_trace(go.Scatter(x=year, y=womSumDoc,
                        mode='lines',
                        name='A-추정 여성 활동 의사수'), secondary_y=False)
    fig.add_trace(go.Scatter(x=year, y=bothSumDoc,
                        mode='lines',
                        name='A-추청 전체 활동 의사수'), secondary_y=False)

    fig.add_trace(go.Scatter(x=list(range(2003, 2021)), y=npRealWorkDoctor[53:71],
                        mode='lines', visible='legendonly',
                        name='A-실제 활동 의사수'), secondary_y=False)    

    fig.add_trace(go.Scatter(x=list(range(1955, 2018)), y=npRealDoctor[1][5:79],
                        mode='lines', visible='legendonly',
                        name='A-실제 남성 신고 의사수'), secondary_y=False)
    fig.add_trace(go.Scatter(x=list(range(1955, 2018)), y=npRealDoctor[2][5:79],
                        mode='lines', visible='legendonly',
                        name='A-실제 여성 신고 의사수'), secondary_y=False)
    fig.add_trace(go.Scatter(x=list(range(1955, 2018)), y=npRealDoctor[0][5:79],
                        mode='lines', visible='legendonly',
                        name='A-실제 전체 신고 의사수'), secondary_y=False)     

    fig.add_trace(go.Scatter(x=list(range(1950, 2047)), y=popDoc,
                        mode='lines',
                        name='B-인구수'), secondary_y=True)
    fig.update_layout(margin=dict(l=0,r=0,t=1,b=0),    
        showlegend=True,
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    # Set y-axes titles
    fig.update_yaxes(title_text="A-의사수", secondary_y=False)
    fig.update_yaxes(title_text="B-인구수", secondary_y=True)
    fig.update_xaxes(title_text="연도")  
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
                        name='남성'))
    fig.add_trace(go.Scatter(x=year, y=womSumDoc,
                        mode='lines',
                        name='여성'))
    fig.add_trace(go.Scatter(x=year, y=bothSumDoc,
                        mode='lines',
                        name='전체'))
    fig.update_layout(margin=dict(l=0,r=0,t=1,b=0),    
        showlegend=True,
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    fig.update_yaxes(title_text="은퇴 의사수")
    fig.update_xaxes(title_text="연도")  
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
                        name='남성'))
    fig.add_trace(go.Scatter(x=year, y=womSumDoc,
                        mode='lines',
                        name='여성'))
    fig.add_trace(go.Scatter(x=year, y=bothSumDoc,
                        mode='lines',
                        name='전체'))
    fig.update_layout(margin=dict(l=0,r=0,t=1,b=0),    
        showlegend=True,
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))                    

    fig.update_yaxes(title_text="사망 의사수")
    fig.update_xaxes(title_text="연도")  
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
                        name='남성'))
    fig.add_trace(go.Scatter(x=year, y=womSumDoc,
                        mode='lines',
                        name='여성'))
    fig.add_trace(go.Scatter(x=year, y=bothSumDoc,
                        mode='lines',
                        name='전체'))
    fig.update_layout(margin=dict(l=0,r=0,t=1,b=0),    
        showlegend=True,
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    fig.update_yaxes(title_text="신규 의사수")
    fig.update_xaxes(title_text="연도")  
    return fig