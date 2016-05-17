#!/usr/bin/env python
import os
import sys

from distutils.core import setup
from distutils.spawn import spawn
from distutils.dir_util import remove_tree
from glob import glob

if os.path.exists(os.path.join(os.curdir, 'dist')):
    remove_tree(os.path.join(os.curdir, 'dist'))

dat_files = glob('files' + os.path.sep + '*.csv')
dat_files.append(os.path.join('examples', 'goog.npy'))
setup(name='R9BDT',
      version='1.0',
      description='A bubble chart application',
      author='Kim Mayfield',
      author_email=' ',
      url='https://www.github.com/kmayfield/r9bdt',
      py_modules=['bubble_chart', 'packcircles'],
      packages=['examples'],
      data_files=dat_files,
     )
