import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from readRefl1d import ReadRefl1d as rr
from itertools import cycle

class GuiTwo:
    text = rr.dataList
    sampleName = rr.sampleName

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

    fig_1, ax_1 = plt.subplots(figsize = (8, 4), nrows=1, ncols=3)
    # ax = fig.add_subplot()
    ax_1[0].set_title('Qz vs. Intensity')
    ax_1[0].set_xlabel('Qz')
    ax_1[0].set_ylabel('intensity')
    ax_1[0].ticklabel_format(axis='both', style='scientific')
    ax_1[0].semilogy()
    plt.legend(loc='best')


    # plot thw whole entry(0 ~ n) in one plot
    for i, item in enumerate(dataToPlot):
        # TODO label in for loop does not show with check button
        ax_1[0].plot(item[0], item[1], label='entry' + str(i), color=next(colors))
        # TODO uplims=True, lowlims=True not working, dodt appears bot not accurate error bar
        ax_1[0].errorbar(item[0], item[1], yerr=item[2], color=next(colors), ms=0.1, mew=1)
        # add 'color, entry i' box in left panel
        # TODO this is not a place where it gets error 'No handles with labels found to put in legend.'
        ax_1[0].legend(loc='best')


    # get list of labels
    labels = []
    for i in range(len(dataToPlot)):
        label = sampleName + '_entry' + str(i)
        labels.append(label)

    # make check box inside panel 2 (location 1 in figsize = (8, 4), nrows=1, ncols=3)
    rax = ax_1[1]
    # visibility = [labels.get_visible() for line in labels]

    # labels read the above list created with for loop
    check = CheckButtons(rax, labels)

    # def func(label):
    #     index = labels.index(label)
    #     labels[index].set_visible(not labels[index].get_visible())
    #     plt.draw()





    plt.show()