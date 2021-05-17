import tkinter as tk
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from readRefl1d import ReadRefl1d as rr
from itertools import cycle
import numpy as np
from matplotlib.ticker import MaxNLocator

### CHANGE DIRECTORY HERE ###
parentDirectory = 'C:/Users/saya6/Documents/NCNR/kineticsDataAnalizer'


# get list from readRefl1d
dataInFloat = rr.dataList
sampleName = rr.sampleName

# get list of original data labels
originalDataLabels = []
for i in range(len(dataInFloat)):
    label = sampleName + '_entry' + str(i)
    originalDataLabels.append(label)

# get list of combined data labels

folderName = sampleName + '_Combined'
folderDirectory = parentDirectory + '/' + folderName + '/'
# read list of combined data in combine data folder
combinedDataLabels = os.listdir(folderDirectory)

allDataList = []
# append list of original data to empty list
for i in range(len(originalDataLabels)):
    allDataList.append(originalDataLabels[i])
# append combined data list after original data
for i in range(len(combinedDataLabels)):
    allDataList.append(combinedDataLabels[i])

tkMaster = tk.Tk()
scrollbar = tk.Scrollbar(tkMaster, orient="vertical")
lb = tk.Listbox(tkMaster, width=50, height=20, yscrollcommand=scrollbar.set)

scrollbar.config(command=lb.yview)
tkMaster.title('List of data selection')

scrollbar.pack(side="right", fill="y")
lb.pack(side="left",fill="both", expand=True)

lb.insert(0, 'number to select data : data set name')
for i in range(len(allDataList)):
    lb.insert(str(i+2), str(i) + ' : ' + allDataList[i])


### tk inter part end ###


### matplotlib part ###

# TODO make it in waterfall plot

originalAndCombinedData = []
for a in range(len(dataInFloat)):
    qzInt = []
    # create list of Qz
    listOfQz = []
    for i in range(len(dataInFloat[a])):
        listOfQz.append(dataInFloat[a][i][0])

    listOfInt = []
    for i in range(len(dataInFloat[a])):
        listOfInt.append(dataInFloat[a][i][1])

    qzInt.append(listOfQz)
    qzInt.append(listOfInt)
    originalAndCombinedData.append(qzInt)

# append combined data set to originalAndCombinedData
oneDataSet = []
# read number of data set in _combined folder
for i in range(len(combinedDataLabels)):
    filePath = folderDirectory + '/' + combinedDataLabels[i]
    text = open(filePath, 'r')
    fullText = [line.split(' ') for line in text.readlines()]
    oneRowInFloat = []
    # read one line each to convert string to float
    for a in range(len(fullText)):
        # print('fullText[a]', fullText[a])
        oneDataInFloat = []
        for b in range(2):
            oneData = float(fullText[a][b])
            oneDataInFloat.append(oneData)
        oneRowInFloat.append(oneDataInFloat)

    oneDataSet.append(oneRowInFloat)
# number of appended data set was correct

### TODO this is duplicate of a method ###
for a in range(len(oneDataSet)):
    qzInt = []
    # create list of Qz
    listOfQz = []
    for i in range(len(oneDataSet[a])):
        listOfQz.append(oneDataSet[a][i][0])

    listOfInt = []
    for i in range(len(oneDataSet[a])):
        listOfInt.append(oneDataSet[a][i][1])

    qzInt.append(listOfQz)
    qzInt.append(listOfInt)
    originalAndCombinedData.append(qzInt)


fig=plt.figure()
ax=plt.axes(projection='3d')
ax.set_title('Qz vs. Intensity')
ax.set_xlabel('Qz')
ax.set_zlabel('intensity')
ax.ticklabel_format(axis='both', style='scientific')
# 3D does not support semilog scale
# ax.semilogz()
ax.set_ylabel('fileName')
# set integer only for y axis tick
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

textBoxLocation = fig.add_axes([0.3, 0.9, 0.1, 0.05])
### make sure input has comma after number for single entry ###
dataNumberToPlot = TextBox(textBoxLocation, 'select number from data list')


fig_2, ax_2= plt.subplots()

ax_2.set_title('Qz vs. Intensity')
ax_2.set_xlabel('Qz')
ax_2.set_ylabel('intensity')
ax_2.ticklabel_format(axis='both', style='scientific')
ax_2.semilogy()
# below line works to show line
# ax_2.plot(originalAndCombinedData[1][0], originalAndCombinedData[1][1], label=allDataList[1], color='k',marker='.')
# ax_2.legend(loc='best', fontsize='small')

def getEntryNumber(expression):
    ax.clear()
    ax.set_title('Qz vs. Intensity')
    ax.set_xlabel('Qz ')
    ax.set_zlabel('intensity(log)')
    # ax.semilogy()
    ax.set_ylabel('entered position in text box')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    enteredNumberToPlot = list(eval(expression))

    colors = cycle(
        ["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red",
         "silver", "teal", "yellow"])
    # # plot 2D figure
    # ax_2.clear()
    ax_2.set_xlabel('Qz ')
    ax_2.set_ylabel('intensity(log)')
    for a in range(len(enteredNumberToPlot)):
        lineiData = ax_2.plot(originalAndCombinedData[enteredNumberToPlot[a]][0], originalAndCombinedData[enteredNumberToPlot[a]][1], label=allDataList[enteredNumberToPlot[a]], color=next(colors),marker='.')
        ax_2.legend(loc='best', fontsize='small')
    plt.draw()


    for a in range(len(enteredNumberToPlot)):

        x = originalAndCombinedData[enteredNumberToPlot[a]][0]
        # 3D axes currently only support linear scales
        y = np.log(originalAndCombinedData[enteredNumberToPlot[a]][1])

        # set length of z to be the same as x and y to be able to plot
        listForZ = []
        for b in range(len(originalAndCombinedData[enteredNumberToPlot[a]][0])):
            # cannot take string (file name) for ax
            listForZ.append(a)

        z = listForZ

        ax.plot3D(x,z,y,label=allDataList[enteredNumberToPlot[a]])
        ax.legend(loc='best', fontsize='small')




    plt.draw()

dataNumberToPlot.on_submit(getEntryNumber)


plt.show()

tkMaster.mainloop()