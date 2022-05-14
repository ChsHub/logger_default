import setuptools
from distutils.core import setup
from logger_default import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='logger_default',
    version=__version__,
    description='long_description',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ChsHub',
    packages=['logger_default'],
    license='MIT License',
    classifiers=['Programming Language :: Python :: 3.7'],
    install_requires=['send2trash']
)
