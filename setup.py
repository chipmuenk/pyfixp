# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
# see e.g. https://github.com/alttch/finac/blob/master/setup.py
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# version_nr contains ... well ... the version in the form  __version__ = '0.1b10'
version_nr = {}
with open(path.join(here, 'pyfixp/version.py'), encoding='utf-8') as f_v:
    exec(f_v.read(), version_nr)

# --- read requirements.txt, remove comments and unneeded modules
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f_r:
    requirements_list = f_r.read().strip().split("\n")

for p in requirements_list[:]:
    if p.startswith('#'):
        requirements_list.remove(p)
if 'nose' in requirements_list:
    requirements_list.remove('nose')

print("Installing packages\n{0}\n".format(requirements_list))

setup(
    name = 'pyfixp',
    version = version_nr['__version__'],
    description = 'pyfixp is a fast library for fixpoint (re)quantization.',
    long_description_content_type='text/markdown',
    #long_description_content_type='text/x-rst',
    long_description = long_description,
    keywords = ["fixpoint", "quantization", "requantization", "CSD"],
    url = 'https://github.com/chipmuenk/pyfixp',
    author = 'Christian Muenker',
    author_email = 'chipmuenk@gmail.com',
    license = 'MIT',
    platforms = ['any'],
    install_requires = requirements_list,

     # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Education',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    # automatically find top-level package and sub-packages
    packages = find_packages(exclude=('doc', 'test')),
    # Read information from MANIFEST.in
    include_package_data = True,
    # add additional data files (= non *.py) for package / subpackages relative
    # to package directory

    # link the executable pyfixp to running the python function main() in the
    # pyfdax module, with an attached terminal:
    entry_points = {
        'console_scripts': [
            'pyfixp = pyfixp.pyfixp:main',
        ]
    }
)
