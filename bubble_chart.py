# http://matplotlib.org/1.5.1/examples/pylab_examples/scatter_symbol.html
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
from copy import deepcopy
from math import sqrt


def calculate_coordinates(radii):
    x = deepcopy(radii[:2])
    for idx, xval in enumerate(x):
        if idx % 2 == 0:
            x[idx] = -x[idx]
    y = [0.0] * 2

    if len(radii) <= 2:
        return (x, y)

    # http://techbus.safaribooksonline.com/book/math/9781400839544/
    # a-tisket-a-tasket-an-apollonian-gasket/subhead_49?uicode=dodairforce
    outerRadius = (radii[0] + radii[1])
    tmp_radii = [outerRadius, radii[0], radii[1], radii[2]]
    print "tmp_radii", tmp_radii
    # centers -- solving for center #4
    centers = [0, x[0], x[1]]
    print "centers", centers
    # bends = inv(centers)
    bends = [float(1/float(xval)) for xval in tmp_radii]
    print "bends", bends
    # bends x centers
    bends_x_centers = map(lambda aval, bval: float(aval * bval),
                          centers, bends[:3])
    print bends_x_centers
    # A^2 + B^2 + C^2 + D^2 = 1/2(A + B + C + D)^2
    bends_x_centers_sqr_sum = sum([(xval * xval) * 2
                                   for xval in bends_x_centers])
    print bends_x_centers_sqr_sum
    bends_x_centers_sum = sum(bends_x_centers)
    print bends_x_centers_sum
    # bends_x_centers_sqr_sum + 2D^2 = (bends_x_centers_sum + D)^2
    # bends_x_centers_sqr_sum + 2D^2 = bends_x_centers_sum ^2 + 2 x bends_x_centers_sum x D + D^2
    # bends_x_centers_sqr_sum - bends_x_centers_sum ^ 2 = 2 x bends_x_centers_sum x D - D^2
    left = bends_x_centers_sqr_sum - (bends_x_centers_sum * bends_x_centers_sum)
    left = sqrt(left)
    left *= -1
    y.append((left / bends[3]))
    x.append(0)
#     for idx, yval in enumerate(y):
#         if idx == 0 or idx == 1:
#             continue
#         y[idx] = 2 / (bends[idx])
#         if (idx) % 2 == 0:
#             y[idx] *= -1
    print x, '\n', y, '\n', centers
    return(x, y)

def draw_circles(axes, x, y, radii, labels):
    # http://techbus.safaribooksonline.com/book/programming/python/
    # 9781783987542/the-custom-zeromq-cluster/ch09lvl2sec70_html?
    # uicode=dodairforce
    for (xval, yval, sval, lval) in zip(x, y, radii, labels):
        print xval, yval, sval, lval
        circle = plt.Circle((xval, yval), sval, fill=True)
        label(plt, (xval, yval), lval)
        axes.add_artist(circle)


# http://matplotlib.org/examples/shapes_and_collections/artist_reference.html
def label(plt, xy, text):
    y = xy[1] - 0.15  # shift y-value for label so that it's below the artist
    plt.text(xy[0], y, text, ha="center", family='sans-serif', size=14)


def main():
    input_data = np.recfromcsv('./files/minimal.csv').tolist()
    input_data.sort(reverse=True)
    radii = [idata[0] for idata in input_data]  # load the diameters into s
    labels = [idata[1] for idata in input_data]  # load the labels

    (figure, axes) = plt.subplots(figsize=(10,10))
    axes.set_xlim((-1000, 1000))
    axes.set_ylim((-1000, 1000))
    axes.set_title("Visualization of Things", 
                   fontsize=28)

    x, y = calculate_coordinates(radii)
    axes.scatter(x, y, alpha=0.5, marker="o", label="bubbles")
    draw_circles(axes, x, y, radii, labels)
    plt.show()


if __name__ == '__main__':
    main()