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

    fig_1, ax_1 = plt.subplots(figsize = (8, 4), nrows=1, ncols=3)
    # ax = fig.add_subplot()
    ax_1[0].set_title('Qz vs. Intensity')
    ax_1[0].set_xlabel('Qz')
    ax_1[0].set_ylabel('intensity')
    ax_1[0].ticklabel_format(axis='both', style='scientific')
    ax_1[0].semilogy()


    # plot thw whole entry(0 ~ n) in one plot
    for i, item in enumerate(dataToPlot):
        # TODO label in for loop does not show with check button
        ax_1[0].plot(item[0], item[1], label='entry' + str(i), color=next(colors))
        plt.errorbar(item[0], item[1], yerr=item[2], color=next(colors), barsabove=True)

        # Make checkbuttons with all plotted lines with correct visibility


    # get list of labels
    labels = []
    for i in range(len(dataToPlot)):
        label = 'entry' + str(i)
        labels.append(label)

    # size of check box part
    rax = ax_1[1]
    # visibility = [line.get_visible() for line in dataToPlot[i]]

    # labels read the above list created with for loop
    check = CheckButtons(rax, labels)

    # def func(label):
    #     index = labels.index(label)
    #     labels[index].set_visible(not labels[index].get_visible())
    #     plt.draw()



    plt.legend(loc='best')

    # log scale to check box
    # plt.semilogy()

    plt.show()