#!/usr/bin/env python
from setuptools import setup, find_packages

install_reqs = []

## install main application
desc = 'A fast thermodynamics-based program for checking PCR primer specificity'
setup(
    name = 'MFEprimer',
    version = '2.0',
    description = desc,
    long_description = desc + '\n See README for more information.',
    author = 'Wubin Qu',
    author_email = 'quwubin@gmail.com',
    install_requires = install_reqs,
    license = "MIT license",
    packages = find_packages(),
    package_dir = {'MFEprimer':
                   'MFEprimer'},
    scripts = ['scripts/MFE_primer.py'],
    url = 'https://github.com/quwubin/MFEprimer'
)




