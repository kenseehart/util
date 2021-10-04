# Installation

```

cd .../asap # directory containing your repo clones
git clone git@192.168.115.252:asap/util.git
cd util
./install-util
```

This will ask for:
 - where to create the `util.pth` file in a dist-packages dir (to make the python modules visible to `import`).
 - where to put command wrappers so they are in `$PATH`
 
To test the installation:
```
whip whip
```
(should print the path of whip.py)

# Commands

## gmon - Reactively display all content in the specified directory

```
usage: gmon [-h] [-v] [-e] path

Reactively display all content in the specified directory

positional arguments:
  path        directory to monitor

optional arguments:
  -h, --help  show this help message and exit
  -v          show debugging output
  -e          raise exception on error
```

### Known issue

On **asapDev**, `gmon` doesn't work because `matplotlib.pyplot` fails to import due to GDK issues.

```
>>> import matplotlib.pyplot as plt
Unable to init server: Could not connect: Connection refused
Unable to init server: Could not connect: Connection refused

(.:2079744): Gdk-CRITICAL **: 16:35:31.557: gdk_cursor_new_for_display: assertion 'GDK_IS_DISPLAY (display)' failed
```

## mkdo - Install a python module as a command in the specified bin directory
```
usage: mkdo [-h] [-d D] name

install a python module command in the bin directory To install this the first time: $ python3 mkdo.py mkdo
my/bin/directory Now mkdo is a command, and my/bin/directory is the default location for new commands. To
install a python module (must be locatable by import) as a command: $ mkdo mycommand Then you can run your
command: $ mycommand ...args...

positional arguments:
  name        command name (python module name) or .wrapper to convert wrappers

optional arguments:
  -h, --help  show this help message and exit
  -d D        bin directory (default=location of mkdo command)

```

## mkpy - Create a python module boilerplate implementation of a command
```
usage: mkpy [-h] name

Create a python module boilerplate implementation of a command

- Recommended: use `mkdo` to install the command

positional arguments:
  name        command name

optional arguments:
  -h, --help  show this help message and exit

```

## whip - Locate a python module - like which, but for python modules
```
usage: whip.py [-h] name

Locate a python module - like which, but for python modules Gives the filename that will be loaded by `import`

positional arguments:
  name        module name

optional arguments:
  -h, --help  show this help message and exit
```

# Modules

## stringbreak - Allows you to set a universal breakpoint on a specified output string.

In your vscode debug console, type this:
```
import stringbreak; stringbreak.sbp('your string here')
```

Or add that to your code, perhaps activated by a command line option.

Either way, the debugger will break on any output to any file/stream with the substring `'your string here'`


## yamster - A reactive yaml store

```
from yamster import Yamster

mydata = Yamster('my_filename.yaml')

mydata.x = 5
z = mydata.z
```

### Known issues:

- Data does not react to file contents changing due to an external process.
- Callback mechanism not implemented yet

Let me know if there is a use case for these reactive features. They are easy to implement.
