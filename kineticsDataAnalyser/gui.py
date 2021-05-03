import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from readRefl1d import ReadRefl1d as rr

text = rr.dataList
print('text in gui', text)

qz_0 = rr.dataList[0][0]
int_0 = rr.dataList[0][1]
qz_1 = rr.dataList[1][0]
int_1 = rr.dataList[1][1]
fig_QvsI = plt.figure(figsize= (5, 4))
plt.xlabel = ('Qz')
plt.ylabel = ('intensity')
plt.plot(qz_0, int_0, label='entry0')
plt.plot(qz_1, int_1, label='entry1')
plt.legend(loc=4)

#
# t = np.arange(0.0, 2.0, 0.01)
# s0 = np.sin(2*np.pi*t)
# s1 = np.sin(4*np.pi*t)
# s2 = np.sin(6*np.pi*t)
#
# fig, ax = plt.subplots()
# l0, = ax.plot(t, s0, visible=False, lw=2, color='k', label='2 Hz')
# l1, = ax.plot(t, s1, lw=2, color='r', label='4 Hz')
# l2, = ax.plot(t, s2, lw=2, color='g', label='6 Hz')
# plt.subplots_adjust(left=0.2)
#
lines = [l0, l1, l2]

# Make checkbuttons with all plotted lines with correct visibility
rax = plt.axes([0.05, 0.4, 0.1, 0.15])
labels = [str(line.get_label()) for line in lines]
visibility = [line.get_visible() for line in lines]
check = CheckButtons(rax, labels, visibility)


def func(label):
    index = labels.index(label)
    lines[index].set_visible(not lines[index].get_visible())
    plt.draw()

check.on_clicked(func)

plt.show()