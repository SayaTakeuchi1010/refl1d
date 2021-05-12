import tkinter as tk
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from readRefl1d import ReadRefl1d as rr
from itertools import cycle


# get list from readRefl1d
dataInFloat = rr.dataList
sampleName = rr.sampleName

#
# # Create our master object to the Application
# master = tk.Tk()
#
# # Create the text widget
# text_widget = tk.Text(master, height=5, width=40)
#
# # Create a scrollbar
# scroll_bar = tk.Scrollbar(master)
#
# # Pack the scroll bar
# # Place it to the right side, using tk.RIGHT
# scroll_bar.pack(side=tk.RIGHT)
#
# # Pack it into our tkinter application
# # Place the text widget to the left side
# text_widget.pack(side=tk.LEFT)
#
# long_text = """This is a multiline string.
# We can write this in multiple lines too!
# Hello from AskPython. This is the third line.
# This is the fourth line. Although the length of the text is longer than
# the width, we can use tkinter's scrollbar to solve this problem!
# """
#
# # Insert text into the text widget
# text_widget.insert(tk.END, long_text)
#
# # Start the mainloop
# tk.mainloop()

# get list of original data labels
originalDataLabels = []
for i in range(len(dataInFloat)):
    label = sampleName + '_entry' + str(i)
    originalDataLabels.append(label)
print('originalDataLabels', originalDataLabels)

# get list of combined data labels
parentDirectory = 'C:/Users/saya6/Documents/NCNR/kineticsDataAnalizer'
folderName = sampleName + '_Combined'
folderDirectory = parentDirectory + '/' + folderName + '/'
# read list of combined data in combine data folder
# path = folderDirectory
combinedDataLabels = os.listdir(folderDirectory)
print('combinedDataLabels', combinedDataLabels)

allDataList = []
# append list of original data to empty list
for i in range(len(originalDataLabels)):
    allDataList.append(originalDataLabels[i])
# append combined data list after original data
for i in range(len(combinedDataLabels)):
    allDataList.append(combinedDataLabels[i])
print('allDataList', allDataList)

tkMaster = tk.Tk()
scrollbar = tk.Scrollbar(tkMaster, orient="vertical")
lb = tk.Listbox(tkMaster, width=50, height=20, yscrollcommand=scrollbar.set)
scrollbar.config(command=lb.yview)

scrollbar.pack(side="right", fill="y")
lb.pack(side="left",fill="both", expand=True)

for i in range(len(allDataList)):
    lb.insert(str(i+1), str(i) + ' : ' + allDataList[i])


### tk inter part end ###


### matplotlib part ###

originalAndCombinedData = []
for a in range(len(dataInFloat)):
    # print('a', a)
    qzInt = []
    # create list of Qz
    listOfQz = []
    for i in range(len(dataInFloat[a])):
        listOfQz.append(dataInFloat[a][i][0])
    # print('listOfQz', listOfQz)

    listOfInt = []
    for i in range(len(dataInFloat[a])):
        listOfInt.append(dataInFloat[a][i][1])
    # print('listOfInt', listOfInt)

    qzInt.append(listOfQz)
    qzInt.append(listOfInt)
    originalAndCombinedData.append(qzInt)
# print('originalAndCombinedData', originalAndCombinedData)




fig_1, ax_1 = plt.subplots()
ax_1.set_title('Qz vs. Intensity')
ax_1.set_xlabel('Qz')
ax_1.set_ylabel('intensity')
ax_1.ticklabel_format(axis='both', style='scientific')
ax_1.semilogy()

textBoxLocation = fig_1.add_axes([0.05, 0.05, 0.05, 0.05])
### make sure input has comma after number for single entry ###
dataNumberToPlot = TextBox(textBoxLocation, 'selected number from data list')

print('after textBox')

def getEntryNumber(expression):
    ax_1.clear()
    ax_1.set_title('Qz vs. Intensity')
    ax_1.set_xlabel('Qz ')
    ax_1.set_ylabel('intensity')
    ax_1.semilogy()

    enteredNumberToPlot = list(eval(expression))

    colors = cycle(
        ["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red",
         "silver", "teal", "yellow"])

    for a in range(len(enteredNumberToPlot)):
        if enteredNumberToPlot[a] <= len(originalAndCombinedData):
            print(enteredNumberToPlot[a])
            print('len(originalAndCombinedData)', len(originalAndCombinedData))
            print('originalAndCombinedData[a][0]', originalAndCombinedData[a][0])
            print('originalAndCombinedData[a][1]', originalAndCombinedData[a][1])
            print('allDataList[a]', allDataList[a])
            lineiData = ax_1.plot(originalAndCombinedData[a][0], originalAndCombinedData[a][1], label=allDataList[enteredNumberToPlot[a]], color=next(colors),
                                    marker='.')
            ax_1.legend(loc='best', fontsize='small')

    # ax_1[1, 1].set_ylabel('Residual:2(S1-S2)/(E1+E2)', color = 'r')
    # ax_1[1, 1].tick_params(axis='y', labelcolor='r')
    # residualsPlot = ax_1[1, 1].plot(dataToPlot[entryNumberForResidual[0]][0], residualsList, color='r', marker='.')

    plt.draw()

dataNumberToPlot.on_submit(getEntryNumber)


plt.show()

tkMaster.mainloop()