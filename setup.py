#!/usr/bin/env python3

from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='ccsi',
    version='0.1',
    description='Copernicus Core Service Interface',
    author='Michal opletal',
    author_email='michal.opletal@gisat.cz',
    long_description=readme(),
    packages=find_packages(),
    install_requires=[
        'flask==1.1.2',
        'setuptools==45.1.0'
    ],
    zip_safe=False,
    package_data={"": ["*.json"]},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    entry_points='',
    scripts=[]
)