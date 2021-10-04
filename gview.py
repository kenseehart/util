
r'''Graphics viewer

Watches a image file and reacts to the yamster at ~/.gmon/{filename}.yaml

Reacts to changes in the file content or changes in the yamster, which is a persistent store of window position and other view settings.

Exits if yamster.visible changes to False, sets yamster.visible=True on startup.

Lauched by gmon. 
'''

# install-me # <- This command will be installed by the install script

from argparse import RawTextHelpFormatter, ArgumentParser
from genericpath import exists
import os, sys
from os.path import join, basename, splitext, abspath, expanduser
import time

import cv2 as cv
import matplotlib
import matplotlib.pyplot as plt
from monitor import FileMonitor
from yamster import Yamster
from matplotlib.backends import backend_qt5


this_name = splitext(basename(__file__))[0]

verbose = False

def vprint(*args, **kwargs):
    if verbose:
        print(*args, file=sys.stderr, **kwargs)

class NoException(Exception):
    pass


the_imgview:'ImgView' = None

def monkey_qt5():
    'matplotlib neglected to support window move events, so we fix that, and treat as a resize'

    class MainWindowMixin:
        def moveEvent(self, event):
            backend_qt5.QtWidgets.QWidget.moveEvent(self, event)
            
            # emit as a resize event
            if the_imgview:
                the_imgview.on_resize(None)

    if MainWindowMixin not in backend_qt5.MainWindow.__bases__:
        backend_qt5.MainWindow.__bases__ = (MainWindowMixin,) + backend_qt5.MainWindow.__bases__


class ImgView(FileMonitor):
    def __init__(self, filename: str):
        global the_imgview
        super().__init__(filename)

        the_imgview = self
        gmon_dir = expanduser('~/.gmon')
        
        if not exists(gmon_dir):
            os.mkdir(gmon_dir)

        self.yamster = Yamster(join(gmon_dir, f'{basename(filename)}.yaml'))
        self.read_img()


    def run(self):
        self.figure.canvas.set_window_title(self.name)
        self.figure.canvas.mpl_connect('resize_event', self.on_resize)
        self.figure.canvas.mpl_connect('close_event', self.on_close)
        self.geom = self.yamster.geom

        plt.ion()
        plt.show() # blocks until window is closed.
        
        while self.alive:
            self.on_idle()
            self.figure.canvas.start_event_loop(0.05)

        vprint('run() exiting')

    def read_img(self):
        vprint(f'loading {self.filename}')
        self.img = cv.imread(self.filename)
        if self.img is not None:
            self.figure = plt.imshow(self.img).figure
        else:
            raise IOError(f"Could not read {self.filename}")

    @property
    def geom(self):
        mngr = plt.get_current_fig_manager()
        return mngr.window.geometry().getRect() # requires matplotlib.use('Qt5Agg')

    @geom.setter
    def geom(self, geom:tuple):
        if geom:
            mngr = plt.get_current_fig_manager()
            mngr.window.setGeometry(*geom)

    def on_change(self):
        vprint(f'{self.name}.onchange()')
        self.read_img()

    def on_delete(self):
        'file was removed'
        vprint(f'{self.name}.on_delete()')
        self.alive = 0

    def on_close(self, _):
        'window closed'
        vprint(f'{self.name}.on_close()')
        self.alive = 0

    def on_resize(self, _):
        vprint(f'{self.name}.on_resize() -> {self.geom}')
        self.yamster.geom = self.geom

def gview(filename:str):
    matplotlib.use('Qt5Agg') # support geom(), and menu on top

    v = ImgView(abspath(filename))
    v.run()


def main():
    global verbose

    parser = ArgumentParser(prog=this_name,
        formatter_class=RawTextHelpFormatter, description=__doc__)
    parser.add_argument('file', help='image file to display')
    parser.add_argument('-v', action='store_true', help='show debugging output')
    parser.add_argument('-e', action='store_true', help='raise exception on error')

    args = parser.parse_args()
    verbose = args.v
    etype = NoException if args.e else Exception # conditional exception handling

    try:
        monkey_qt5()
        gview(args.file)
    except etype as e: # Best if replaced with explicit exception
        print (e, file=sys.stderr)
        exit(1)

if __name__=='__main__':
    main()

