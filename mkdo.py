
r'''install a python module as a command in the bin directory

To install this the first time:

$ python3 mkdo.py mkdo my/bin/directory

Now mkdo is a command, and my/bin/directory is the default location for new commands.

To install a python module (must be locatable by import) as a command:

$ mkdo mycommand

Then you can run your command:

$ mycommand ...args...

'''

# install-me # <- This command will be installed by the setup script

import argparse
import sys, os
from os.path import basename, dirname, splitext, join, exists, isdir, islink, abspath
import subprocess

this_name = splitext(basename(__file__))[0]

def mkdo(name:str, bin_dir:str=None):
    bin_dir = bin_dir or dirname(subprocess.check_output(['which', this_name]).decode())
    print ('installing', name, 'in', bin_dir)
    bin_name = abspath(join(bin_dir, name))

    if exists(bin_name):
        os.unlink(bin_name)

    src = 'python -m `basename "$0"` "$@"\n'

    with open(bin_name, 'w') as f:
        f.write(src)

    os.chmod(bin_name, 0o755)

    return bin_name

def main():
    parser = argparse.ArgumentParser(prog=this_name, description=__doc__)
    parser.add_argument('name', help='command name (python module name) or .wrapper to convert wrappers')
    parser.add_argument('-d', help=f'bin directory (default=location of {this_name} command)')

    args = parser.parse_args()

    try:
        r = mkdo(args.name, args.d)
        print (r)
    except Exception as e: # Best if replaced with explicit exception
        print (e, file=sys.stderr)
        exit(1)

if __name__=='__main__':
    main()

