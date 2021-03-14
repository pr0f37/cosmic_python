# Cosmic Python notes

[![Documentation Status](https://readthedocs.org/projects/cosmic-python-thoughts/badge/?version=latest)](https://cosmic-python-thoughts.readthedocs.io/en/latest/?badge=latest)

This is a training repository to practice techniques presented in the
[Architecture Patterns with Python](http://www.cosmicpython.com) book by Harry J.W Percival & Bob Gregory.

## Documentation

Check more detailed documentation at [read the docs!](https://cosmic-python-thoughts.readthedocs.io)

## Installation

### As a package

This code should be available as a pypi installation package.

```
TODO: pip installation command
```

## Local setup

To start working with code you need to set up your working environment. I strongly encourage you to use the following tools:

### Pyenv/Virtualenv

Pyenv is a tool which helps with installation and control of different versions of python on your machine.
Virtualenv is a matured and easy to use pyenv plugin which can group your python packages into virtual environments.
Virtualenv lets you isolate the project specific configuration from the system specific configuration which helps to
limit the packages only to the ones mandatory for the project and keep things clean and tidy.
Combining pyenv and virtualenv let you easily decide on the python versions you want to use and install on your system
as well as using them in your projects.

For installation instructions please visit:

* Pyenv: <https://github.com/pyenv/pyenv>
* Virtualenv: <https://github.com/pyenv/pyenv-virtualenv>

Please use python 3.9 and install all the necessary packages by:
```
pip install -r requirements.txt
```

### Pre-commit
Pre-commit checks & formats the code automatically against a list of configured and preinstalled hooks.
The list of default hooks for this repository is available in the `.pre-commit-config.yaml` file.

To install the pre-commit package:

```
pip install pre-commit
```

To install git hooks in your repository:

```
pre-commit install
```

After installation pre-commit will start automatically running a set of checks after every ``git commit`` command.

# License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
