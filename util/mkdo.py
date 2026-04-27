r'''Install a Python module (or other command) as an executable wrapper.

`mkdo` creates executable command wrappers in a `bin/` directory.

The default behavior wraps a Python module so it can be run by name (no `.py`,
unified import semantics via `python -m`). With `-t/--template` you can install
arbitrary wrapper styles — see TEMPLATES below.

USAGE:

  Initial setup:
  $ python3 mkdo.py mkdo /path/to/bin

  This installs mkdo itself as a command, with /path/to/bin as the
  default location for new commands.

  Creating commands:
  $ mkdo module_name             # default template: `python -m module_name`
  $ mkdo package.module          # default template: `python -m package.module`
  $ mkdo -t vertical foo         # use the `vertical` template instead

  The created command can be run directly:
  $ module_name [arguments]

TEMPLATES:

  Templates are looked up in two places, in order:
    1. <bin_dir>/.templates/<template>
    2. <util-package>/mkdo_templates/<template>   (shipped with mkdo)

  If the template is found in (2) but not (1), it is copied into (1) on first
  use so the project ends up owning a local copy that can be edited.

  Template files are rendered with Python `str.format`, so literal `{` and `}`
  must be escaped as `{{` / `}}`. The default template uses one placeholder,
  `{package_prefix}` (e.g. "util." for `mkdo util.whip`, "" for `mkdo whip`).

  The default template requires the named module to be importable (so its
  optional `_mkdo_modules` attribute can drive recursive expansion). Other
  templates do not import the name and treat it as the literal command name.

mkdo (default template) requires that the module be importable from the
current Python environment.
'''

# install-me # <- This command will be installed by the setup script

import argparse
import importlib
import os
import shutil
import subprocess
import sys
from os.path import abspath, basename, dirname, exists, join, split, splitext

this_name = splitext(basename(__file__))[0]

DEFAULT_TEMPLATE = 'default'


def _resolve_bin_dir(bin_dir: str|None=None) -> str:
    if bin_dir:
        return bin_dir
    try:
        return dirname(subprocess.check_output(['which', this_name]).decode().strip())
    except subprocess.CalledProcessError:
        if 'VIRTUAL_ENV' in os.environ or 'CONDA_PREFIX' in os.environ:
            return split(sys.executable)[0]
        raise Exception(
            f'not in virtual or conda environment, so please use '
            f'python -m {this_name} {this_name} -d mybinpath'
        )


def _resolve_template(bin_dir: str, template: str) -> str:
    """Return path to the template file, bootstrap-copying from util's
    shipped templates into <bin_dir>/.templates/<template> if missing."""
    local = join(bin_dir, '.templates', template)
    if exists(local):
        return local
    shipped = join(dirname(__file__), 'mkdo_templates', template)
    if not exists(shipped):
        raise FileNotFoundError(
            f"template not found: {template!r} "
            f"(checked {local} and {shipped})"
        )
    os.makedirs(dirname(local), exist_ok=True)
    shutil.copyfile(shipped, local)
    print(f"[mkdo] installed template {template!r} -> {local}")
    return local


def _render_template(template_path: str, **ctx: str) -> str:
    with open(template_path) as f:
        body = f.read()
    return body.format(**ctx)


def mkdo(name: str, bin_dir: str|None=None, template: str = DEFAULT_TEMPLATE):
    if template == DEFAULT_TEMPLATE:
        # Recurse into _mkdo_modules if the imported module declares any.
        try:
            module = importlib.import_module(name)
            submodules = getattr(module, '_mkdo_modules', None)
            if submodules:
                print(f"[mkdo] Expanding '{name}' to submodules: {submodules}")
                results = []
                for sub in submodules:
                    full_sub = f"{name}.{sub}"
                    try:
                        results.append(mkdo(full_sub, bin_dir, template))
                    except Exception as e:
                        print(f"[mkdo] Failed to mkdo {full_sub}: {e}", file=sys.stderr)
                return results
        except Exception as e:
            # Module not importable → no _mkdo_modules to expand; proceed
            # with single install. Preserves prior best-effort behavior.
            print(f"[mkdo] note: could not import module {name}: {e}", file=sys.stderr)

    bin_dir = _resolve_bin_dir(bin_dir)

    if template == DEFAULT_TEMPLATE:
        if '.' in name:
            package, leaf = name.rsplit('.', 1)
            package_prefix = f'{package}.'
        else:
            leaf = name
            package_prefix = ''
        bin_name = leaf
        ctx = {'package_prefix': package_prefix, 'name': leaf}
    else:
        # Non-default templates: name is the literal command. Templates that
        # need the name embed it via `basename "$0"` or via the {name} field.
        bin_name = name
        ctx = {'package_prefix': '', 'name': name}

    print(f'installing {name} as {bin_name} in {bin_dir} (template={template})')

    template_path = _resolve_template(bin_dir, template)
    src = _render_template(template_path, **ctx)

    bin_path = abspath(join(bin_dir, bin_name))
    if exists(bin_path):
        os.unlink(bin_path)
    with open(bin_path, 'w') as f:
        f.write(src)
    os.chmod(bin_path, 0o755)
    return bin_path


def main():
    parser = argparse.ArgumentParser(
        prog=this_name,
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'name',
        help='command name (Python module / package.module for default template; '
             'literal command name for other templates)',
    )
    parser.add_argument('-d', help=f'bin directory (default=location of {this_name} command)')
    parser.add_argument(
        '-t', '--template',
        default=DEFAULT_TEMPLATE,
        help=f'template name (default: {DEFAULT_TEMPLATE!r}). Looked up in '
             '<bin>/.templates/<template>, falling back to mkdo_templates/ '
             'shipped with util (bootstrap-copied on first use).',
    )

    args = parser.parse_args()

    try:
        r = mkdo(args.name, args.d, args.template)
        if isinstance(r, list):
            for result in r:
                print(result)
        else:
            print(r)
    except Exception as e:  # Best if replaced with explicit exception
        print(e, file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
