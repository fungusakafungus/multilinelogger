import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "multilinelogger",
    version = "0.0.1",
    author = "Ilya Margolin",
    author_email = "ilya@ulani.de",
    description = ("multiline-capable /usr/bin/logger companion"),
    license = "BSD",
    py_modules = ["multilinelogger"],
    long_description=read('README.md'),

    entry_points = {
        'console_scripts': [
            'multilinelogger = multilinelogger:main',
        ],
    }
)

