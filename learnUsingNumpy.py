import iddModel.doctor as idoctor


#의대수, 의전원수, 의대남비율, 의전원남비율 
npBasicPopulation = np.zeros([22,4])
for i in range(22):
    npBasicPopulation[i] = np.array([3400,50,0.6,0.6])
    
tuningSetAgeRate = [[0.9,0.6,0.1,0.1,0.9,0.9],[26,26,28,28,27,27],[39, 39, 39, 39, 39, 39]]
tuningSetRetireRate = [[1.2, 1.2],[30, 30],[0.4, 0.1]]
tuningSet = [tuningSetAgeRate, tuningSetRetireRate]



dataTest2 = idoct.makeDoctorData(npBasicPopulation, tuningSet)
dfTest = pd.DataFrame(dataTest2[4])
#dfTest.index = range(1950,2048)
print(dfTest)