'Yaml store'

import os
from logging import FileHandler
from os.path import exists, join
from typing import Any, Dict, Callable, NoReturn
import unittest
import tempfile
import time
from cv2 import split
import yaml

from filelock import Timeout, FileLock # pip3 install filelock
import monitor

class Yamster:
    _filename:str
    _content:Dict[str, Any]

    _cache = {}

    def __new__(cls, filename:str, *args):
        if filename not in cls._cache:
            cls._cache[filename] = super().__new__(cls)

        return cls._cache[filename]

    def __init__(self, filename:str, callback: Callable[[str, Any, Any], NoReturn]=None):
        self._filename = filename

        d, f = os.path.split(filename)
        self._lock_filename = join(d, '.filelock.'+f)
        self._lock = FileLock(self._lock_filename)

        if exists(filename):
            self._load()
        else:
            self._content = {}
            self._save()

        self._callback = callback

        if callback:
            self._react_thread = threading.Thread(target = self._react_monitor)
            self._react_thread.start()
            self._t = self._h = 0


    def _react_monitor(self):
        while 1:
            time.sleep(0.05)
            dirty = False

            try:
                t = os.stat(self._filename)[8]
            except FileNotFoundError:
                dirty = True
                self._t = t = 0

            if self._t != t:
                self._t = t

                with open(self._filename, 'rb') as f:
                    h = hash(f.read())

                if self._h != h:
                    self._h = h
                    dirty = True

            if dirty:
                old_content = self._content.copy()
                if exists(self._filename):
                    self._load()
                else:
                    self._content = {}
                    try:
                        self._save()
                    except FileNotFoundError:
                        # directory gone.
                        break

                for k in set(self._content.keys()) | set(old_content):
                    if self._content.get(k, None) != old_content.get(k, None):
                        self._callback(k, old_content.get(k, None), self._content.get(k, None))


    def __repr__(self):
        return f'<Yamster: {self._filename}'

    def _load(self):
        with self._lock:
            with open(self._filename) as f:
                self._content = yaml.load(f, Loader=yaml.FullLoader)
            assert(isinstance(self._content, dict))

    def _save(self):
        with self._lock:
            with open(self._filename, 'w') as f:
                yaml.safe_dump(self._content, f)
    
    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            return super().__getattr__(name)
        else:
            try:
                return self._content[name]
            except KeyError:
                return None

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            return super().__setattr__(name, value)
        else:
            if self._content.get(name, None) != value:
                with self._lock:
                    backup = self._content.copy()

                    if value is None:
                        if name in self._content:
                            del self._content[name]
                    else:
                        self._content[name] = value

                try:
                    self._save()
                except yaml.representer.RepresenterError:
                    self._content = backup
                    raise TypeError(f"type({name}): {type(value)} is not serializable as yaml")

    def __delattr__(self, name: str) -> None:
        self.__setattr__(name, None)

    __getitem__ = __getattr__
    __setitem__ = __setattr__
    __delitem__ = __delattr__

        
class TestYamster(unittest.TestCase):
    def test_yamster(self):
        def cb(k, v0, v1):
            print(f'{k} = {v0}->{v1}')

        with tempfile.TemporaryDirectory() as dirname:
            filename = join(dirname, 'y')
            print (f'temp file: {filename}')
            y = Yamster(filename, cb)
            y.foo = 5
            y.bar = 6
            y.foo=None
            self.assertEqual(y['bar'], 6)
            y['x'] = 7
            self.assertEqual(y.x, 7)

            z = Yamster(filename)
            with self.assertRaises(TypeError):
                z.bad = z

            self.assertEqual(z.bad, None)

            self.assertEqual(z.x, 7)
            z.x = 12

            with open(filename) as f:
                s = f.read()
                print (s)

            time.sleep(.5)

if __name__ == '__main__':
    unittest.main()

