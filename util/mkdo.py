r'''Install a Python module as an executable command

`mkdo` creates executable command wrappers for Python modules.

This is preferable to the common practice of using `#!/usr/bin/env python` and making
a script executable. We recommend deprecating that practice in favor of `mkdo`.

Using python -m unifies import semantics. Removing .py from the command name makes it
more user-friendly.

USAGE:

  Initial setup:
  $ python3 mkdo.py mkdo /path/to/bin

  This installs mkdo itself as a command, with /path/to/bin as the
  default location for new commands.

  Creating commands:
  $ mkdo module_name        # Creates a command for a standard module
  $ mkdo package.module     # Creates a command for a module in a package

  The created command can be run directly:
  $ module_name [arguments]

mkdo requires that the module be importable from the current Python environment.
'''

# install-me # <- This command will be installed by the setup script

import argparse
import sys, os
from os.path import basename, dirname, split, splitext, join, exists, isdir, islink, abspath
import subprocess

this_name = splitext(basename(__file__))[0]

def mkdo(name:str, bin_dir:str=None):
    try:
        bin_dir = bin_dir or dirname(subprocess.check_output(['which', this_name]).decode())
    except subprocess.CalledProcessError:
        # are we in a virtualenv or conda environment?
        if 'VIRTUAL_ENV' in os.environ or 'CONDA_PREFIX' in os.environ:
            bin_dir = split(sys.executable)[0]
        else:
            raise Exception(f'not in virtual or conda environment, so please use python -m {this_name} mkdo mkdo -d mybinpath')

    print ('installing', name, 'in', bin_dir)

    if '.' in name:
        package, name = name.split('.')
        src = f'python -m {package}.`basename "$0"` "$@"\n'
    else:
        src = 'python -m `basename "$0"` "$@"\n'

    bin_name = abspath(join(bin_dir, name))

    if exists(bin_name):
        os.unlink(bin_name)

    with open(bin_name, 'w') as f:
        f.write(src)

    os.chmod(bin_name, 0o755)

    return bin_name

def main():
    parser = argparse.ArgumentParser(
        prog=this_name,
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('name', help='command name (Python module name, or package.module format)')
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
