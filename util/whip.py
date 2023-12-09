
'''Locate a python module - like which, but for python modules

Gives the filename that will be loaded by `import`
'''

# install-me # <- This command will be installed by the install script

import sys
import argparse
from importlib.util import find_spec

def whip(name):
    spec = find_spec(name)
    if spec and spec.loader:
        return spec.loader.get_filename(name)
    raise FileNotFoundError(name)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', help='module name')

    args = parser.parse_args()
    name = args.name
    try:
        print (whip(name))
    except FileNotFoundError:
        print (f'module {name} not found', file=sys.stderr)
        exit(1)

if __name__=='__main__':
    main()








