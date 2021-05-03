import math

filePath = 'C:/Users/saya6/Documents/NCNR/kineticsDataAnalizer/LionSi_kinetics4805_0.refl'

# fulltext = []
with open(filePath) as f:
    lines = f.readlines()
    # print(lines)
#     fulltext.append(lines)
# print('fulltext', fulltext)
# print(len(fulltext))

# this fails with space in a string ("title":"cdr slit")
text = open(filePath, 'r')
fullText = [line.split(' ') for line in text.readlines()]
print('fullText', fullText)
print(len(fullText))

rfl1dData = []
word1 = 'name'
word2 = 'units'
nameRowNumbers = []
unitRowNumbers = []
rowNumberDataStarts = []
rowNumberDataEnds = []
totalRow=0
for i, line in enumerate(lines):
    if word1 in line:
        print(word1)
        print(i)
        firstRowOfData = i+1
        # print(firstRowOfData)
        nameRowNumbers.append(i)
        endOfData = i-3
        print('endOfData', endOfData)
        if endOfData > 10:
            # get endOfData from the data set "entry" 2 and above,
            # "entry" 1 results in endOfData = -2 and does not get appended
            rowNumberDataEnds.append(endOfData)

    # one row after "units" is the start of data set
    if word2 in line:
        print('line of word2')
        print(i)
        unitRowNumbers.append(i)
        dataStarts = i+1
        rowNumberDataStarts.append(dataStarts)
    totalRow = totalRow + 1

print((totalRow))
rowNumberDataEnds.append(totalRow)

print('nameRowNumbers', nameRowNumbers)
print('unitRowNumbers', unitRowNumbers)
print('rowNumberDataEnds', rowNumberDataEnds)
print('rowNumberDataStarts', rowNumberDataStarts)

dataList = []
for a in range(len(rowNumberDataStarts)):
    print('a', a)
    startRow = rowNumberDataStarts[a]
    print('startRow', startRow)
    print(type(startRow))
    endRow = rowNumberDataEnds[a]+1
    individualList = fullText[startRow: endRow]
    # test = fullText[10:20]
    # print('test', test)
    print('individualList', individualList)
    dataList.append(individualList)


# 2(S1-S2)/(E1+E2)  where S is specular intensity and E is SQRT(S)
# print('dataList', dataList)
print('len((dataList))', len(dataList))
while a in range(len(dataList)-1):
    print('datalist[a]', dataList[a])
    print('datalist[a+1]', dataList[a+1])
    indivisualResiduals = []
    individualRelativeDifferences = []

    for b in range(len(dataList[a])):
        if b <= len(dataList[a]):
            print('a', a)
            print('b', b)
            S1 = float(dataList[a][b][1])
            # S1 = dataList[a][b][1]
            S2 = float(dataList[a+1][b][1])
            E1 = math.sqrt(S1)
            E2 = math.sqrt(S2)
            # print('S1, S2', S1, S2)
            print('S1, S2, E1, E2', S1, S2, E1, E2)

            try:
                residual = 2*(S1-S2)/(E1+E2)
                relativeDifference = 2*(S1-S2)/(S1+S2)
                indivisualResiduals.append(residual)
                individualRelativeDifferences.append(relativeDifference)
            except:
                # if E1+E2 = 0 or S1+S2 = 0
                indivisualResiduals.append('value zero')
                individualRelativeDifferences.append('value zero')

        else:
            a+1
        print('indivisualResiduals', indivisualResiduals)
        print('individualRelativeDifferences', individualRelativeDifferences)















