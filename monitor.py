'''
Base classes to reactively monitor files in a directory.

Copyright 2016, 2019 Ken Seehart, all rights reserved

Written independently by Ken Seehart, not under contract.
'''

import os, sys
import threading
import time
from os.path import splitext, isfile, basename
from queue import Queue

verbose = False

def vprint(*args, **kwargs):
    if verbose:
        print(*args, file=sys.stderr, **kwargs)

class Poller:
    thread: threading.Thread
    q:Queue # queue of command tuples (callable, arg1, arg2, ...)

    def __init__(self):
        self.q = Queue()
        self.alive = True
        self.thread = threading.Thread(target=self.poll_loop)
        self.thread.start()
        
    def poll_loop(self):
        'polling thread'
        while self.alive:
            time.sleep(0.05)
            self.poll()

    def on_idle(self):
        'call this from the main thread (GUI thread if any, otherwise in run()) periodically'
        while not self.q.empty():
            fn = self.q.get_nowait()
            if fn is not None:
                fn[0](*fn[1:])

    def run_forever(self):
        'Main loop (if you have a GUI thread, use that instead of run_forever() and call self.on_idle() from there)'
        while self.alive:
            self.on_idle()
            time.sleep(0.05)


class FileMonitor(Poller):
    '''Base class for file monitors
    A file monitor watches a specified file, and triggers on_change and on_delete accordingly
    '''
    
    name:str
    filename:str

    def __init__(self, filename:str):
        self.filename = filename
        self.name = os.path.splitext(basename(filename))[0]
        self.t = 0
        self.h = 0
        super().__init__()

    def __repr__(self):
        return f'<{type(self)}: {self.name}>'

    def poll(self):
        'called by polling thread. Do not make gui calls from here: instead use self.q.put()'
        try:
            t = os.stat(self.filename)[8]
        except FileNotFoundError:
            self.q.put((self.on_delete,))
            return False

        if self.t != t:
            self.t = t
            try:
                with open(self.filename, 'rb') as f:
                    h = hash(f.read())
            except FileNotFoundError:
                self.q.put((self.on_delete,))
                return False
            except PermissionError:
                return False

            if self.h != h:
                self.h = h
                self.q.put((self.on_change,))
                return True

    def on_change(self):
        vprint('changed '+self.filename)

    def on_delete(self):
        vprint('deleted '+self.filename)



class DirMonitor(Poller):
    '''Monitors a the contents of a directory
    A directory monitor watches a specified directory and attaches a FileMonitor instances (of the specified type)
    to files in that directory.
    
    fmClass is a FileMonitor class to attach to files with the specified extension

    The process exits if the directory is deleted!
    '''

    def __init__(self, path:str, ext_types:dict):
        self.path = path
        self.ext_types = ext_types
        self.views = {}
        self.t = 0
        super().__init__()

    def __repr__(self):
        return f'<{type(self)}: {self.path}>'

    def poll(self):
        'called by polling thread. Do not make gui calls from here: instead use self.q.put()'
        try:
            t = os.stat(self.path)[8]
        except FileNotFoundError:
            self.q.put((self.on_delete,))
            return False

        if self.t != t:
            self.t = t
            self.q.put((self.on_change,))

    def on_change(self):
        fset = set([f for f in os.listdir(self.path) 
            if splitext(f)[1][1:] in self.ext_types and
            isfile(os.path.join(self.path, f))])

        fkeys = set(self.views.keys())

        for f in fset-fkeys:
            self.views[f] = self.ext_types[splitext(f)[1][1:]](os.path.join(self.path, f))
            print('added '+f)

        for f in fkeys-fset:
            self.views.pop(f)
            print('removed '+f)


    def on_delete(self):
        print('deleted '+self.path)
        self.alive = False

