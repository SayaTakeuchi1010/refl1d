import math

filePath = 'C:/Users/saya6/Documents/NCNR/kineticsDataAnalizer/LionSi_kinetics4805_0.refl'

class ReadRefl1d:
    filePath = 'C:/Users/saya6/Documents/NCNR/kineticsDataAnalizer/LionSi_kinetics4805_0.refl'

    def getFulTextSplitWithSpace(self, filePath):
        # this fails with space in a string e.g. ("title":"cdr slit")
        # works ok for data part
        text = open(filePath, 'r')
        fullText = [line.split(' ') for line in text.readlines()]
        return fullText

    def radLines(self, filePath):
        with open(filePath) as f:
            lines = f.readlines()
        return lines


    def getStartEndRowNumbers(self, lines):
        word1 = 'name'
        word2 = 'units'
        nameRowNumbers = []
        unitRowNumbers = []
        rowNumberDataStarts = []
        rowNumberDataEnds = []

        totalRow = 0
        for i, line in enumerate(lines):
            if word1 in line:

                nameRowNumbers.append(i)
                # data ends 3 rows before rpw with 'name"
                endOfData = i - 3
                if endOfData > 10:
                    # get endOfData from the data set ' "entry":1 ' and above,
                    # ' "entry":0 ' results in endOfData = -2 and does not append rowNumberDataEnds
                    rowNumberDataEnds.append(endOfData)

            if word2 in line:
                unitRowNumbers.append(i)
                # one row after "units" is the start of data set
                dataStarts = i + 1
                rowNumberDataStarts.append(dataStarts)

            # move pn to next row
            totalRow = totalRow + 1

        # append the last row of where data ends
        rowNumberDataEnds.append(totalRow)

        return rowNumberDataStarts, rowNumberDataEnds


    def createDataList(self, rowNumberDataStarts, rowNumberDataEnds, fullText):
        dataList = []
        for a in range(len(rowNumberDataStarts)):
            startRow = rowNumberDataStarts[a]
            endRow = rowNumberDataEnds[a] + 1
            # list[start:stop], value of stop is the point where the list cuts off. +1 to include the last data row
            # individualList = [["Qz", "Intensity", "uncertainty", "resolution"], ["Qz",,, "resolution"]...]
            # extract one data set entry from .refl1d
            individualList = fullText[startRow: endRow]

            # change dataList from strings to floats
            individualListInFloat = []
            for b in range(len(individualList)):
                oneRowInFloat = []
                # 4 columns in each row
                for c in range(4):
                    oneDataInARow = float(individualList[b][c])
                    oneRowInFloat.append(oneDataInARow)
                individualListInFloat.append(oneRowInFloat)
            dataList.append(individualListInFloat)
        return dataList



    def calculateResidualAndRelativeDifference(self, dataList):
        ### this part needs to be fixed to take any selected entry number ##@
        while a in range(len(dataList) - 1):
            indivisualResiduals = []
            individualRelativeDifferences = []

            #len(dataList[a]) is number of rows in each entry
            for b in range(len(dataList[a])):
                if b <= len(dataList[a]):
                    # 2(S1-S2)/(E1+E2)  where S is specular intensity and E is SQRT(S)
                    S1 = dataList[a][b][1]
                    S2 = dataList[a + 1][b][1]
                    E1 = math.sqrt(S1)
                    E2 = math.sqrt(S2)

                    try:
                        residual = 2 * (S1 - S2) / (E1 + E2)
                        relativeDifference = 2 * (S1 - S2) / (S1 + S2)
                        indivisualResiduals.append(residual)
                        individualRelativeDifferences.append(relativeDifference)
                    except:
                        # if E1+E2 = 0 or S1+S2 = 0
                        indivisualResiduals.append('value zero')
                        individualRelativeDifferences.append('value zero')

                else:
                    a + 1
        return indivisualResiduals, individualRelativeDifferences


    def getSampleName(self, lines):
        for i, line in enumerate(lines):
            if 'name' in line:
                sampleName = line[11:-2]
        return sampleName
        print('sampleName', sampleName)


def main():
    rr = ReadRefl1d
    filePath = 'C:/Users/saya6/Documents/NCNR/kineticsDataAnalizer/LionSi_kinetics4805_0.refl'
    fullText = rr.getFulTextSplitWithSpace(rr, filePath)
    print('fullText', fullText)
    lines = rr.radLines(rr, filePath)
    print('lines', lines)
    rowNumberDataStarts, rowNumberDataEnds = rr.getStartEndRowNumbers(rr, lines)
    print('rowNumberDataStarts', rowNumberDataStarts)
    print('rowNumberDataEnds', rowNumberDataEnds)
    dataList = rr.createDataList(rr, rowNumberDataStarts, rowNumberDataEnds, fullText)
    print('dataList', dataList)




if __name__ == "__main__":
    main()






