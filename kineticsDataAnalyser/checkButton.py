import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import TextBox
from readRefl1d import ReadRefl1d as rr
from itertools import cycle
import math
import os

# get list from readRefl1d
dataInFloat = rr.dataList
sampleName = rr.sampleName


### plot original data in ax_1[0, 0] ###
dataToPlot = []
for a in range(len(dataInFloat)):
    # print('a', a)
    qzIntUncertainty = []
    # create list of Qz
    listOfQz = []
    for i in range(len(dataInFloat[a])):
        listOfQz.append(dataInFloat[a][i][0])
    # print('listOfQz', listOfQz)

    listOfInt = []
    for i in range(len(dataInFloat[a])):
        listOfInt.append(dataInFloat[a][i][1])
    # print('listOfInt', listOfInt)

    listOfUncertainty = []
    for i in range(len(dataInFloat[a])):
        listOfUncertainty.append(dataInFloat[a][i][2])
    # print('listOfUncertainty', listOfUncertainty)

    qzIntUncertainty.append(listOfQz)
    qzIntUncertainty.append(listOfInt)
    qzIntUncertainty.append(listOfUncertainty)
    dataToPlot.append(qzIntUncertainty)

colors = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])

fig_1, ax_1 = plt.subplots(nrows=1, ncols=2)
ax_1[0].set_title('Qz vs. Intensity')
ax_1[0].set_xlabel('Qz')
ax_1[0].set_ylabel('intensity')
ax_1[0].ticklabel_format(axis='both', style='scientific')
ax_1[0].semilogy()


allplotsData = []
allplotsErrorbar = []

# TODO take 'entry' from .refl do not append with list order
# plot thw whole entry(0 ~ n) in one plot
for i in range(len(dataToPlot)):
    lineiData = ax_1[0].plot(dataToPlot[i][0], dataToPlot[i][1], label='entry' + str(i), color=next(colors), marker='.')
    # print('lineiData', lineiData)
    allplotsData.append(lineiData)
    # add 'color, entry i' box in left panel
    ax_1[0].legend(loc='best', fontsize='small')


### plot original data in ax_1[0, 0] end ###


### check buttons to make visible/not visible in ax_1[0, 1] ###

# get list of labels
labels = []
for i in range(len(dataToPlot)):
    label = sampleName + '_entry' + str(i)
    labels.append(label)


# make check box inside panel 2 (location 1 in figsize = (8, 4), nrows=1, ncols=3)
rax = ax_1[ 1]

rax.set_title('List of data')

activated = []
for i in range(len(dataToPlot)):
    activated.append(True)
# print('activated', activated)

chxbox = CheckButtons(rax, labels, activated)

def set_visible(label):
    index = labels.index(label)
    # print('label', label)
    # print('labels', labels)
    # allplotsData[index][0]: get inside of the list to get <class 'matplotlib.lines.Line2D'>
    # print('allplotsData[index]', allplotsData[index][0])
    # print(type(allplotsData[index][0]))
    allplotsData[index][0].set_visible(not allplotsData[index][0].get_visible())

    ### may need to handle inside the order in artist to deal with error bar ###
    # https://stackoverflow.com/questions/19470104/python-matplotlib-errorbar-legend-picking
    # allplotsErrorbar[index].set_visible(not allplotsErrorbar[index].get_visible())

    # update legend and do not show the lines not shown, but label still exists
    ax_1[0].legend(loc='best', fontsize='small')
    # lgd = ax_1[0, 0].legend()
    # lgd.set_visible(True)

    plt.draw()

chxbox.on_clicked(set_visible)

### check buttons to make visible/not visible in ax_1[0, 1] end ###


### error bar plot part ####

fig_2, ax_2 = plt.subplots()
ax_2.set_title('Qz vs. Intensity (error bar)')
ax_2.set_xlabel('Qz ')
ax_2.set_ylabel('Intensity ')

textBoxLocation = fig_2.add_axes([0.05, 0.05, 0.05, 0.05])
### make sure input has comma after number for single entry ###
textBox = TextBox(textBoxLocation, 'input')

def submit(expression):
    ax_2.clear()
    selectedEntry = list(eval(expression))
    print('selectedEntry', selectedEntry)
    print(type(selectedEntry))

    selectedPlotsData = []
    for i in range(len(selectedEntry)):
        # print('i in submit for loop', i)
        # print('selectedEntry[i]', selectedEntry[i])
        erroriData = ax_2.errorbar(dataToPlot[selectedEntry[i]][0], dataToPlot[selectedEntry[i]][1], label='entry' + str(selectedEntry[i]), yerr=dataToPlot[selectedEntry[i]][2], color=next(colors))
        selectedPlotsData.append(erroriData)
        ax_2.legend(loc='best')

    ax_2.set_title('Qz vs. Intensity (error bar)')
    ax_2.set_xlabel('Qz ')
    ax_2.set_ylabel('Intensity ')
    # error below
    # ax_1[1, 0].ticklabel_format(axis='both', style='scientific')
    ax_2.semilogy()
    # ax_1[1, 0].autoscale_view()

    # below does not work
    plt.draw()

textBox.on_submit(submit)

### error bar plot part  end####


### residuals plot part ####
fig_3, ax_3 = plt.subplots()

entryForResidualsLocation = fig_3.add_axes([0.5, 0.05, 0.05, 0.05])
### make sure input has comma after number for single entry ###
entryForResiduals = TextBox(entryForResidualsLocation, 'selected entry number')
ax_3.set_title('Qz vs. Residual')
ax_3.set_xlabel('Qz ')
ax_3.set_ylabel('Residual: 2(S1-S2)/(E1 + E2)')

# ntryNumberForResidualList = []
def getEntryNumber(expression):
    ax_3.clear()
    ax_3.set_title('Qz vs. Residual')
    ax_3.set_xlabel('Qz ')

    entryNumberForResidual = list(eval(expression))
    # print('entryNumberForResidual', entryNumberForResidual)
    # print(type(entryNumberForResidual))
    # entryNumberForResidualList.append(entryNumberForResidual)
    # return entryNumberForResidual

    # print('entryNumberForResidualList', entryNumberForResidualList)

    residualsList = []
    relativeDifferencesList = []

    # len(dataList[a]) is number of rows in each entry

    # dataToPlot[list of "Qz"][list of "Intensity"][list of "uncertainty"]
    for a in range(len(dataToPlot[entryNumberForResidual[0]][0])):
        # print('entryNumberForResidual[0]', entryNumberForResidual[0])
        # print('entryNumberForResidual[1]', entryNumberForResidual[1])
        # print('dataToPlot[entryNumberForResidual[0]]', dataToPlot[entryNumberForResidual[0]][0])
        # print('dataToPlot[entryNumberForResidual[1]]', dataToPlot[entryNumberForResidual[1]][0])


        # 2(S1-S2)/(E1+E2)  where S is specular intensity and E is SQRT(S)
        S1 = dataToPlot[entryNumberForResidual[0]][1][a]
        S2 = dataToPlot[entryNumberForResidual[1]][1][a]
        E1 = math.sqrt(S1)
        E2 = math.sqrt(S2)

        print('S1, S2, E1, E2', S1, S2, E1, E2)

        try:
            residual = 2 * (S1 - S2) / (E1 + E2)
            relativeDifference = 2 * (S1 - S2) / (S1 + S2)
            residualsList.append(residual)
            relativeDifferencesList.append(relativeDifference)
        except:
            # if E1+E2 = 0 or S1+S2 = 0
            residualsList.append(0)
            relativeDifferencesList.append(0)

    ## calculation checked with first and last of 3-4 rows of data set##

    # print('residualsList', residualsList)
    # print('relativeDifferencesList', relativeDifferencesList)

    ax_3.set_ylabel('Residual:2(S1-S2)/(E1+E2)', color = 'r')
    ax_3.tick_params(axis='y', labelcolor='r')
    # TODO change line width
    residualsPlot = ax_3.plot(dataToPlot[entryNumberForResidual[0]][0], residualsList, color='r', marker='.')

    ax_3_2 = ax_3.twinx()
    ax_3_2.tick_params(axis='y', labelcolor='b')
    ax_3_2.set_ylabel('Relative Differences', color='b')

    # TODO change line width
    relativeDifferencesPlot = ax_3_2.plot(dataToPlot[entryNumberForResidual[0]][0], relativeDifferencesList, color='b', marker='.')

    # print('residual plot before draw')

    plt.draw()

entryForResiduals.on_submit(getEntryNumber)

### residuals plot part end ####

### combine data and plot part ###

fig_4, ax_4 = plt.subplots()
entryForCombineDataLocation = fig_4.add_axes([0.8, 0.9, 0.05, 0.05])
### make sure input has comma after number for single entry ###
entryForCombineData = TextBox(entryForCombineDataLocation, 'combine data')

ax_4.set_title('combine data')
ax_4.set_xlabel('Qz')
ax_4.set_ylabel('intensity')
ax_4.semilogy()

def combineData(expression):
    ax_4.clear()
    # entry must be only two selected data (list length must be 2 to make inside for-loop work
    entryNumberForCombineData = list(eval(expression))

    # check how many data to combine
    numberOfDataToCombine = len(entryNumberForCombineData)
    print('numberOfDataToCombine', numberOfDataToCombine)

    # create empty list to put in combined data
    combinedIntensityList = []

    dataToCombine = []
    for n in range(numberOfDataToCombine):
        intOfOeDataSet = dataToPlot[entryNumberForCombineData[n]][1]
        dataToCombine.append(intOfOeDataSet)
    # taking the right data set, checked by first and last couple of intensity columns of selected data
    print('dataToCombine', dataToCombine)

    # take length of Qz column len(dataToPlot[entryNumberForCombineData[0]][0]), should be the same uf u take other columns
    # for loop appears to be working. entry1+entry2 in previous code with individualCombinedData = (S1+S2)/2 match with current code
    for a in range(len(dataToPlot[entryNumberForCombineData[0]][0])):
        print('len(dataToPlot[entryNumberForCombineData[0]][0])', len(dataToPlot[entryNumberForCombineData[0]][0]))

        sumData = 0
        for n in range(numberOfDataToCombine):
            # combine the values in the same row
            oneData = dataToPlot[entryNumberForCombineData[n]][1][a]
            #print('dataToPlot[entryNumberForCombineData[n]][1]', dataToPlot[entryNumberForCombineData[n]][1][a])
            #print(type(oneData))
            print('oneData', oneData)
            sumData = float(sumData) + float(oneData)
            print('sumData', sumData)
            #print('sumData', sumData)

            #print('n', n)

        # combine n number of data points and divide by n
        print('numberOfDataToCombine after for n ...', numberOfDataToCombine)
        indivisualCombinedIntensity = sumData/numberOfDataToCombine
        print('indivisualCombinedIntensity', indivisualCombinedIntensity)

        combinedIntensityList.append(indivisualCombinedIntensity)

    print('combinedIntensityList', combinedIntensityList)

    # set aces label and semi log scale for y
    ax_4.set_xlabel('Qz')
    ax_4.set_ylabel('Intensity')
    ax_4.semilogy()

    # x axis : Qz = dataToPlot[entryNumberForCombineData[0]][0]
    # y axis : combined intensity = combinedDataList
    combinedDataPlot = ax_4.plot(dataToPlot[entryNumberForCombineData[0]][0], combinedIntensityList, color='k', marker='.')

    # put Qz and combined intensity in one list
    combinedQzIntList = []
    for a in range(len(dataToPlot[entryNumberForCombineData[0]][0])):
        # text format: str(Qz) + (space) + str(Intensity)
        oneLine= str(dataToPlot[entryNumberForCombineData[0]][0][a]) + ' ' + str(combinedIntensityList[a])
        combinedQzIntList.append(oneLine)
    print('combinedQzIntList', combinedQzIntList)

    # create a folder  for combined data text if it doesn't exist
    parentDirectory = 'C:/Users/saya6/Documents/NCNR/kineticsDataAnalizer'
    folderName = sampleName + '_Combined'
    path = os.path.join(parentDirectory, folderName)
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)
        pass
    # make folder directory
    folderDirectory = 'C:/Users/saya6/Documents/NCNR/kineticsDataAnalizer/' + folderName + '/'


    # combined entry names
    n = 0
    combinedEntryNames = '_entry'
    # for two dataset entry, range is range(2), takes position 0 ~ 2.
    for n in range(numberOfDataToCombine):
        print('n', n)

        print('range(numberOfDataToCombine-1)', range(numberOfDataToCombine))
        if n < numberOfDataToCombine-1:
            print('n begining of  if', n)
            combinedEntryNames = combinedEntryNames + str(entryNumberForCombineData[n]) + ','
            print('n end of  if', n)
            print('numberOfDataToCombine-1', numberOfDataToCombine)
        elif n == numberOfDataToCombine-1:
            print('in elif')
            combinedEntryNames = combinedEntryNames + str(entryNumberForCombineData[n])

    print('combinedEntryNames', combinedEntryNames)


    # export combnied data into text file
    textFileName = folderDirectory + sampleName + combinedEntryNames +'.txt'
    f = open(textFileName, "a+")
    # 'w+' overwrites previous data? "Date modified" time gets updated"

    # take each line in list and put into txt
    for element in combinedQzIntList:
        f.write(element)
        f.write('\n')

    f.close

    plt.draw()

entryForCombineData.on_submit(combineData)

### combine data and plot part end ###

plt.show()