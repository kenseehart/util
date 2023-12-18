'''Create a python module boilerplate implementation of a command

- Recommended: use `mkdo` to install the command
'''

template = """
r'''This is all boilerplate for your new command created by mkpy.

This docstring is also the help comment

Remember to `mkdo {name}` to install it.
'''

# install-me # <- This command will be installed

from argparse import RawTextHelpFormatter, ArgumentParser
import sys
from os.path import basename, splitext, join
this_name = splitext(basename(__file__))[0]

verbose = False

def vprint(*args, **kwargs):
    if verbose:
        print(*args, file=sys.stderr, **kwargs)

class NoException(Exception):
    pass

def {name}():
    pass

def main():
    global verbose

    parser = ArgumentParser(prog=this_name,
        formatter_class=RawTextHelpFormatter, description=__doc__)
    #parser.add_argument('name', help='name of something')
    parser.add_argument('-v', action='store_true', help='show debugging output')
    parser.add_argument('-e', action='store_true', help='raise exception on error')

    args = parser.parse_args()
    verbose = args.v
    etype = NoException if args.e else Exception # conditional exception handling

    try:
        r = {name}()
        print (r)
    except etype as e: # Best if replaced with explicit exception
        print (e, file=sys.stderr)
        exit(1)

if __name__=='__main__':
    main()

"""
# install-me # <- This command will be installed

from argparse import RawTextHelpFormatter, ArgumentParser
import sys
from os.path import join, basename, splitext, dirname
import subprocess
this_name = splitext(basename(__file__))[0]


def mkpy(name:str, py_dir=None):
    py_dir = py_dir or dirname(__file__)
    py_name = join(py_dir, name+'.py')
    src = template.format(name=name)

    with open(py_name, 'w') as f:
        f.write(src)

    return py_name



def main():
    parser = ArgumentParser(prog=this_name,
        formatter_class=RawTextHelpFormatter, description=__doc__)
    parser.add_argument('name', help='command name')

    args = parser.parse_args()
    name = args.name

    r = mkpy(name)
    print (r)

if __name__=='__main__':
    main()


