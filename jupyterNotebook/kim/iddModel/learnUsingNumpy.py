import pandas as pd
import numpy as np
import math

# 1950~2067년
dfDeathWoman = pd.read_excel('iddModel/data/여성사망률추이.xlsx').set_index(['year']).iloc[:98,:100]
dfDeathMan = pd.read_excel('iddModel/data/남성사망률추이.xlsx').set_index(['year']).iloc[:98,:100]
npDeathWoman = np.array(dfDeathWoman)
npDeathMan = np.array(dfDeathMan)

# 1950~2047년
dfDoctorData = pd.read_excel('iddModel/data/doctorData.xlsx').set_index(['년도']).iloc[:98,:]
npPassDoctor = np.around(np.array(dfDoctorData[['의대졸합격/남', '의대졸합격/여', '의전졸합격/남', '의전졸합격/여', '불합합격/남', '불합합격/여']]))
npDoctorExam = np.around(np.array(dfDoctorData[['의사고시 합격자수','의사고시 불합격자수']]))
npPopulation = np.array(dfDoctorData['추계인구'])
npPassDoctorRate = np.array(dfDoctorData[['의대졸비율/남', '의대졸비율/여', '의전졸비율/남', '의전졸비율/여', '불합비율/남', '불합비율/여']])

# 2011~2016년 의사 연령 분포
dfDoctorAgeData = pd.read_excel('iddModel/data/의사연령별분포.xlsx')
npDoctorAgeData = np.array(dfDoctorAgeData)[:,2:]

# 1951년 의사수
dfFirstDoctor = pd.read_excel('iddModel/data/firstDoctor.xlsx')
npFirstDoctor = np.array(dfFirstDoctor)[:,1:-1]

# 1950~2020년 연령분포
dfKoreaAgePopRateData = pd.read_excel('iddModel/data/koreaAgePopRateData.xlsx')
npKoreaAgePopRateDataMan = np.array(dfKoreaAgePopRateData[dfKoreaAgePopRateData['sex']=='MALE'])[:,2:]
npKoreaAgePopRateDataWoman = np.array(dfKoreaAgePopRateData[dfKoreaAgePopRateData['sex']=='FEMALE'])[:,2:]

def makeLogModel3(tunSet):
    npData = np.zeros(100)
    start = tunSet[0]
    end = tunSet[1]
    head = tunSet[2]
    height = tunSet[3]

    for i in range(start,end+1):
        if i>head:
            a1 = height**(1/(-1*(end-head)))
            gx = ((a1**(2*(i-end)))/10)
            npData[i] = gx
        elif i<=head:
            a2 = height**(1/(head-0))
            fx = ((a2**(2*(i-0)))/100)
            npData[i] = fx

    sumValue = np.sum(npData)
    npRateData = npData / sumValue
        
    return npRateData

def makeLogModel2(tunSet):
    npData = np.zeros(100)
    start = tunSet[0]
    end = tunSet[1]
    head = tunSet[2]
    height = tunSet[3]

    for i in range(start,end+1):
        if i>head:
            a1 = height**(1/(-1*(end-head)))
            gx = a1**(i-end)-1
            npData[i] = gx
        elif i<=head:
            a2 = height**(1/(head-0))
            fx = a2**(i-0)-1
            npData[i] = fx

    sumValue = np.sum(npData)
    npRateData = npData / sumValue
        
    return npRateData

def makeLogModel1(tunSet):
    npData = np.zeros(100)
    start = tunSet[0]
    end = tunSet[1]
    b = tunSet[2]
    c = tunSet[3]
    d = tunSet[4]
    h = tunSet[5]

    for i in range(start,end+1):    
        if (i-start)>0:
            value1 = ( 1/( d * (i-start) * b * math.sqrt(2*math.pi) ) )
            value2 = ((math.log((i-start)/c*d))**2)/(2*(b**2))
            value3 = value1 * math.exp(-1*value2)
            npData[i] = value3*h
        else :
            npData[i] = 0
        
        sumValue = np.sum(npData)
        npRateData = npData / sumValue
        
    return npRateData

def clusterAgeModel(rate,st,end):
    npData = np.zeros(100)
    for i in  range(st,end):
        npData[i] = (rate**(i-end))-1      
    sumValue = np.sum(npData)
    npRateData = npData / sumValue
    return npRateData


def makeArrayUseModel(tuningList):
    # model1 = clusterAgeModel(tuningList[0][0], tuningList[1][0], tuningList[2][0]) # 의대
    # model2 = clusterAgeModel(tuningList[0][1], tuningList[1][1], tuningList[2][1]) # 의전원
    # model3 = clusterAgeModel(tuningList[0][2], tuningList[1][2], tuningList[2][2]) # 재시험

    model1 = makeLogModel2(tuningList[0])
    model2 = makeLogModel2(tuningList[1])
    model3 = makeLogModel2(tuningList[2])

    resultData =  np.array([model1, model2, model3])
    return resultData


def makeAlivePerson(npData,year):
    deathRate = np.array([npDeathMan[year], npDeathWoman[year]])
    deadPerson = np.around((npData*deathRate))
    resultData = npData - deadPerson
    return resultData


def makeWorkPerson(npData,tuningSet):
    valueList = np.zeros([2,100])
    c = tuningSet[2]/((tuningSet[0]**(100-tuningSet[1]))-1)
    for i in range(100):
        resultRate = ((tuningSet[0]**(i-tuningSet[1]))-1)*c

        if resultRate < 0:
            valueList[0][i] = 0
            valueList[1][i] = 0
        elif resultRate > 1:
            valueList[0][i] = 1
            valueList[1][i] = 1
        else :
            valueList[0][i] = resultRate
            valueList[1][i] = resultRate

    retirePerson = np.around(npData*valueList)
    resultData = npData - retirePerson   
    return resultData


def makeNewPerson(tuningSet):
    oldSize = 100
    yearSize = 67
    modelSize = len(npPassDoctor[0])

    #신규인원 배열 67 x 2 x 100
    newPersonArray = np.zeros((yearSize,2,oldSize))

    modelAry = makeArrayUseModel(tuningSet)
    
    for i in range(yearSize):
        newPersonArray[i][0] += np.around(modelAry[0]*npPassDoctor[i][0])
        newPersonArray[i][1] += np.around(modelAry[0]*npPassDoctor[i][1])
        newPersonArray[i][0] += np.around(modelAry[1]*npPassDoctor[i][2])
        newPersonArray[i][1] += np.around(modelAry[1]*npPassDoctor[i][3])
        newPersonArray[i][0] += np.around(modelAry[2]*npPassDoctor[i][4])
        newPersonArray[i][1] += np.around(modelAry[2]*npPassDoctor[i][5])
    
    return newPersonArray

def shiftOld(personArray):
    dataArray = np.zeros((2,len(personArray[0])))
    dataArray[0] = np.roll(personArray[0], 1)  
    dataArray[1] = np.roll(personArray[1], 1)
    dataArray[0][0] = 0
    dataArray[1][0] = 0
    
    return dataArray

def makeResultPersonArray(tuningSet):
    # 1950~2016
    # 67 x 2 x 100 
    npNewPerson = makeNewPerson(tuningSet[0])
    npResultPerson = np.zeros(np.shape(npNewPerson))
    npResultPerson[1][0] = np.around(npFirstDoctor[0].astype(np.double))
    npResultPerson[1][1] = np.around(npFirstDoctor[1].astype(np.double))

    for i in range(2,67):
        # 1살 올리기 / shiftData -> 2 x 100
        shiftData = shiftOld(npResultPerson[i-1])
        # 사망률 적용 / aliveData -> 2 x 100
        aliveData = makeAlivePerson(shiftData, i)
        # 은퇴율 적용 / workData -> 2 x 100
        workData = makeWorkPerson(aliveData, tuningSet[1])
        # 최종 계산
        npResultPerson[i] =  workData + npNewPerson[i]
       
    return npResultPerson


def sumPeopleUseAge(npData):
    yearSize = len(npData)
    
    resultData = np.zeros([yearSize, 3, 12])
    
    for i in range(yearSize):
        for j in range(2):
            # 남/여 소계 계산
            resultData[i][j][0] = np.sum(npData[i][j])
            resultData[i][j][1] = np.sum(npData[i][j][0:30])
            resultData[i][j][2] = np.sum(npData[i][j][30:40])
            resultData[i][j][3] = np.sum(npData[i][j][40:50])
            resultData[i][j][4] = np.sum(npData[i][j][50:60])
            resultData[i][j][5] = np.sum(npData[i][j][60:])
            
            # 남/여 비율 계산
            for n in range(6):
                resultData[i][j][6+n] = resultData[i][j][n]/resultData[i][2][0] if resultData[i][2][0] > 0 else 0
        
        for j in range(6):
            # 합계 계산
            resultData[i][2][j] = resultData[i][0][j] + resultData[i][1][j]  
            # 합계 비율 계산
            resultData[i][2][6+j] = resultData[i][2][j]/resultData[i][2][0] if resultData[i][2][0] > 0 else 0
            # 남/여 비율 계산
            resultData[i][0][6+j] = resultData[i][0][j]/resultData[i][2][0] if resultData[i][2][0] > 0 else 0
            resultData[i][1][6+j] = resultData[i][1][j]/resultData[i][2][0] if resultData[i][2][0] > 0 else 0


    return resultData

def calculateCost(npData):   
    npSumData = np.concatenate((npData[0][:2],npData[1][:2],npData[2][:2],npData[3][:2],npData[4][:2],npData[5][:2]),axis=0)
    npResultData = np.abs(npDoctorAgeData - npSumData)
    return npResultData

def getCost(tuningSet):
    npResultData = makeResultPersonArray(tuningSet)
    npSumData = sumPeopleUseAge(npResultData[61:67])
    npCalData = calculateCost(npSumData)

    return npCalData


def startGetCost():
    tAge1 = np.arange(0.1, 1, 0.1) # 연령분포모델1 변수 / 범위 0~1
    tAge2 = np.arange(0.1, 1, 0.1) # 연령분포모델2 변수 / 범위 0~1
    tAge3 = np.arange(0.1, 1, 0.1) # 연령분포모델3 변수 / 범위 0~1
    tAge4 = np.arange(40,41) # 합격연령 최대치 / 범위 30~45
    tRetire1 = np.arange(1.1, 2, 0.1) # 은퇴율모델 변수1 / 범위 1 이상
    tRetire2 = np.arange(30, 31) # 은퇴율모델 변수2 / 은퇴시작나이 / 범위 20 이상
    tRetire3 = np.arange(0.1, 1, 0.1) # 은퇴율모델 변수3 / 범위 0~1
    
    dataSize = len(tAge1)*len(tAge2)*len(tAge3)*len(tAge4)*len(tRetire1)*len(tRetire2)*len(tRetire3)
    timeMinute = dataSize*20/1000/60
    curentData = 0
    resultData = []
    

    now = time.localtime()
    print("Start Time : %04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    print("learn Time : " + str(round(timeMinute)) + "min")
    print("Data Size = " + str(dataSize))
    print("")
    
    for h in tAge1:
        for i in tAge2:
            print(str(round(curentData/dataSize,2))+'%')
            for j in tAge3:
                for k in tAge4:
                    for m in tRetire1:
                        for n in tRetire2:
                            for p in tRetire3:
                                resultData.append([[h,i,j,k,m] ,idoctor.getCost([[[h, i, j],[26,28,27],[k,k,k]], [m,n,p]])])
                                curentData += 1

    return resultData