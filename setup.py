#!/usr/bin/env python
from setuptools import setup, find_packages

install_reqs = []

scripts = [
    'scripts/MFE_primer.py',
    'scripts/faToTwoBit',
    'scripts/twoBitToFa',
    'scripts/mfe_index_db.py',
    'scripts/UniFastaFormat.py'
]

## install main application
desc = 'A fast thermodynamics-based program for checking PCR primer specificity (linux-specific)'
setup(
    name = 'MFEprimer_linux',
    version = '2.1.1',
    description = desc,
    long_description = desc + '\n See README for more information.',
    author = 'Nick Youngblut',
    author_email = 'nyoungb2@gmail.com',
    install_requires = install_reqs,
    license = "MIT license",
    packages = find_packages(),
    package_dir = {'MFEprimer':
                   'MFEprimer'},
    scripts = scripts,
    url = 'https://github.com/nick-youngblut/MFEprimer_linux'
)




