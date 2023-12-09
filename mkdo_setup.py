import sys
from os.path import dirname
from util.mkdo import mkdo

bin_dir = dirname(sys.executable)
mkdo('util.mkdo', bin_dir)
mkdo('util.mkpy', bin_dir)
mkdo('util.whip', bin_dir)
