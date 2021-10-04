
r'''Reactively display all content in the specified directory
'''

# install-me # <- This command will be installed by the install script

from monitor import DirMonitor, FileMonitor
import os, sys, shutil
import argparse
from os.path import join, basename, splitext, exists, expanduser, abspath

from subprocess import Popen, PIPE, run
import tkinter as tk

from yamster import Yamster

DEFAULT_SELECTED = True # True: images shown by default

this_name = splitext(basename(__file__))[0]

verbose = False

def vprint(*args, **kwargs):
    if verbose:
        print(*args, file=sys.stderr, **kwargs)

class NoException(Exception):
    pass


class ImgFileMonitor(FileMonitor):
    def __init__(self, filename: str):
        super().__init__(filename)

        gmon_dir = expanduser('~/.gmon')
        
        if not exists(gmon_dir):
            os.mkdir(gmon_dir)

        self.yamster = Yamster(join(gmon_dir, f'{basename(filename)}.yaml'))

        if self.yamster.selected == None:
            self.yamster.selected = DEFAULT_SELECTED
        
        self.process = None
        self.start_process()

        self.selected = tk.IntVar()
        self.selected.set(self.yamster.selected)
        self.cb = tk.Checkbutton(app, text=self.name, variable=self.selected, command=self.on_cb)
        self.cb.pack(anchor=tk.W)
        app.pack(fill=tk.BOTH)

    def start_process(self):
        if self.process is None:
            self.process = Popen(['python3', '-m', 'gview', self.filename])

    def kill_process(self):
        if self.process:
            self.process.kill()
            self.process = None

    def update_process(self):
        if self.yamster.selected:
            self.start_process()
        else:
            self.kill_process()


    def on_cb(self):
        self.yamster.selected = self.selected.get()
        self.update_process()



class Application(tk.Frame):
    dm: DirMonitor

    def __init__(self, path:str):
        self.path = abspath(path)
        self.master = tk.Tk()
        tk.Frame.__init__(self, self.master)
        self.master.title(f'{this_name} - {self.path}')
        
        self.dm = DirMonitor(path, {
            'jpg': ImgFileMonitor,
            'png': ImgFileMonitor,
            'tif': ImgFileMonitor,
            'tiff': ImgFileMonitor,
        })

        self.master.geometry("600x200")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.dm.alive = False
        ifm:ImgFileMonitor

        for ifm in self.dm.views.values():
            ifm.alive = False
            ifm.kill_process()

        self.master.destroy()


def gmon(path: str):
    global app
    app = Application(path)
    while app.dm.alive:
        app.dm.on_idle()
        app.update_idletasks()
        app.update()


def main():
    global verbose

    parser = argparse.ArgumentParser(prog=this_name, description=__doc__)
    parser.add_argument('path', help='directory to monitor')
    parser.add_argument('-v', action='store_true', help='show debugging output')
    parser.add_argument('-e', action='store_true', help='raise exception on error')

    args = parser.parse_args()
    verbose = args.v
    etype = NoException if args.e else Exception # conditional exception handling

    try:
        r = gmon(args.path)
    except etype as e:
        print (e, file=sys.stderr)
        exit(1)

if __name__=='__main__':
    main()

