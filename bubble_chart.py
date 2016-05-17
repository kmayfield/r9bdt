# http://matplotlib.org/1.5.1/examples/pylab_examples/scatter_symbol.html
# http://www.optimization-online.org/DB_FILE/2008/06/1999.pdf
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
from copy import deepcopy
import math
from examples.circles import positionCircles
from examples.CirclePack import CirclePack
from unittest import TestCase
from argparse import ArgumentParser
import os
import networkx as nx


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


def calculate_coordinates(radii):
    """Uses Descartes' algorithm to place the circles.  This only works for
    fractal operations where the know radii are the same size and all filler
    circles use radii based on the uniform center circles.  Not useful for this
    project, but an interesting foray into gasket theory."""
    x = deepcopy(radii[:2])
    for idx, xval in enumerate(x):
        if idx % 2 != 0:
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
    centers = [complex(0), complex(x[0]), complex(x[1])]
    print "centers", centers
    # bends = inv(centers)
    bends = [float(1/float(xval)) for xval in tmp_radii]
    print "bends", bends
    # bends x centers
    bends_x_centers = map(lambda aval, bval: aval * complex(bval),
                          centers, bends[:-1])
    print "bends_x_centers", bends_x_centers
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
    # left = (-1 * (2 * bends_x_centers_sum * D)) + D^2
    left *= -1
    print "left", left
    if left.real < 0 or left.imag < 0:
        tmp = left * -1
        left = math.sqrt(tmp.real) * -1
    left = left / bends[-1]
    new_coord = complex(left)
    x.append(0)
    y.append(new_coord.real)
#     x.append(new_coord.real)
#     y.append(int(new_coord.imag))
#     return(new_coord.real, int(new_coord.imag))
    return (x, y)


# python -m unittest bubble_chart.TestImplementations or by test name as
# python -m unittest bubble_chart.TestImplementations.test_minimal_mine for ex.
class TestImplementations(TestCase):
    def get_minimal_data(self):
        file_name = './files/minimal.csv'
        input_data = np.recfromcsv(file_name).tolist()
        input_data.sort(reverse=True)
        radii = [idata[0] for idata in input_data]  # load the radii
        labels = [idata[1] for idata in input_data]  # load the labels
        return file_name, radii, labels

    def gen_large_data(self):
        from random import randint, SystemRandom
        import string
        with open('./files/LargeRandomSet2.csv', 'w+') as fd:
            for _ in xrange(400):
                fd.write('%d, %s\n' % (randint(1,500),
                ''.join(SystemRandom().choice(string.uppercase +
                             string.digits) for _ in range(6))))

    def get_large_data(self):
        file_name = './files/LargeRandomSet2.csv'
        input_data = np.recfromcsv(file_name).tolist()
        input_data.sort(reverse=True)
        radii = [idata[0] for idata in input_data]  # load the radii
        labels = [idata[1] for idata in input_data]  # load the labels
        return file_name, radii, labels

    def test_minimal_mine(self):
        file_name, radii, labels = self.get_minimal_data()
        (figure, axes) = plt.subplots(figsize=(10,10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0],
                     fontsize=28)
#         x = [radii[0]]
#         y = [0.0]
#         x1, y1 = calculate_coordinates(radii[:2])
#         x2, y2 = calculate_coordinates(radii[1:3])
#         x.append(x1)
#         x.append(x2)
#         y.append(y1)
#         y.append(y2)
        x, y = calculate_coordinates(radii)
        print "x", x, "y", y
        axes.scatter(x, y, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, x, y, radii, labels)
        plt.show()

    def test_minimal_circles(self):
        """This brute force search algorithm works ok on small sets."""
        file_name, radii, labels = self.get_minimal_data()
        (figure, axes) = plt.subplots(figsize=(10,10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0],
                     fontsize=28)
        circles = positionCircles(radii)
        print circles
        x = [aval for aval, bval, cval in circles]
        y = [bval for aval, bval, cval in circles]
        axes.scatter(x, y, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, x, y, radii, labels)
        plt.show()

    def test_large_circles(self):
        """This brute force search algorithm really tanks on large sets."""
        file_name, radii, labels = self.get_large_data()
        (figure, axes) = plt.subplots(figsize=(10,10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0],
                     fontsize=28)
        circles = positionCircles(radii)
        print circles
        x = [aval for aval, bval, cval in circles]
        y = [bval for aval, bval, cval in circles]
        axes.scatter(x, y, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, x, y, radii, labels)
        plt.show()

    def test_minimal_circlepack(self):
        filename, radii, labels = self.get_minimal_data()
        (figure, axes) = plt.subplots(figsize=(10,10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0],
                     fontsize=28)
        my_graph = self.test_create_graph(radii, labels)
        internal = dict([(labels[0], my_graph.neighbors(labels[0]))])
        external = dict([(label, radius) for radius, label in zip(radii[1:], labels[1:])])
        print internal
        print external
        circle_pack_data = CirclePack(internal, external)
        x = [aval.real for aval, bval in circle_pack_data.values()]
        y = [aval.imag for aval, bval in circle_pack_data.values()]
        axes.scatter(x, y, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, x, y, radii, labels)
        plt.show()

    def test_large_circlepack(self):
        file_name, radii, labels = self.get_large_data()
        (figure, axes) = plt.subplots(figsize=(10,10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0],
                     fontsize=28)
        my_graph = self.test_create_graph(radii, labels)
        internal = dict([(labels[0], my_graph.neighbors(labels[0]))])
        external = dict([(label, radius) for radius, label in zip(radii[1:], labels[1:])])
        print internal
        print external
        circle_pack_data = CirclePack(internal, external)
        x = [aval.real for aval, bval in circle_pack_data.values()]
        y = [aval.imag for aval, bval in circle_pack_data.values()]
        axes.scatter(x, y, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, x, y, radii, labels)
        plt.show()

    def test_create_graph(self, radii=None, labels=None):
        if radii == None or labels == None:
            radii, labels = self.get_minimal_data()
        my_graph = nx.Graph()
#         my_graph.add_cycle(labels, length=radii)
        my_graph.add_star(labels)
        return my_graph


def main():
    parser = ArgumentParser(description='Plot a set of circles provided ' +
        'a list of radii in column 1 of a comma separated value (CSV).')
    parser.add_argument('file', type=file)
    args = parser.parse_args()
    args.file.close()
    input_data = np.recfromcsv(args.file.name).tolist()
    input_data.sort(reverse=True)
    radii = [idata[0] for idata in input_data]  # load the radii
    labels = [idata[1] for idata in input_data]  # load the labels

    (figure, axes) = plt.subplots(figsize=(10,10))
    axes.set_xlim((-1000, 1000))
    axes.set_ylim((-1000, 1000))
    axes.set_title(os.path.splitext(os.path.basename(args.file.name))[0],
                     fontsize=28)
    circles = positionCircles(radii)
    x = [aval for aval, bval, cval in circles]
    y = [bval for aval, bval, cval in circles]
    axes.scatter(x, y, alpha=0.5, marker="o", label="bubbles")
    draw_circles(axes, x, y, radii, labels)
    plt.show()


if __name__ == '__main__':
    main()