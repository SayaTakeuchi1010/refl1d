import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import TextBox
from readRefl1d import ReadRefl1d as rr
from itertools import cycle
import os
import numpy as np

### CHANGE DIRECTORY HERE ###
parentDirectory = 'C:/Users/saya6/Documents/NCNR/kineticsDataAnalizer'

# get list of float data and sampleName from readRefl1d
dataInFloat = rr.dataList
sampleName = rr.sampleName
entryNames = rr.entryList


### plot original data in fig_1, ax_1[0]  ###

# dataInFloat format is [[Qz, intensity, uncertainty], [Qz, intensity, uncertainty]...]
# change format to [[row1 Qz, row2 Qz,,,][row1 int, row2 int,,,][row1 uncertainty, row2 uncertainty,,]],,,,

dataToPlot = []
for a in range(len(dataInFloat)):
    # empty list to append Qz, Intensity and uncertainty for one entry
    qzIntUncertainty = []

    # create empty list of Qz
    listOfQz = []
    for i in range(len(dataInFloat[a])):
        # append Qz value in
        listOfQz.append(dataInFloat[a][i][0])

    # create empty list of Intensity
    listOfInt = []
    for i in range(len(dataInFloat[a])):
        listOfInt.append(dataInFloat[a][i][1])

    # create empty list of uncertainty
    listOfUncertainty = []
    for i in range(len(dataInFloat[a])):
        listOfUncertainty.append(dataInFloat[a][i][2])

    # listOfQz format: [row1 Qz, row2 Qz,,,]
    # lisfOfInt format: [row1 int, row2 int,,,]
    # listOfUncertainty format: [row1 uncertainty, row2 uncertainty,,]
    qzIntUncertainty.append(listOfQz)
    qzIntUncertainty.append(listOfInt)
    qzIntUncertainty.append(listOfUncertainty)
    # qzIntUncertainty format: [row1 Qz, row2 Qz,,,][row1 int, row2 int,,,][row1 uncertainty, row2 uncertainty,,] of entry#
    dataToPlot.append(qzIntUncertainty)
    # dataToPlot format: [[entry0 qzIntUncertainty], [entry1 qzIntUncertainty],,,]

# list of color that python would go through. It has more than 10, and probably don't use everything.
colors = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])

# fig1 has Qz vs Intensity on left panel, check box with list of original entries in right box
fig_1, ax_1 = plt.subplots(nrows=1, ncols=2)
ax_1[0].set_title('Qz vs. Intensity')
ax_1[0].set_xlabel('Qz')
ax_1[0].set_ylabel('intensity')
ax_1[0].ticklabel_format(axis='both', style='scientific')
ax_1[0].semilogy()


allplotsMatplotlib = []
allplotsErrorbar = []

# TODO take 'entry' from .refl do not append with list order
# plot thw whole entry(0 ~ n) in one plot
for i in range(len(dataToPlot)):
    # entry looks correct in order
    print('dataToPlot[i][0], dataToPlot[i][1]', dataToPlot[i][0], dataToPlot[i][1])
    lineiMatplotlib = ax_1[0].plot(dataToPlot[i][0], dataToPlot[i][1], label=entryNames[i], color=next(colors), marker='.')
    # print('lineiData', lineiData)
    allplotsMatplotlib.append(lineiMatplotlib)
    # add 'color, entry i' box in left panel
    ax_1[0].legend(loc='best', fontsize='small')


### plot original data in ax_1[0] end ###


### check buttons to make visible/not visible in fig_1 ax_1[1] ###

# crate list of labels
labels = []
for i in range(len(dataToPlot)):
    label = sampleName + '_' + entryNames[i]
    labels.append(label)


# make check box inside panel 2 (location 2 in nrows=1, ncols=2)
rax = ax_1[1]

rax.set_title('List of data')

activated = []
for i in range(len(dataToPlot)):
    activated.append(True)

chxbox = CheckButtons(rax, labels, activated)

# function to go in for check box
def set_visible(label):
    index = labels.index(label)
    allplotsMatplotlib[index][0].set_visible(not allplotsMatplotlib[index][0].get_visible())
    # update legend and do not show the lines not checked on box (label still exists)
    ax_1[0].legend(loc='best', fontsize='small')

    plt.draw()

chxbox.on_clicked(set_visible)

### check buttons to make visible/not visible in ax_1[1] end ###


### error bar plot part ####
# get_visible function does not handle error bar that is in Artist.
# show/no show with error bar is handled by re-plotting the selected entry

fig_2, ax_2 = plt.subplots()
ax_2.set_title('Qz vs. Intensity (error bar)')
ax_2.set_xlabel('Qz ')
ax_2.set_ylabel('Intensity ')

# text box location
textBoxLocation = fig_2.add_axes([0.2, 0.94, 0.1, 0.05])
textBox = TextBox(textBoxLocation, 'selected number' )
# !!! make sure input has comma after number for single entry !!! #
ax_2.text(0,1, 'type comma after a number to show one data only')

def submit(expression):
    ax_2.clear()
    # redefine axes settings
    ax_2.set_title('Qz vs. Intensity (error bar)')
    ax_2.set_xlabel('Qz ')
    ax_2.set_ylabel('Intensity ')
    ax_2.semilogy()
    # text inside axis goes away with clear ()
    ax_2.text(0, 1, 'type comma after a number to show one data only')

    selectedEntry = list(eval(expression))

    # select entry number tped in the box
    for i in range(len(selectedEntry)):
        ax_2.errorbar(dataToPlot[selectedEntry[i]][0], dataToPlot[selectedEntry[i]][1], label='entry' + str(selectedEntry[i]), yerr=dataToPlot[selectedEntry[i]][2], color=next(colors))
        ax_2.legend(loc='best')

    plt.draw()

textBox.on_submit(submit)

### error bar plot part  end####


### residuals plot part ####
fig_3, ax_3 = plt.subplots(nrows=2, ncols=1)
# fig_3, ax_3 = plt.subplots()
entryForResidualsLocation = fig_3.add_axes([0.3, 0.9, 0.05, 0.05])

entryForResiduals = TextBox(entryForResidualsLocation, 'entry two numbers to compare')
# ax_3.set_title('Qz vs. Residual')
# ax_3.set_xlabel('Qz ')
# ax_3.set_ylabel('Residual: 2(S1-S2)/(E1 + E2)', color='r')

ax_3[0].set_title('Qz vs. Residual')
ax_3[0].set_xlabel('Qz ')
ax_3[0].set_ylabel('Residual: 2(S1-S2)/(E1 + E2)', color='r')
# ax_3_2 = ax_3.twinx()
# ax_3_2.tick_params(axis='y', labelcolor='b')
# ax_3_2.set_ylabel('Relative Differences', color='b')
ax_3[1].tick_params(axis='y', labelcolor='b')
ax_3[1].set_ylabel('Relative Differences', color='b')
### make sure input has comma after number for single entry ###
ax_3[0].text(0,1, 'format: #1, #2')

# define calcuation process after box entry
def getEntryNumber(expression):
    ax_3[0].clear()
    ax_3[1].clear()
    # ax_3_2 = ax_3.twinx()
    # ax_3_2.clear()
    # ax_3.set_title('Qz vs. Residual')
    # ax_3.set_xlabel('Qz ')
    # ax_3.text(0, 1, 'format: #1, #2')

    entryNumberForResidual = list(eval(expression))

    residualsList = []
    relativeDifferencesList = []

    # len(dataList[a]) is number of rows in each entry

    # dataToPlot format : [[[entry1 "Qz"][entry1 "Intensity"][entry1 "uncertainty"]][[entry2 "Qz"]....]...]
    for a in range(len(dataToPlot[entryNumberForResidual[0]][0])):
        # 2(S1-S2)/(E1+E2)  where S is specular intensity and E is Undertainty
        S1 = dataToPlot[entryNumberForResidual[0]][1][a]
        S2 = dataToPlot[entryNumberForResidual[1]][1][a]
        E1 = dataToPlot[entryNumberForResidual[0]][2][a]
        E2 = dataToPlot[entryNumberForResidual[1]][2][a]

        try:
            residual = 2 * (S1 - S2) / (E1 + E2)
            relativeDifference = 2 * (S1 - S2) / (S1 + S2)
            residualsList.append(residual)
            relativeDifferencesList.append(relativeDifference)
        except:
            # if E1+E2 = 0 or S1+S2 = 0, cannot be divided by 0. Put 0 in list since there is no difference.
            residualsList.append(0)
            relativeDifferencesList.append(0)

    ## calculation checked with first and last of 3-4 rows of data set##

    # ax_3.set_ylabel('Residual:2(S1-S2)/(E1+E2)', color = 'r')
    # ax_3.tick_params(axis='y', labelcolor='r')
    # # residualsPlot
    # ax_3.plot(dataToPlot[entryNumberForResidual[0]][0], residualsList, color='r', linewidth=0.5)

    ax_3[0].set_ylabel('Residual:2(S1-S2)/(E1+E2)', color = 'r')
    ax_3[0].tick_params(axis='y', labelcolor='r')
    # residualsPlot
    ax_3[0].plot(dataToPlot[entryNumberForResidual[0]][0], residualsList, color='r', linewidth=0.5)

    #
    # ax_3_2.set_ylabel('Relative Differences', color='b')
    # # # relativeDifferencesPlot
    # ax_3_2.plot(dataToPlot[entryNumberForResidual[0]][0], relativeDifferencesList, color='b', linewidth=0.5)
    # ax_3_2.tick_params(axis='y', labelcolor='b')

    ax_3[1].set_ylabel('Relative Differences', color='b')
    # # relativeDifferencesPlot
    ax_3[1].plot(dataToPlot[entryNumberForResidual[0]][0], relativeDifferencesList, color='b', linewidth=0.5)
    ax_3[1].tick_params(axis='y', labelcolor='b')

    plt.draw()

entryForResiduals.on_submit(getEntryNumber)

### residuals plot part end ####

### combine data and plot part ###

fig_4, ax_4 = plt.subplots()

entryForCombineDataLocation = fig_4.add_axes([0.8, 0.9, 0.05, 0.05])
entryForCombineData = TextBox(entryForCombineDataLocation, 'combine data')

ax_4.text(0,1, 'format: #1, #2')

ax_4.set_title('combine data')
ax_4.set_xlabel('Qz')
ax_4.set_ylabel('intensity')
ax_4.semilogy()

def combineData(expression):
    ax_4.clear()
    # entry must be only two selected data (list length must be 2 to make inside for-loop work
    entryNumberForCombineData = list(eval(expression))

    # check how many data to combine (take length of list entered in a box)
    numberOfDataToCombine = len(entryNumberForCombineData)

    # create empty list to put in combined data
    combinedIntensityList = []
    combinedErrorList = []

    dataToCombine = []
    for n in range(numberOfDataToCombine):
        intOfOeDataSet = dataToPlot[entryNumberForCombineData[n]][1]
        dataToCombine.append(intOfOeDataSet)
    # taking the right data set, checked by first and last couple of intensity columns of selected data

    # take length of Qz column len(dataToPlot[entryNumberForCombineData[0]][0]), should be the same uf u take other columns
    # for loop appears to be working. entry1+entry2 in previous code with individualCombinedData = (S1+S2)/2 match with current code
    for a in range(len(dataToPlot[entryNumberForCombineData[0]][0])):

        # TODO change to correct equation for combining data
        sumData = 0
        for n in range(numberOfDataToCombine):
            # combine the values in the same row
            oneData = dataToPlot[entryNumberForCombineData[n]][1][a]
            sumData = float(sumData) + float(oneData)

        # combine n number of data points and divide by n
        indivisualCombinedIntensity = sumData/numberOfDataToCombine

        combinedIntensityList.append(indivisualCombinedIntensity)

        # E(combined) = Average E / SQRT(N)
        # yerr = dataToPlot[selectedEntry[i]][2]
        sumError = 0
        for n in range(numberOfDataToCombine):
            oneError = dataToPlot[entryNumberForCombineData[n]][2][a]
            sumError = float(sumError) + float(oneError)

        individualCombinedError = float(sumError)/np.sqrt(numberOfDataToCombine)
        combinedErrorList.append(individualCombinedError)
    print('combinedErrorList', combinedErrorList)


    # set aces label and semi log scale for y
    ax_4.set_xlabel('Qz')
    ax_4.set_ylabel('Intensity')
    ax_4.semilogy()

    # x axis : Qz = dataToPlot[entryNumberForCombineData[0]][0]
    # y axis : combined intensity = combinedDataList
    combinedDataPlot = ax_4.errorbar(dataToPlot[entryNumberForCombineData[0]][0], combinedIntensityList,yerr=combinedErrorList, color='k', marker='.')

    # put Qz and combined intensity in one list
    combinedQzIntErrList = []
    for a in range(len(dataToPlot[entryNumberForCombineData[0]][0])):
        # text format: str(Qz) + (space) + str(Intensity)
        oneLine= str(dataToPlot[entryNumberForCombineData[0]][0][a]) + ' ' + str(combinedIntensityList[a]) + ' ' + str(combinedErrorList[a])
        print('oneLine', oneLine)
        combinedQzIntErrList.append(oneLine)

    # create a folder  for combined data text if it doesn't exist
    # parentDirectory defined at the top
    folderName = sampleName + '_Combined'
    path = os.path.join(parentDirectory, folderName)
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)
        pass
    # make folder directory
    folderDirectory = parentDirectory + '/' + folderName + '/'


    # combined entry names
    n = 0
    combinedEntryNames = '_entry'
    # for two dataset entry, range is range(2), takes position 0 ~ 2.
    for n in range(numberOfDataToCombine):
        if n < numberOfDataToCombine-1:
            # append data entry number after '_entry' with comma
            combinedEntryNames = combinedEntryNames + str(entryNumberForCombineData[n]) + ','
        elif n == numberOfDataToCombine-1:
            # append number without comma for the end of the entry number
            combinedEntryNames = combinedEntryNames + str(entryNumberForCombineData[n])


    # export combnied data into text file
    textFileName = folderDirectory + sampleName + combinedEntryNames +'.txt'
    f = open(textFileName, "a+")
    # 'w+' overwrites previous data? "Date modified" time gets updated"

    # take each line in list and put into txt
    for element in combinedQzIntErrList:
        f.write(element)
        f.write('\n')

    f.close

    plt.draw()

entryForCombineData.on_submit(combineData)

### combine data and plot part end ###

plt.show()