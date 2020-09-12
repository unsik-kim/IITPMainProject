
def makeFigure():
    import pandas as pd

    #OECD 의료인력 평균
        
    data_df = pd.read_excel('.\data\OECD의사수.xlsx')
    # Variable 0:Practising physicians / 1:Professionally active physicians / 2:Physicians licensed to practice
    # Measure 0:Number of persons (head counts) / 1: Density per 1 000 population (head counts)
    # OECD 0: OECD Economies / 1: Non-OECD Economies
    print(data_df)
    meanData_df = data_df.groupby(['Variable','Measure','OECD']).mean()
    y2 = meanData_df.iloc[3]
    y2



    local_doc = pd.read_excel(".\data\local_doc_1000.xlsx")
    x_year = local_doc['year']
    y_total = local_doc['합계']
    y_seoul = local_doc['서울']
    y_pusan = local_doc['부산']
    y_daegu =local_doc['대구']
    y_Incheon =local_doc['인천']
    y_guangju = local_doc['광주']
    y_daejoen = local_doc['대전']
    y_ulsan = local_doc['울산']
    y_sejong = local_doc['세종']
    y_gyeonggi = local_doc['경기']
    y_kangwon = local_doc['강원']
    y_choungbuk = local_doc['충북']
    y_choungnam = local_doc['충남']
    y_jeonbuk = local_doc['전북']
    y_jeonnam = local_doc['전남']
    y_gyeongbuk = local_doc['경북']
    y_gyeongnam = local_doc['경남']
    y_jeju = local_doc['제주']

    import plotly.graph_objects as go

    # Create traces
    fig = go.Figure()

    yearList = list(range(2000,2020))

    fig.add_trace(go.Scatter(x=yearList, y=y2, 
                            mode='lines+markers',
                            name='OECD 평균')),

    fig.add_trace(go.Scatter(x= x_year, y=y_total,
                        mode='lines+markers',
                        name='전국'))
    fig.add_trace(go.Scatter(x= x_year, y=y_seoul,
                        mode='lines+markers',
                        name='서울'))
    fig.add_trace(go.Scatter(x= x_year, y=y_pusan,
                        mode='lines+markers',
                        name='부산'))

    fig.add_trace(go.Scatter(x= x_year, y=y_daegu,
                        mode='lines+markers',
                        name='대구'))
    fig.add_trace(go.Scatter(x= x_year, y=y_Incheon,
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