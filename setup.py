from setuptools import setup, find_packages
from os.path import join, dirname, basename, split, splitext, abspath, exists
from os import listdir
import sys
from importlib import import_module
from glob import glob

this_name = splitext(basename(__file__))[0]
this_dir = abspath(dirname(__file__))

verbose = False

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name=basename(dirname(__file__)),
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
)


