# Converted from C++ to python using source posted at
# https://github.com/mbedward/packcircles/blob/master/src/packcircles.cpp
from math import sqrt
"""
// Attempts to position circles without overlap.
// 
// Given an input matrix of circle positions and sizes, attempts to position them
// without overlap by iterating the pair-repulsion algorithm.
// 
// @param xyr 3 column matrix (centre x, centre y, radius)
// @param weights vector of double values between 0 and 1, used as multiplicative
//   weights for the distance a circle will move with pair-repulsion.
// @param xmin lower X bound
// @param xmax upper X bound
// @param ymin lower Y bound
// @param ymax upper Y bound
// @param maxiter maximum number of iterations
// @param wrap true to allow coordinate wrapping across opposite bounds 
//
// @return the number of iterations performed.
"""
def iterate_layout(xyr, weights, xmin, xmax, ymin, ymax, maxiter, wrap):
    rows = xyr.shape[0];

    for iter in range(maxiter):
        moved = 0;
        for i_cnt in range(rows - 1):
            for j_cnt in range(i_cnt + 1, rows):
                if (do_repulsion(xyr, weights, i_cnt, j_cnt,
                                 xmin, xmax, ymin, ymax, wrap)):
                    moved = 1
        if moved == 0: break
    if iter == maxiter - 1:
        print "returning for maxiter"
    return iter


"""
/*
 * Checks if two circles overlap excessively and, if so, moves them
 * apart. The distance moved by each circle is proportional to the
 * radius of the other to give some semblance of intertia.
 * 
 * xyr     - 3 column matrix of circle positions and sizes (x, y, radius)
 * c0      - index of first circle
 * c1      - index of second circle
 * xmin    - bounds min X
 * xmax    - bounds max X
 * ymin    - bounds min Y
 * ymax    - bounds max Y
 * wrap    - allow coordinate wrapping across opposite bounds
 */
"""
def do_repulsion(xyr, weights, c0, c1, xmin, xmax, ymin, ymax, wrap):
    ## if both weights are zero, return zero to indicate
    ## no movement
    if (almostZero(weights[c0]) and almostZero(weights[c1])):
        return 0
    
    dx = xyr.item(c1, 0) - xyr.item(c0, 0)
    dy = xyr.item(c1, 1) - xyr.item(c0, 1)
    d = sqrt(dx*dx + dy*dy)
    r = xyr.item(c1, 2) + xyr.item(c0, 2)
    p = 0
    w0 = 0
    w1 = 0
 
    if (gtZero(r - d)):
      if (almostZero(d)):
        ## The two centres are coincident or almost so.
        ## Arbitrarily move along x-axis
        p = 1.0;
        dx = r - d;
      else:
        p = (r - d) / d;

      w0 = weights[c0] * xyr.item(c1, 2) / r
      w1 = weights[c1] * xyr.item(c0, 2) / r
      
      xyr.itemset(c1, 0, ordinate(xyr.item(c1, 0) + p*dx*w1, xmin, xmax, wrap))
      xyr.itemset(c1, 1, ordinate(xyr.item(c1, 1) + p*dy*w1, ymin, ymax, wrap))
      xyr.itemset(c0, 0, ordinate(xyr.item(c0, 0) - p*dx*w0, xmin, xmax, wrap))
      xyr.itemset(c0, 1, ordinate(xyr.item(c0, 1) - p*dy*w0, ymin, ymax, wrap))
      
      return 1

    return 0

"""
/*
 * Adjust an X or Y ordinate to the given bounds by either wrapping
 * (if `wrap` is true) or clamping (if `wrap` is false).
 */
"""
def ordinate(x, lo, hi, wrap):
  if (wrap):
    return wrapOrdinate(x, lo, hi)
  else:
    return max(lo, min(hi, x))


"""
/*
 * Map an X or Y ordinate to the toroidal interval [lo, hi).
 *
 * x  - X or Y ordinate to be adjusted
 * lo - lower coordinate bound
 * hi - upper coordinate bound
 */
"""
def wrapOrdinate(x, lo, hi):
  w = hi - lo;
  while (x < lo):
    x += w
  while (x >= hi):
    x -= w
  return x

def almostZero(x):
  TOL = 0.00001;
  return abs(x) < TOL;


def gtZero(x):
  return almostZero(x) == 0 and (x > 0.0)  
