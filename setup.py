__author__ = 'Paul Severance'

from setuptools import setup

setup(
    name='python-cayley',
    version='0.0.1',
    author='Paul Severance',
    author_email='paulseverance@gmail.com',
    packages=['src'],
    description='A synchronous Cayley client.',
    install_requires=[
        'requests',
        'pyley'
    ],
    dependency_links=[
        'git+https://github.com/sugarush/pyley.git@411e4eaf6ed3e91175e2c6b22833693fbcf6a370#egg=pyley'
    ]
)
