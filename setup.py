import subprocess
from setuptools import setup, find_packages, Extension

setup(
    name='pgsparky',
    version='0.0.1',
    author='Shiti',
    license='Apache 2',
    packages=['pgsparky'],
    install_requires=[
        'multicorn',
    ]
)
