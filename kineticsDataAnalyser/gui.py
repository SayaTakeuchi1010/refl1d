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
fig_1 = plt.figure(figsize=(5, 4))
axes_1 = fig_1.add_axes([0.2, 0.2, 0.6, 0.6])
axes_1.set_xlabel('Qz')
axes_1.set_ylabel('intensity')
plt.ticklabel_format(axis='both', style = 'scientific' )
axes_1.plot(qz_0, int_0, label='entry0')
axes_1.plot(qz_1, int_1, label='entry1')
axes_1.legend(loc=4)


fig, ax = plt.subplots()
ax.set_xlabel('Qz')
ax.set_ylabel('intensity')
plt.ticklabel_format(axis='both', style='scientific' )

l0, = ax.plot(qz_0, int_0, lw=2, color='b', marker='.', label='entry0')
l1, = ax.plot(qz_1, int_1, lw=2, color='r', marker='.', label='entry1')
plt.legend(loc=4)
# l2, = ax.plot(t, s2, lw=2, color='g', label='6 Hz')
# plt.subplots_adjust(left=0.2)
#
lines = [l0, l1]

# Make checkbuttons with all plotted lines with correct visibility
rax = plt.axes([0.9, 0.2, 0.1, 0.15])
labels = [str(line.get_label()) for line in lines]
visibility = [line.get_visible() for line in lines]
check = CheckButtons(rax, labels, visibility)


def func(label):
    index = labels.index(label)
    lines[index].set_visible(not lines[index].get_visible())
    plt.draw()

check.on_clicked(func)

plt.show()