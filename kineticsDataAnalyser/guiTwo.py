import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from readRefl1d import ReadRefl1d as rr
from itertools import cycle

class GuiTwo:

    dataInFloat = rr.dataList
    print('after dataList')
    print(type(rr.dataList))
    print('dataInFloat', dataInFloat)
    sampleName = rr.sampleName

    dataToPlot = []
    for a in range(len(dataInFloat)):
        print('a', a)
        qzIntUncertainty = []
        # create list of Qz
        listOfQz= []
        for i in range(len(dataInFloat[a])):
            # print('len(dataInFloat[a])', len(dataInFloat[a]))
            # print('dataInFloat[a][i][0]', dataInFloat[a][i][0])
            # print(type(dataInFloat[a][i][0]))
            listOfQz.append(dataInFloat[a][i][0])
        print('listOfQz', listOfQz)

        listOfInt = []
        for i in range(len(dataInFloat[a])):
            # print('len(rr.dataList[a])', len(rr.dataList[a]))
            # print('rr.dataList[a][i][0]', rr.dataList[a][i][1])
            # print(type(rr.dataList[a][i][1]))
            listOfInt.append(dataInFloat[a][i][1])
        print('listOfInt', listOfInt)

        listOfUncertainty = []
        for i in range(len(dataInFloat[a])):
            # print('len(rr.dataList[a])', len(rr.dataList[a]))
            # print('rr.dataList[a][i][0]', rr.dataList[a][i][2])
            # print(type(rr.dataList[a][i][2]))
            listOfUncertainty.append(dataInFloat[a][i][2])
        print('listOfUncertainty', listOfUncertainty)

        qzIntUncertainty.append(listOfQz)
        qzIntUncertainty.append(listOfInt)
        qzIntUncertainty.append(listOfUncertainty)
        dataToPlot.append(qzIntUncertainty)
    # print('dataToPlot', dataToPlot)

    colors = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])

    fig_1, ax_1 = plt.subplots(figsize = (8, 4), nrows=1, ncols=3)

    # tight layout doesn't seem to change
    plt.tight_layout()

    # ax = fig.add_subplot()
    ax_1[0].set_title('Qz vs. Intensity')
    ax_1[0].set_xlabel('Qz')
    ax_1[0].set_ylabel('intensity')
    ax_1[0].ticklabel_format(axis='both', style='scientific')
    ax_1[0].semilogy()
    plt.legend(loc='best')

    allplots = []
    # plot thw whole entry(0 ~ n) in one plot
    for i in range(len(dataToPlot)):
        # TODO label in for loop does not show with check button
        linei = ax_1[0].plot(dataToPlot[i][0], dataToPlot[i][1], label='entry' + str(i), color=next(colors))
        allplots.append(linei)
        # TODO uplims=True, lowlims=True not working, dodt appears bot not accurate error bar
        errori = ax_1[0].errorbar(dataToPlot[i][0], dataToPlot[i][1], yerr=dataToPlot[i][2], color=next(colors), ms=0.1, mew=1)
        # add 'color, entry i' box in left panel
        # TODO this is not a place where it gets error 'No handles with labels found to put in legend.'
        ax_1[0].legend(loc='best')
    print('allplots', allplots)
    print('type of allplots[0]', type(allplots[0][0]))

    # gets only entry0
    visibility = [line.get_visible() for line in allplots[0]]


    # get list of labels
    labels = []
    for i in range(len(dataToPlot)):
        label = sampleName + '_entry' + str(i)
        labels.append(label)

    # make check box inside panel 2 (location 1 in figsize = (8, 4), nrows=1, ncols=3)
    rax = ax_1[1]

    # visibility = [labels.get_visible() for line in labels]

    # labels read the above list created with for loop
    check = CheckButtons(rax, labels, visibility)
    # check.label.set_fontsize(10)

    # def func(label):
    #     index = labels.index(label)
    #     labels[index].set_visible(not labels[index].get_visible())
    #     plt.draw()





    plt.show()