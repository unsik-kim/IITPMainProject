import pandas as pd
import numpy as np

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

# 2011~2016년
npDoctorAgeData = np.array(pd.read_excel('iddModel/data/의사연령별분포.xlsx'))

# 1951년 의사수
dfFirstDoctor = pd.read_excel('iddModel/data/firstDoctor.xlsx')
npFirstDoctor = np.array(dfFirstDoctor)[:,1:-1]

# 1950~2020년 연령분포
dfKoreaAgePopRateData = pd.read_excel('iddModel/data/koreaAgePopRateData.xlsx')
npKoreaAgePopRateDataMan = np.array(dfKoreaAgePopRateData[dfKoreaAgePopRateData['sex']=='MALE'])[:,2:]
npKoreaAgePopRateDataWoman = np.array(dfKoreaAgePopRateData[dfKoreaAgePopRateData['sex']=='FEMALE'])[:,2:]

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


def clusterAgeModel(rate,st,end):
    npData = np.zeros(100)
    
    for i in range(st,end):
        npData[i] = (rate**(i-end))-1  
        
    sumValue = np.sum(npData)
    npRateData = npData / sumValue
    return npRateData

def makeAlivePerson(npData,year):
    
    deathRate = np.array([npDeathMan[year], npDeathWoman[year]])
    deadPerson = np.around((npData*deathRate))
    resultData = npData - deadPerson
    
    return [resultData, deadPerson]

def makeWorkPerson(npData,tuningSet):
    valueList = np.zeros([2,100])
    c1 = tuningSet[2][0]/((tuningSet[0][0]**(100-tuningSet[1][0]))-1)
    c2 = tuningSet[2][1]/((tuningSet[0][1]**(100-tuningSet[1][1]))-1)

    for i in range(100):
        result1 = ((tuningSet[0][0]**(i-tuningSet[1][0]))-1)*c1
        result2 = ((tuningSet[0][1]**(i-tuningSet[1][1]))-1)*c2
        valueList[0][i] = 0 if result1<0 else 1 if result1>1 else  result1
        valueList[1][i] = 0 if result2<0 else 1 if result2>1 else  result2

    retirePerson = np.around(npData*valueList)
    resultData = npData - retirePerson
    
    return [resultData, retirePerson]

def makeArrayUseModel(tuningList):
    # model1 = clusterAgeModel(tuningList[0][0], tuningList[1][0], tuningList[2][0]) # 의대 남
    # model2 = clusterAgeModel(tuningList[0][1], tuningList[1][1], tuningList[2][1]) # 의대 여
    # model3 = clusterAgeModel(tuningList[0][2], tuningList[1][2], tuningList[2][2]) # 의전원 남
    # model4 = clusterAgeModel(tuningList[0][3], tuningList[1][3], tuningList[2][3]) # 의전원 여
    # model5 = clusterAgeModel(tuningList[0][4], tuningList[1][4], tuningList[2][4]) # 재시험 남
    # model6 = clusterAgeModel(tuningList[0][5], tuningList[1][5], tuningList[2][5]) # 재시험 여
    
    model1 = makeLogModel2(tuningList[0])
    model2 = makeLogModel2(tuningList[1])
    model3 = makeLogModel2(tuningList[2])
    # model1 = makeLogModel2(tuningList[3])
    # model2 = makeLogModel2(tuningList[4])
    # model3 = makeLogModel2(tuningList[5])

    resultData =  np.array([model1, model2, model3, model4, model5, model6])
    
    return resultData

def makeNewPerson(npData, tuningSet):
    oldSize = 100
    yearSize = len(npData)
    modelSize = len(npData[0])
    
    #모델 적용 배열 98 x 6 x 100
    applyModelArray = np.zeros((yearSize,modelSize,oldSize))

    #신규인원 배열 98 x 2 x 100
    newPersonArray = np.zeros((yearSize,2,oldSize))

    modelAry = makeArrayUseModel(tuningSet)
    
    for i in range(yearSize):
        for j in range(modelSize):
            applyModelArray[i][j] = np.around(modelAry[j]*np.around(npData[i][j]))

            if j%2==0:
                newPersonArray[i][0] += applyModelArray[i][j]
            else:
                newPersonArray[i][1] += applyModelArray[i][j]
    
    resultData = newPersonArray
    
    return resultData

def shiftOld(personArray):
    dataArray = np.zeros((2,len(personArray[0])))
    dataArray[0] = np.roll(personArray[0], 1)  
    dataArray[1] = np.roll(personArray[1], 1)
    dataArray[0][0] = 0
    dataArray[1][0] = 0
    
    return dataArray

def makeResultPersonArray(newPersonArray, tuningSet):
    #누적인원 배열
    sizeArray = list(np.shape(newPersonArray))
    yearSize = sizeArray[0]
    
    # 98 x 2 x 100 
    resultPersonArray = np.zeros(sizeArray)
    deadPersonArray = np.zeros(sizeArray)
    retirePersonArray = np.zeros(sizeArray)

    for i in range(yearSize):
        # 1살 올리기 / shiftData -> 2 x 100
        shiftData = shiftOld(resultPersonArray[i-1])

        # 사망률 적용 / aliveData -> 2 x 100
        aliveData = makeAlivePerson(shiftData, i)
        deadPersonArray[i] = aliveData[1]

        # 은퇴율 적용 / workData -> 2 x 100
        workData = makeWorkPerson(aliveData[0], tuningSet)
        retirePersonArray[i] = workData[1]

        # 최종 계산
        resultPersonArray[i] =  workData[0] + newPersonArray[i]

            
            
    return [resultPersonArray,newPersonArray,deadPersonArray,retirePersonArray]


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
    resultData = np.zeros([6,5,5])

    for i in range(6):
        manNumCost = npData[39-i][0][1:6] - npAgeData[5-i][8:13]
        womanNumCost = npData[39-i][1][1:6] - npAgeData[5-i][14:19]
        totalNumCost = npData[39-i][2][1:6] - npAgeData[5-i][2:7]
        
        manRateCost = npData[39-i][0][7:12] - npAgeData[5-i][26:31]
        womanRateCost = npData[39-i][1][7:12] - npAgeData[5-i][32:37]
        
        npCostArray = np.array([manNumCost, womanNumCost, totalNumCost, 
                    manRateCost, womanRateCost])

        resultData[i] = npCostArray

    return resultData

def getCost(npData, tuningSet):
    newPerson = makeNewPerson(npData, tuningSet[0])
    resultPerson = makeResultPersonArray(newPerson,tuningSet[1])
    
    # sumData -> 43 x 3 x 12
    sumData = sumPeopleUseAge(resultPerson)
    costData = calculateCost(sumData)
    
    return [sumData, costData]

def makeDataFrame(npData):
    dfList = []
    startYear = 1950
    for i in range(4):
        for j in range(2):
            dfResult = pd.DataFrame(npData[i][0][j]).T
            indexList = []
            indexList.append(startYear)

            for k in range(1,98):
                dfResult = pd.concat([dfResult,pd.DataFrame(npData[i][k][j]).T])
                indexList.append(k+startYear)

            dfResult.index = indexList 
            dfList.append(dfResult)
            
    return dfList

def makeThousandPerDoctor(dfResultPerson, npPopulation):
    startYear = 1950
    dfResultPersonSum = dfResultPerson[2].sum(axis=1)
    npResultPersonSum = np.array(dfResultPersonSum)
    dfThousandPerDoctor = pd.DataFrame(npResultPersonSum/npPopulation*1000)
    dfThousandPerDoctor.index = range(startYear, 2048)
    return dfThousandPerDoctor

def makeFuturePerson(npBasicPopulation):
    yearSize = 98
    optSize = len(npBasicPopulation)
    npFuturePerson = np.zeros([yearSize,6])
    
    for i in range(optSize):
        npDoctorExam[i+76][0] = (npBasicPopulation[i][0]*0.94)+(npBasicPopulation[i][1]*0.94) #의대 합격자
        npDoctorExam[i+76][1] = (npBasicPopulation[i][0]*0.06)+(npBasicPopulation[i][1]*0.06) # 의대 불합격자 
        
        popSum = npBasicPopulation[i][0]+npBasicPopulation[i][1]+npDoctorExam[i+75][1]

        npPassDoctorRate[i+76][0] = (npBasicPopulation[i][0]*npBasicPopulation[i][2])/popSum #의대남자비율
        npPassDoctorRate[i+76][1] = (npBasicPopulation[i][0]*(1-npBasicPopulation[i][2]))/popSum #의대여자비율
        npPassDoctorRate[i+76][2] = (npBasicPopulation[i][1]*npBasicPopulation[i][3])/popSum #의전원남자비율
        npPassDoctorRate[i+76][3] = (npBasicPopulation[i][1]*(1-npBasicPopulation[i][3]))/popSum #의전원여자비율
        npPassDoctorRate[i+76][4] = npDoctorExam[i+75][1]*(npPassDoctorRate[i+76][0]+npPassDoctorRate[i+76][2])/popSum # 불합격남자비율
        npPassDoctorRate[i+76][5] = npDoctorExam[i+75][1]*(npPassDoctorRate[i+76][1]+npPassDoctorRate[i+76][3])/popSum # 불합격여자비율
        
        npFuturePerson[i+76][0] = np.around(popSum * npPassDoctorRate[i+76][0])
        npFuturePerson[i+76][1] = np.around(popSum * npPassDoctorRate[i+76][1])
        npFuturePerson[i+76][2] = np.around(popSum * npPassDoctorRate[i+76][2])
        npFuturePerson[i+76][3] = np.around(popSum * npPassDoctorRate[i+76][3])
        npFuturePerson[i+76][4] = np.around(popSum * npPassDoctorRate[i+76][4])
        npFuturePerson[i+76][5] = np.around(popSum * npPassDoctorRate[i+76][5])
        
    return npFuturePerson


def makeDoctorData(npData, tuningSet):
    #의대수, 의전원수, 의대남비율, 의전원남비율 

    npFuturePerson = makeFuturePerson(npData)
    npNewPassDoctor = npPassDoctor + npFuturePerson
    newPerson = makeNewPerson(npNewPassDoctor, tuningSet[0])
    resultData = makeResultPersonArray(newPerson,tuningSet[1])

    dfData = makeDataFrame(resultData)

    dfResultPerson = [dfData[0],dfData[1],dfData[0]+dfData[1]] # 의사수
    dfNewPerson = [dfData[2],dfData[3],dfData[2]+dfData[3]]    # 신규의사수
    dfDeadPerson = [dfData[4],dfData[5],dfData[4]+dfData[5]]   # 사망자수
    dfRetirePerson = [dfData[6],dfData[7],dfData[6]+dfData[7]] # 은퇴자수
    dfThousandPerDoctor = makeThousandPerDoctor(dfResultPerson, npPopulation) # 1000명당 의사수
    
    return [dfResultPerson, dfNewPerson, dfDeadPerson, dfRetirePerson, dfThousandPerDoctor]


def clusterAgeModel(center,start,rate):
    npData = np.zeros(100)
    
    for i in range(st,end):
        npData[i] = ()
        
    sumValue = np.sum(npData)
    npRateData = npData / sumValue
    return npRateData