# http://matplotlib.org/1.5.1/examples/pylab_examples/scatter_symbol.html
from matplotlib import pyplot as plt
import numpy as np
import matplotlib

input_data = np.recfromcsv('./files/minimal.csv')
x = np.arange(0.0, 3.0)
y = x ** 1.3 + np.random.rand(*x.shape) * 30.0
s = [idata[0] for idata in input_data]
labels = [idata[1] for idata in input_data]

plt.scatter(x, y, s, alpha=0.5, marker="o", label="bubbles")

# http://matplotlib.org/examples/shapes_and_collections/artist_reference.html
def label(xy, text):
    y = xy[1] - 0.15  # shift y-value for label so that it's below the artist
    plt.text(xy[0], y, text, ha="center", family='sans-serif', size=14)

plt.xlabel("Leprechauns")
plt.ylabel("Gold")
plt.legend(loc=2)
for (x, y) in zip(x, y):
    label((x, y), labels.pop())

plt.show()
