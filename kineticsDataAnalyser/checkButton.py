import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import TextBox
from readRefl1d import ReadRefl1d as rr
from itertools import cycle
import math


# get list from readRefl1d
dataInFloat = rr.dataList
sampleName = rr.sampleName

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

fig_1, ax_1 = plt.subplots(nrows=2, ncols=3)
ax_1[0, 0].set_title('Qz vs. Intensity')
ax_1[0, 0].set_xlabel('Qz')
ax_1[0, 0].set_ylabel('intensity')
ax_1[0, 0].ticklabel_format(axis='both', style='scientific')
ax_1[0, 0].semilogy()
plt.legend(loc='best')


allplotsData = []
allplotsErrorbar = []

# plot thw whole entry(0 ~ n) in one plot
for i in range(len(dataToPlot)):
    lineiData = ax_1[0, 0].plot(dataToPlot[i][0], dataToPlot[i][1], label='entry' + str(i), color=next(colors), marker='.')
    # print('lineiData', lineiData)
    allplotsData.append(lineiData)
    # add 'color, entry i' box in left panel
    ax_1[0, 0].legend(loc='best')


# get list of labels
labels = []
for i in range(len(dataToPlot)):
    label = sampleName + '_entry' + str(i)
    labels.append(label)

# make check box inside panel 2 (location 1 in figsize = (8, 4), nrows=1, ncols=3)
rax = ax_1[0, 1]

activated = []
for i in range(len(dataToPlot)):
    activated.append(True)
# print('activated', activated)

chxbox = CheckButtons(rax, labels, activated)

def set_visible(label):
    index = labels.index(label)
    # allplotsData[index][0]: get inside of the list to get <class 'matplotlib.lines.Line2D'>
    # print('allplotsData[index]', allplotsData[index][0])
    # print(type(allplotsData[index][0]))
    allplotsData[index][0].set_visible(not allplotsData[index][0].get_visible())

    ### may need to handle inside the order in artist to deal with error bar ###
    # https://stackoverflow.com/questions/19470104/python-matplotlib-errorbar-legend-picking
    # allplotsErrorbar[index].set_visible(not allplotsErrorbar[index].get_visible())
    plt.draw()

chxbox.on_clicked(set_visible)

textBoxLocation = fig_1.add_axes([0.05, 0.05, 0.05, 0.05])
### make sure input has comma after number for single entry ###
textBox = TextBox(textBoxLocation, 'input')

def submit(expression):
    ax_1[1, 0].clear()
    selectedEntry = list(eval(expression))
    print('selectedEntry', selectedEntry)
    print(type(selectedEntry))

    selectedPlotsData = []
    for i in range(len(selectedEntry)):
        print('i in submit for loop', i)
        print('selectedEntry[i]', selectedEntry[i])
        erroriData = ax_1[1, 0].errorbar(dataToPlot[selectedEntry[i]][0], dataToPlot[selectedEntry[i]][1], label='entry' + str(selectedEntry[i]), yerr=dataToPlot[selectedEntry[i]][2], color=next(colors))
        selectedPlotsData.append(erroriData)
        ax_1[1, 0].legend(loc='best')

    ax_1[1, 0].set_title('Qz vs. Intensity (error bar)')
    ax_1[1, 0].set_xlabel('Qz ')
    ax_1[1, 0].set_ylabel('intensity ')
    # error below
    # ax_1[1, 0].ticklabel_format(axis='both', style='scientific')
    ax_1[1, 0].semilogy()
    # ax_1[1, 0].autoscale_view()

    # below does not work
    plt.draw()

textBox.on_submit(submit)


# show residual plot
entryForResidualsLocation = fig_1.add_axes([0.5, 0.05, 0.05, 0.05])
### make sure input has comma after number for single entry ###
entryForResiduals = TextBox(entryForResidualsLocation, 'selected entry number')
ax_1[1, 1].set_title('Qz vs. Residual')
ax_1[1, 1].set_xlabel('Qz ')
ax_1[1, 1].set_ylabel('Residual: 2(S1-S2)/(E1 + E2)')

# ntryNumberForResidualList = []
def getEntryNumber(expression):
    ax_1[1, 1].clear()
    ax_1[1, 1].set_title('Qz vs. Residual')
    ax_1[1, 1].set_xlabel('Qz ')

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

        # print('S1, S2, E1, E2', S1, S2, E1, E2)

        try:
            residual = 2 * (S1 - S2) / (E1 + E2)
            relativeDifference = 2 * (S1 - S2) / (S1 + S2)
            residualsList.append(residual)
            relativeDifferencesList.append(relativeDifference)
        except:
            # if E1+E2 = 0 or S1+S2 = 0
            residualsList.append(0)
            relativeDifferencesList.append(0)


    # print('residualsList', residualsList)
    # print('relativeDifferencesList', relativeDifferencesList)

    ax_1[1, 1].set_ylabel('Residual:2(S1-S2)/(E1+E2)', color = 'r')
    ax_1[1, 1].tick_params(axis='y', labelcolor='r')
    residuals = ax_1[1, 1].plot(dataToPlot[entryNumberForResidual[0]][0], residualsList, label='Residual',color='r', marker='.')
    # ax_1[1, 1].legend(loc='best')

    #ax_1.tick_params(axis='y', labelcolor='r')
    ax2 = ax_1[1, 1].twinx()
    ax2.tick_params(axis='y', labelcolor='b')
    ax2.set_ylabel('Relative Differences', color='b')
    relativeDifferences = ax2.plot(dataToPlot[entryNumberForResidual[0]][0], relativeDifferencesList, label='relativeDifferences',color='b', marker='.')
    # ax2.legend(loc='best')
    #ax2.legend(loc='best')
    print('residual plot before draw')

    plt.draw()


entryForResiduals.on_submit(getEntryNumber)


plt.show()