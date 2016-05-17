"""The bubble_chart module takes an optional command-line parameter, a
filename, which contains comma-separated values denoting the radius and the
label for a set of circles to plot and display.  The plot should show the
bubbles packed into a tight bunch, with no overlapping circles.  Three
algorithms can be demonstrated with this test script.  None of the three
implement a circle packing algorithm that demonstrates the requested layout
in a robust and efficient manner."""
# http://matplotlib.org/1.5.1/examples/pylab_examples/scatter_symbol.html
# http://www.optimization-online.org/DB_FILE/2008/06/1999.pdf
from matplotlib import pyplot as plt
import numpy as np
from numpy.matrixlib.defmatrix import matrix
from copy import deepcopy
import math
from examples.circles import positionCircles
from examples.CirclePack import CirclePack
from packcircles import iterate_layout
from unittest import TestCase
from argparse import ArgumentParser
import os
import networkx as nx
from random import randint, uniform, SystemRandom
import string


def draw_circles(axes, xar, yar, radii, labels):
    """Helper function to add circles to the plot."""
    # http://techbus.safaribooksonline.com/book/programming/python/
    # 9781783987542/the-custom-zeromq-cluster/ch09lvl2sec70_html?
    # uicode=dodairforce
    for (xval, yval, sval, lval) in zip(xar, yar, radii, labels):
        circle = plt.Circle((xval, yval), sval, fill=True)
        draw_label((xval, yval), lval)
        axes.add_artist(circle)


# http://matplotlib.org/examples/shapes_and_collections/artist_reference.html
def draw_label(xycord, text):
    """Helper function to add text labels to the circles on the plot."""
    yval = xycord[1] - 0.15  # shift y-value for label
    plt.text(xycord[0], yval, text, ha="center", family='sans-serif', size=14)


def calculate_coordinates(radii):
    """Uses Descartes' algorithm to place the circles.  This only works for
    fractal operations where the know radii are the same size and all filler
    circles use radii based on the uniform center circles.  Not useful for this
    project, but an interesting foray into gasket theory."""
    xar = deepcopy(radii[:2])
    for idx, xval in enumerate(xar):
        if idx % 2 != 0:
            xar[idx] = -xar[idx]
    yar = [0.0] * 2

    if len(radii) <= 2:
        return (xar, yar)

    # http://techbus.safaribooksonline.com/book/math/9781400839544/
    # a-tisket-a-tasket-an-apollonian-gasket/subhead_49?uicode=dodairforce
    outer_radius = (radii[0] + radii[1])
    tmp_radii = [outer_radius, radii[0], radii[1], radii[2]]
    # centers -- solving for center #4
    centers = [complex(0), complex(xar[0]), complex(xar[1])]
    # bends = inv(centers)
    bends = [float(1/float(xval)) for xval in tmp_radii]
    # bends x centers
    bends_x_centers = map(lambda aval, bval: aval * complex(bval),
                          centers, bends[:-1])
    # A^2 + B^2 + C^2 + D^2 = 1/2(A + B + C + D)^2
    bends_x_centers_sqr_sum = sum([(xval * xval) * 2
                                   for xval in bends_x_centers])
    bends_x_centers_sum = sum(bends_x_centers)
    # bends_x_centers_sqr_sum + 2D^2 = (bends_x_centers_sum + D)^2
    # bends_x_centers_sqr_sum + 2D^2 =
    #               bends_x_centers_sum ^2 + 2 x bends_x_centers_sum x D + D^2
    # bends_x_centers_sqr_sum - bends_x_centers_sum ^ 2 =
    #               2 x bends_x_centers_sum x D - D^2
    left = bends_x_centers_sqr_sum - (bends_x_centers_sum * bends_x_centers_sum)
    # left = (-1 * (2 * bends_x_centers_sum * D)) + D^2
    left *= -1
    if left.real < 0 or left.imag < 0:
        tmp = left * -1
        left = math.sqrt(tmp.real) * -1
    left = left / bends[-1]
    new_coord = complex(left)
    xar.append(0)
    yar.append(new_coord.real)
    return (xar, yar)


# python -m unittest bubble_chart.TestImplementations or by test name as
# python -m unittest bubble_chart.TestImplementations.test_minimal_mine for ex.
class TestImplementations(TestCase):
    """Class that demonstrates the various algorithms considered."""
    def get_minimal_data(self):
        """Helper function to read the minimal data set."""
        file_name = './files/minimal.csv'
        input_data = np.recfromcsv(file_name).tolist()
        input_data.sort(reverse=True)
        radii = [idata[0] for idata in input_data]  # load the radii
        labels = [idata[1] for idata in input_data]  # load the labels
        return file_name, radii, labels

    def get_medium_data(self, entries=50):
        """Helper function to generate a medium data set."""
        radii = [randint(1, 500) for _ in xrange(entries)]
        labels = [''.join(SystemRandom().choice(string.uppercase +
                string.digits) for _ in range(6)) for _ in xrange(entries)]
        return ('MediumRandomSet.csv', radii, labels)

#         with open('./files/MediumRandomSet.csv', 'w+') as _fd:
#             for _ in xrange(50):
#                 _fd.write('%d, %s\n' % (randint(1, 500),
#                 ''.join(SystemRandom().choice(string.uppercase +
#                              string.digits) for _ in range(6))))

    def gen_large_data(self):
        """Helper function to generate a large data set."""
        with open('./files/LargeRandomSet2.csv', 'w+') as _fd:
            for _ in xrange(400):
                _fd.write('%d, %s\n' % (randint(1, 500),
                ''.join(SystemRandom().choice(string.uppercase +
                             string.digits) for _ in range(6))))

    def get_large_data(self):
        """Helper function to read the large data set."""
        file_name = './files/LargeRandomSet2.csv'
        input_data = np.recfromcsv(file_name).tolist()
        input_data.sort(reverse=True)
        radii = [idata[0] for idata in input_data]  # load the radii
        labels = [idata[1] for idata in input_data]  # load the labels
        return file_name, radii, labels

    def test_minimal_mine(self):
        """This algorithm did not work at all, since the algorithm is meant
        for use with a uniformly sized set of initial circles.  This is not
        the problem we are solving."""
        file_name, radii, labels = self.get_minimal_data()
        (_, axes) = plt.subplots(figsize=(10, 10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0] +
                       ' - Descartes', fontsize=28)
        xar, yar = calculate_coordinates(radii)
        axes.scatter(xar, yar, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, xar, yar, radii, labels)
        plt.show()

    def test_minimal_circles(self):
        """This brute force search algorithm works ok on tiny sets
        of 2, 3, 4 (if the data is well formed). It works fine for the
        configuration of data given in the example set, but does not work
        consistently if random generated data is used (see next test)."""
        file_name, radii, labels = self.get_minimal_data()
        (_, axes) = plt.subplots(figsize=(10, 10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0] +
                       ' - Brute', fontsize=28)
        circles = positionCircles(radii)
        xar = [aval for aval, bval, _ in circles]
        yar = [bval for aval, bval, _ in circles]
        axes.scatter(xar, yar, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, xar, yar, radii, labels)
        plt.show()

    def test_medium_circles(self):
        """This brute force search algorithm works ok on tiny sets.
        Overlaps at 3 - 6 (if data is not well formed), 10, 50 entries."""
        file_name, radii, labels = self.get_medium_data(entries=7)
        (_, axes) = plt.subplots(figsize=(10, 10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0] +
                       ' - Brute', fontsize=28)
        circles = positionCircles(radii)
        xar = [aval for aval, bval, _ in circles]
        yar = [bval for aval, bval, _ in circles]
        axes.scatter(xar, yar, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, xar, yar, radii, labels)
        plt.show()

    def test_large_circles(self):
        """This brute force search algorithm really tanks on large sets
        of 400 entries."""
        self.skipTest('Just TOO slow!')
        file_name, radii, labels = self.get_large_data()
        (_, axes) = plt.subplots(figsize=(10, 10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0] +
                       ' - Brute', fontsize=28)
        circles = positionCircles(radii)
        xar = [aval for aval, bval, _ in circles]
        yar = [bval for aval, bval, _ in circles]
        axes.scatter(xar, yar, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, xar, yar, radii, labels)
        plt.show()

    def test_minimal_circlepack(self):
        """This algorithm is incredibly fast, and I had high hopes of getting
        the graph to work correctly.  However, I am either configuring the
        graph incorrectly or the the CirclePack code is not spacing the
        circles correctly.  They are all overlapping.  Perhaps with more time
        I would be able to research this approach further."""
        file_name, radii, labels = self.get_minimal_data()
        (_, axes) = plt.subplots(figsize=(10, 10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0] +
                       ' - Graph', fontsize=28)
        my_graph = self.create_graph(radii, labels)
        internal = dict([(labels[0], my_graph.neighbors(labels[0]))])
        external = dict([(label, radius)
                          for radius, label in zip(radii[1:], labels[1:])])
        circle_pack_data = CirclePack(internal, external)
        xar = [aval.real for aval, _ in circle_pack_data.values()]
        yar = [aval.imag for aval, _ in circle_pack_data.values()]
        axes.scatter(xar, yar, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, xar, yar, radii, labels)
        plt.show()

    def test_large_circlepack(self):
        """This algorithm is incredibly fast, and I had high hopes of getting
        the graph to work correctly.  However, I am either configuring the
        graph incorrectly or the the CirclePack code is not spacing the
        circles correctly.  They are all overlapping.  Perhaps with more time
        I would be able to research this approach further."""
        file_name, radii, labels = self.get_large_data()
        (_, axes) = plt.subplots(figsize=(10, 10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0] +
                       ' - Graph', fontsize=28)
        my_graph = self.create_graph(radii, labels)
        internal = dict([(labels[0], my_graph.neighbors(labels[0]))])
        external = dict([(label, radius)
                          for radius, label in zip(radii[1:], labels[1:])])
        circle_pack_data = CirclePack(internal, external)
        xar = [aval.real for aval, _ in circle_pack_data.values()]
        yar = [aval.imag for aval, _ in circle_pack_data.values()]
        axes.scatter(xar, yar, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, xar, yar, radii, labels)
        plt.show()

    def create_graph(self, radii=None, labels=None):
        """Helper function to create the graph for use with CirclePack."""
        if radii == None or labels == None:
            _, radii, labels = self.get_minimal_data()
        my_graph = nx.Graph()
#         my_graph.add_cycle(labels, length=radii)
        my_graph.add_star(labels)
        return my_graph

    def test_minimal_repulsion(self, radii=None, labels=None):
        """This algorithm attempts to jitter the circles around until they
        settle on a non-overlapped position or the max number of iterations
        is reached. It works well for small sets, and is relatively fast.
        """
        file_name, radii, labels = self.get_minimal_data()
        (_, axes) = plt.subplots(figsize=(10, 10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0] +
                       ' - Repulsion', fontsize=28)
        data = []
        for radius in radii:
            data.append([randint(100, 200), randint(201, 300), radius])
        mat = matrix(data=data)
        iterate_layout(mat, [uniform(0, 1) for _ in xrange(len(radii))],
                       1, 1000, 1, 1000, 100000, False)
        xar = [entry[0] for entry in mat[:, 0].tolist()]
        yar = [entry[0] for entry in mat[:, 1].tolist()]
        axes.scatter(xar, yar, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, xar, yar, radii, labels)
        plt.show()

    def test_medium_repulsion(self):
        """This algorithm attempts to jitter the circles around until they
        settle on a non-overlapped position or the max number of iterations
        is reached. It doesn't work well for medium to large sets where the
        number of iterations required to jitter the circles out is time-wise
        expensive.
        """
        file_name, radii, labels = self.get_medium_data(20)
        (_, axes) = plt.subplots(figsize=(10, 10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0] +
                       ' - Repulsion', fontsize=28)
        data = []
        for radius in radii:
            data.append([randint(100, 200), randint(201, 300), radius])
        mat = matrix(data=data)
        iterate_layout(mat, [uniform(0, 1) for _ in xrange(len(radii))],
                       1, 1000, 1, 1000, 10000, False)
        xar = [entry[0] for entry in mat[:, 0].tolist()]
        yar = [entry[0] for entry in mat[:, 1].tolist()]
        axes.scatter(xar, yar, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, xar, yar, radii, labels)
        plt.show()

    def test_large_repulsion(self, radii=None, labels=None):
        """This algorithm attempts to jitter the circles around until they
        settle on a non-overlapped position or the max number of iterations
        is reached. It doesn't work well for medium to large sets where the
        number of iterations required to jitter the circles out is time-wise
        expensive.
        """
        self.skipTest('Just TOO slow!')
        file_name, radii, labels = self.get_large_data()
        (_, axes) = plt.subplots(figsize=(10, 10))
        axes.set_xlim((-1000, 1000))
        axes.set_ylim((-1000, 1000))
        axes.set_title(os.path.splitext(os.path.basename(file_name))[0] +
                       ' - Repulsion', fontsize=28)
        data = []
        for radius in radii:
            data.append([randint(100, 200), randint(201, 300), radius])
        mat = matrix(data=data)
        iterate_layout(mat, [uniform(0, 1) for _ in xrange(len(radii))],
                       1, 1000, 1, 1000, 5000, False)
        xar = [entry[0] for entry in mat[:, 0].tolist()]
        yar = [entry[0] for entry in mat[:, 1].tolist()]
        axes.scatter(xar, yar, alpha=0.5, marker="o", label="bubbles")
        draw_circles(axes, xar, yar, radii, labels)
        plt.show()


def main():
    """The bubble_chart main function."""
    parser = ArgumentParser(description='Plot a set of circles provided ' +
        'a list of radii in column 1 of a comma separated value (CSV).')
    parser.add_argument('-f', '--file', type=file,
                        default=os.path.join('files', 'minimal.csv'))
    args = parser.parse_args()
    args.file.close()
    input_data = np.recfromcsv(args.file.name).tolist()
    input_data.sort(reverse=True)
    radii = [idata[0] for idata in input_data]  # load the radii
    labels = [idata[1] for idata in input_data]  # load the labels

    (_, axes) = plt.subplots(figsize=(10, 10))
    axes.set_xlim((-1000, 1000))
    axes.set_ylim((-1000, 1000))
    axes.set_title(os.path.splitext(os.path.basename(args.file.name))[0] +
                   ' - Repulsion', fontsize=28)
    data = []
    for radius in radii:
        data.append([randint(100, 200), randint(201, 300), radius])
    mat = matrix(data=data)
    iterate_layout(mat, [uniform(0, 1) for _ in xrange(len(radii))],
                   1, 1000, 1, 1000, 5000, False)
    xar = [entry[0] for entry in mat[:, 0].tolist()]
    yar = [entry[0] for entry in mat[:, 1].tolist()]
    axes.scatter(xar, yar, alpha=0.5, marker="o", label="bubbles")
    draw_circles(axes, xar, yar, radii, labels)
    plt.show()


if __name__ == '__main__':
    main()
