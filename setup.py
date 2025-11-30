from setuptools import find_packages, setup

setup(
    name='livpylib',
    packages=find_packages(
        include=['livpylib']
    ),
    version='1.0.0',
    description='liv\'s library!',
    author='livkaminske'
)

"""
To Build:

1. move terminal wd to the root of this dir

2. python3 setup.py bdist_wheel

3. pip install path/to/wheelfile.whl (should be in dist folder here)

"""