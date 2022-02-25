'''Indexed Properties

Syntactic sugar to express virtual indexed access with simple array notation

See IPropTest for usage examples
'''

from collections import defaultdict
from subprocess import call
from typing import Any, Callable, Dict
import unittest


# Type declarations for indexed getter and setter
GETI = Callable[[Any, int], Any]
SETI = Callable[[Any, int, Any], None]


class iproperty():
    'indexed property: wraps indexed methods with intuitive array semantics'
    names: Dict[int,str]

    def __init__(self, geti: GETI, seti: SETI):
        self.geti:GETI = lambda obj, i: self.types[i](geti(obj, i))
        self.seti:SETI = seti
        self.names = {} # alias declaration names
        self.types = defaultdict(lambda: lambda x:x) # type annotations (implicitly casts geti)

    def __getitem__(self, i:int):
        'return a propery than accesses the specified index (invoke as attribute declaration)'

        p = property(
            lambda obj: self.geti(obj, i),
            lambda obj, v: self.seti(obj, i, v),
        )
        p.fget.__annotations__['i'] = i # save index in annotation for ipropclass setup
        p.fget.__annotations__['iprop'] = self # save index in annotation for ipropclass setup
        return p

    def __get__(self, obj, objtype):
        'return a read/write indexable object (invoke at run time)'

        class iprop_instance:
            'instantiated iproperty'
            def __init__(self, obj: Any, iprop:'iproperty'):
                self.obj = obj
                self.iprop:iproperty = iprop
                self.names = iprop.names

            def __getitem__(self, i:int):
                v = self.iprop.geti(self.obj, i)
                return v

            def __setitem__(self, i:int, v:Any):
                self.iprop.seti(self.obj, i, v)

        return iprop_instance(obj, self)


def ipropclass(cls):
    cls.iprop_by_id = {}

    for k in dir(cls):
        if k[:2] != '__':
            v = getattr(cls, k)
            if isinstance(v, property):
                try:
                    iprop:iproperty = v.fget.__annotations__['iprop']
                    i = v.fget.__annotations__['i']
                    iprop.names[i] = k
                    try:
                        t = cls.__annotations__[k]
                        if callable(t):
                            iprop.types[i] = t
                    except KeyError:
                        pass
                except KeyError:
                    pass # it's a property, but not a indexed propery, so no business here.
    return cls

class IPropTest(unittest.TestCase):

    def test_all(self):

        @ipropclass
        class Foo:
            def __init__(self):
                self.a = [0, 1, 2, 3]

            def get_i(self, i:int):
                return self.a[i]

            def set_i(self, i:int, v:Any):
                self.a[i] = v


            # declaration of a virtual array property
            reg = iproperty(get_i, set_i)

            # declarations of index aliases
            ichi = reg[1]
            ni:float = reg[2] # implicitly casts ni and reg[2] as float
            san = reg[3]


        foo = Foo()

        self.assertEqual(foo.ni, 2)
        self.assertEqual(foo.san, 3)

        # writing by alias
        foo.ni = 77

        # reading by index
        self.assertEqual(foo.reg[2], 77.0)


        # writing by index
        foo.reg[3] = 777

        # reading by alias
        self.assertEqual(foo.san, 777)

        # type annotations
        self.assertIsInstance(foo.ni, float)
        self.assertIsInstance(foo.san, int)

        # names
        self.assertEqual(foo.reg.names[3], 'san')


if __name__ == '__main__':
    unittest.main()
