'''Locate a python module - like which, but for python modules

Gives the filename that will be loaded by `import`
'''

# install-me # <- This command will be installed by the install script

import sys
import os
import argparse
import subprocess
from importlib.util import find_spec
from pathlib import Path

def get_package_from_script(module_name):
    """Get the package that a module script is using by running 'which' on it"""
    try:
        # Get the path to the module script
        which_result = subprocess.run(['which', module_name], capture_output=True, text=True)
        if which_result.returncode != 0:
            return None

        script_path = which_result.stdout.strip()

        # Read the script to extract the package
        cat_result = subprocess.run(['cat', script_path], capture_output=True, text=True)
        if cat_result.returncode != 0:
            return None

        script_content = cat_result.stdout.strip()

        # Parse the content to find the package
        if 'python -m ' in script_content:
            # Extract the package name (e.g., 'util' from 'python -m util.`basename "$0"`')
            parts = script_content.split('python -m ')[1].split('.')[0]
            return parts
    except Exception as e:
        print(f"Error getting package from script: {e}", file=sys.stderr)

    return None

def whip(name):
    # First try direct module lookup
    try:
        spec = find_spec(name)
        if spec and spec.loader:
            return spec.loader.get_filename(name)
    except (ImportError, AttributeError):
        pass

    # If that fails, try to find the package by running 'which' on the module name
    package = get_package_from_script(name)
    if package:
        # Try to find the module in that package
        try:
            package_module = f"{package}.{name}"
            spec = find_spec(package_module)
            if spec and spec.loader:
                return spec.loader.get_filename(package_module)
        except (ImportError, AttributeError):
            pass

    raise FileNotFoundError(name)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', help='module name')

    args = parser.parse_args()
    name = args.name
    try:
        print(whip(name))
    except FileNotFoundError:
        print(f'module {name} not found', file=sys.stderr)
        exit(1)

if __name__=='__main__':
    main()
