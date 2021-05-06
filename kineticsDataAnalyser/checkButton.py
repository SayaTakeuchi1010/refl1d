import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import TextBox
from readRefl1d import ReadRefl1d as rr
from itertools import cycle

# get list from readRefl1d
dataInFloat = rr.dataList
sampleName = rr.sampleName

dataToPlot = []
for a in range(len(dataInFloat)):
    print('a', a)
    qzIntUncertainty = []
    # create list of Qz
    listOfQz = []
    for i in range(len(dataInFloat[a])):
        listOfQz.append(dataInFloat[a][i][0])
    print('listOfQz', listOfQz)

    listOfInt = []
    for i in range(len(dataInFloat[a])):
        listOfInt.append(dataInFloat[a][i][1])
    print('listOfInt', listOfInt)

    listOfUncertainty = []
    for i in range(len(dataInFloat[a])):
        listOfUncertainty.append(dataInFloat[a][i][2])
    # print('listOfUncertainty', listOfUncertainty)

    qzIntUncertainty.append(listOfQz)
    qzIntUncertainty.append(listOfInt)
    qzIntUncertainty.append(listOfUncertainty)
    dataToPlot.append(qzIntUncertainty)

colors = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])

fig_1, ax_1 = plt.subplots(figsize = (8, 4), nrows=2, ncols=3)
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
    lineiData = ax_1[0, 0].plot(dataToPlot[i][0], dataToPlot[i][1], label='entry' + str(i), color=next(colors))
    # print('lineiData', lineiData)
    allplotsData.append(lineiData)
    # errori = ax_1[0, 0].errorbar(dataToPlot[i][0], dataToPlot[i][1], label='entry' + str(i), yerr=dataToPlot[i][2], color=next(colors))
    # print('errori', errori)
    # allplotsErrorbar.append(errori)
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
    # print('allplotsErrorbar[index]', allplotsErrorbar[index])
    # print(type(allplotsErrorbar[index]))
    # allplotsErrorbar[index].set_visible(not allplotsErrorbar[index].get_visible())

    plt.draw()

chxbox.on_clicked(set_visible)

textBoxLocation = ax_1[1,1]
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

    ax_1[1, 0].set_xlabel('Qz')
    ax_1[1, 0].set_ylabel('intensity')
    # error below
    # ax_1[1, 0].ticklabel_format(axis='both', style='scientific')
    ax_1[1, 0].semilogy()
    ax_1[1, 0].autoscale_view()
    plt.draw()

textBox.on_submit(submit)


# x = range(0,11)
# y1 = [10]*11
# y2 = [20]*11
# y3 = [30]*11
#
# fig, ax = plt.subplots()
# # these needs to be in tuple
# p1, = ax.plot(x, y1, color='red', label='red')
# p2, = ax.plot(x, y2, color='blue', label='blue')
# p3, = ax.plot(x, y3, color='green', label='green')
# lines =[p1, p2, p3]
#
# labels = ['red', 'blue', 'green']
# activated = [True, True, True]
# axCheckButtons = plt.axes([0.03, 0.4, 0.15, 0.15])
# chxbox = CheckButtons(axCheckButtons, labels, activated)
#
# def set_visible(label):
#     index = labels.index(label)
#     lines[index].set_visible(not lines[index].get_visible())
#     plt.draw()

# chxbox.on_clicked(set_visible)

plt.show()