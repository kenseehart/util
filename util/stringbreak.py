'''
String Break

A small collection of monkey-patch hacks that let you do things you aren't supposed to do.

Use with caution!

Best use case: make extreme debugging tools.

- wbp: break (or do something else) when anything writes the specified string to any file
- abp: break (or do something else) on attribute access globally
- alias_attr: alias an attribute on all objects everywhere

Set a global breakpoint on writing a specified string, or appending to a list

## Limitations:

- not supported on Windows

## Requirements:

- python 3.6 or later
- ctypes


## Credits *(these contributions are in the public domain)*:

- [proxy dict monkeypatching technique using ctypes: ](https://gist.github.com/bricef/1b0389ee89bd5b55113c7f3f3d6394ae)Armin R.
- [magic_flush_mro_cache](https://stackoverflow.com/questions/38257613/how-to-monkey-patch-python-list-setitem-method): Hrvoje

-----


# Typical workflow

Invoke the following either in your code or in an interactive python session

```
from write_breakpoint import wbp
wbp('spam')
```

Set a breakpoint in WBPContext.check_string() in this file

When any code writes a specified string to a stream, file, StringIO, or list, the breakpoint will be triggered.

'''

import ctypes
import io
from types import MappingProxyType
from collections import defaultdict

class WBPExecption(Exception):
    pass

# figure out side of _Py_ssize_t
if hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
    _Py_ssize_t = ctypes.c_int64
else:
    _Py_ssize_t = ctypes.c_int

# regular python
class _PyObject(ctypes.Structure):
    pass
_PyObject._fields_ = [
    ('ob_refcnt', _Py_ssize_t),
    ('ob_type', ctypes.POINTER(_PyObject))
]

# python with trace
if object.__basicsize__ != ctypes.sizeof(_PyObject):
    class _PyObject(ctypes.Structure):
        pass
    _PyObject._fields_ = [
        ('_ob_next', ctypes.POINTER(_PyObject)),
        ('_ob_prev', ctypes.POINTER(_PyObject)),
        ('ob_refcnt', _Py_ssize_t),
        ('ob_type', ctypes.POINTER(_PyObject))
    ]


class _DictProxy(_PyObject):
    _fields_ = [('dict', ctypes.POINTER(_PyObject))]


def reveal_dict(proxy):
    if not isinstance(proxy, MappingProxyType):
        raise TypeError('dictproxy expected')
    dp = _DictProxy.from_address(id(proxy))
    ns = {}
    ctypes.pythonapi.PyDict_SetItem(ctypes.py_object(ns),
                                    ctypes.py_object(None),
                                    dp.dict)
    return ns[None]


def get_class_dict(cls):
    if isinstance(cls, dict):
        return cls

    d = getattr(cls, '__dict__', None)
    if d is None:
        raise TypeError('given class does not have a dictionary')
    if isinstance(d, MappingProxyType):
        return reveal_dict(d)
    return d


def magic_flush_mro_cache():
    ctypes.PyDLL(None).PyType_Modified(ctypes.py_object(object))

file_type = type(open(__file__))

class ProxyMap:
    def __init__(self):
        self.std = defaultdict(lambda: (None, None))
        self.disabled = False

    def __del__(self):
        self.clear_proxies()

    def set_proxy(self, cls, name, fn):
        d = get_class_dict(cls)
        super_fn, _ = self.std[(str(cls), name)]

        if not super_fn:
            super_fn = d[name]
            self.std[(str(cls), name)] = (super_fn, cls)

        def new_fn(*args, fn=fn, sup=super_fn, **kwargs):
            if self.disabled:
                sup(*args, **kwargs)
            else:
                self.disabled = True # prevent recursion
                fn(sup, *args, **kwargs)
                self.disabled = False

        d[name] = new_fn
        magic_flush_mro_cache()

    def clear_proxies(self):
        for ((_, name), (fn, cls)) in self.std.items():
            d = get_class_dict(cls)
            d[name] = fn

        try:
            magic_flush_mro_cache()
        except TypeError:
            pass


class WBPContext(ProxyMap):
    def __init__(self):
        super().__init__()
        self.breakpoints = set()
        self.disabled = False

    def enable_hook(self):
        self.set_proxy(list, 'append', self.proxy_append)
        self.set_proxy(file_type, 'write', self.proxy_write)
        self.set_proxy(io.StringIO, 'write', self.proxy_write)

    def disable_hook(self):
        self.clear_proxies()

    def sbp(self, s: str):
        'set write breakpoint'
        if not self.breakpoints:
            self.enable_hook()

        self.breakpoints.add(s)

    def cbp(self, s=None):
        'clear write breakpoint'
        if s:
            self.breakpoints.remove(s)
        else:
            self.breakpoints.clear()

        if not self.breakpoints:
            self.disable_hook()

    def proxy_write(self, sup, f, s):
        sup(f, s)
        self.check_string(s)

    def proxy_append(self, sup, l, s):
        sup(l, s)
        if isinstance(s, str):
            self.check_string(s)

    def check_string(self, s):
        for bs in self.breakpoints:
            if bs in s:
                breakpoint()


def add_global_property(k, get_k, set_k):
    d = get_class_dict(object)
    d[k] = property(get_k, set_k)


def alias_attr(alias_k, target_k):
    def get_k(obj):
        if target_k in obj.__dict__:
            return obj.__dict__[target_k]
        return getattr(obj, alias_k)

    def set_k(obj, v):
        return setattr(obj, alias_k, v)

    add_global_property(target_k, get_k, set_k)

    # mask dir() such that the target only shows up if the alias has a value, and hide the alias
    old_dir = object.__dir__

    def __dir__(obj):
        'hide the attr alias'
        dlist = old_dir(obj)
        if not hasattr(obj, target_k):
            dlist.remove(target_k)
        if alias_k in dlist:
            dlist.remove(alias_k)
        return dlist

    d = get_class_dict(object)
    d['__dir__'] = __dir__



    #d = get_class_dict(type)
    #old_type_new = type.__new__

    #def __new__(*args, **kwargs):
        #if alias_k in kwargs:
            #kwargs[target_k] = kwargs.pop(alias_k)

        #old_type_new(*args, **kwargs)

    #d['__new__'] = __new__
    magic_flush_mro_cache()



wbp_context = WBPContext()

sbp = wbp_context.sbp
cbp = wbp_context.cbp
