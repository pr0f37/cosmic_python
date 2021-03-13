===================
Cosmic Python notes
===================

.. image:: https://readthedocs.org/projects/cosmic-python-thoughts/badge/?version=latest
    :alt: Documentation Status
    :target: https://cosmic-python-thoughts.readthedocs.io/en/latest/?badge=latest

This is a training repository to practice techniques presented in the
`Architecture Patterns with Python <http://www.cosmicpython.com>`_ book by Harry J.W Percival & Bob Gregory.

Documentation
=============
Check more detailed documentation at readthedocs.org! (link will be added soon)

Installation
============
As a package
------------
This code should be available as a pypi installation package.

``TODO: pip installation command``

Contribution
============
If you want to contribute please clone the repository and submit your changes via pull request!

To start working you need to set up your working environment. I strongly encourage you to use the following tools:

Pyenv/Virtualenv
----------------
Pyenv is a tool which helps with installation and controll different vestions of python on your machine.
Virtualenv is matured and easy to use pyenv plugin which can group your python packages into virtual environments.
Virtualenv lets you isolate the project specific configuration from the system specific configuration which helps to
limit the packages only to the ones mandatory for the project and keep things clean and tidy.
Connecting pyenv and virtualenv let's you easily decide on the python versions you want to use and install on your system
as well as using those python installations in your projects virtual environments.

Installation
^^^^^^^^^^^^
For installation instructions please visit:

* Pyenv: `https://github.com/pyenv/pyenv`
* Virtualenv: `https://github.com/pyenv/pyenv-virtualenv`

After installation please choose python 3.9 and install all the necessary packages by:
``pip install -r requirements.txt``

Pre-commit
----------
Pre commit is a tool that checks & formats the code automatically against a list of configured and preinstalled hooks.
The list of default hooks for this repository is listed in the `.pre-commit-config.yaml` file.

Installation
^^^^^^^^^^^^
To install the pre commit package:

``pip install pre-commit``

To install git hooks in your repository:

``pre-commit install``

After installation pre-commit will automatically run a set of checks after `git commit` command.
