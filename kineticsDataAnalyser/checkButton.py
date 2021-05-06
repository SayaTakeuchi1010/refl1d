import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
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

fig_1, ax_1 = plt.subplots(figsize = (8, 4), nrows=1, ncols=3)
ax_1[0].set_title('Qz vs. Intensity')
ax_1[0].set_xlabel('Qz')
ax_1[0].set_ylabel('intensity')
ax_1[0].ticklabel_format(axis='both', style='scientific')
ax_1[0].semilogy()
plt.legend(loc='best')

allplotsData = []
allplotsName = []
# plot thw whole entry(0 ~ n) in one plot
for i in range(len(dataToPlot)):
    lineiData = ax_1[0].plot(dataToPlot[i][0], dataToPlot[i][1], label='entry' + str(i), color=next(colors))
    allplotsData.append(lineiData)
    errori = ax_1[0].errorbar(dataToPlot[i][0], dataToPlot[i][1], yerr=dataToPlot[i][2], color=next(colors), ms=0.1,
                              mew=1)
    # add 'color, entry i' box in left panel
    ax_1[0].legend(loc='best')
    # get tuple of line names
    lineiName = 'entry_'+ str(i) + ','
    print('lineiName', lineiName)
    print(type(lineiName))
    allplotsName.append(lineiName)
print('allplotsName', allplotsName)

# get list of labels
labels = []
for i in range(len(dataToPlot)):
    label = sampleName + '_entry' + str(i)
    labels.append(label)

# make check box inside panel 2 (location 1 in figsize = (8, 4), nrows=1, ncols=3)
rax = ax_1[1]

activated = []
for i in range(len(dataToPlot)):
    activated.append(True)
print('activated', activated)

chxbox = CheckButtons(rax, labels, activated)

def set_visible(label):
    index = labels.index(label)
    print('allplotsData[index]', allplotsData[index][0])
    print(type(allplotsData[index][0]))
    allplotsData[index][0].set_visible(not allplotsData[index][0].get_visible())

    plt.draw()

chxbox.on_clicked(set_visible)




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