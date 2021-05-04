import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from readRefl1d import ReadRefl1d as rr
from itertools import cycle

class GuiTwo:
    text = rr.dataList

    dataToPlot = []
    for a in range(len(rr.dataList)):
        print('a', a)
        qzIntUncertainty = []
        # create list of Qz
        listOfQz= []
        for i in range(len(rr.dataList[a])):
            # print('len(rr.dataList[a])', len(rr.dataList[a]))
            # print('rr.dataList[a][i][0]', rr.dataList[a][i][0])
            # print(type(rr.dataList[a][i][0]))
            listOfQz.append(rr.dataList[a][i][0])
        print('listOfQz', listOfQz)

        listOfInt = []
        for i in range(len(rr.dataList[a])):
            # print('len(rr.dataList[a])', len(rr.dataList[a]))
            # print('rr.dataList[a][i][0]', rr.dataList[a][i][1])
            # print(type(rr.dataList[a][i][1]))
            listOfInt.append(rr.dataList[a][i][1])
        print('listOfInt', listOfInt)

        listOfUncertainty = []
        for i in range(len(rr.dataList[a])):
            # print('len(rr.dataList[a])', len(rr.dataList[a]))
            # print('rr.dataList[a][i][0]', rr.dataList[a][i][2])
            # print(type(rr.dataList[a][i][2]))
            listOfUncertainty.append(rr.dataList[a][i][2])
        print('listOfUncertainty', listOfUncertainty)

        qzIntUncertainty.append(listOfQz)
        qzIntUncertainty.append(listOfInt)
        qzIntUncertainty.append(listOfUncertainty)

        dataToPlot.append(qzIntUncertainty)
    # print('dataToPlot', dataToPlot)

    colors = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])

    fig = plt.figure()
    ax = fig.add_subplot()

    ax.set_xlabel('Qz')
    ax.set_ylabel('intensity')
    plt.ticklabel_format(axis='both', style='scientific')


    for i, item in enumerate(dataToPlot):
        # TODO label in for loop does not show with check button
        ax.plot(item[0], item[1], label='entry' + str(i), color=next(colors))
        plt.errorbar(item[0], item[1], yerr=item[2], color=next(colors), barsabove=True)

        # Make checkbuttons with all plotted lines with correct visibility


    # get list of labels
    labels = []
    for i in range(len(dataToPlot)):
        label = 'entry' + str(i)
        labels.append(label)

    # isibility = [line.get_visible() for line in dataToPlot[i]]

    # size of check box part
    rax = plt.axes([0.8, 0.2, 0.2, 0.5])

    check = CheckButtons(rax, labels)

    def func(label):
        index = labels.index(label)
        dataToPlot[index].set_visible(not dataToPlot[index].get_visible())
        plt.draw()



    plt.legend(loc='best')

    plt.show()