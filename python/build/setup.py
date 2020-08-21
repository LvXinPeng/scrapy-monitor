from setuptools import setup, find_packages
from os import path, environ

from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='scrapy-monitor',
    version=0.1,
    description='scrapy monitor',
    author='Roc',
    author_email='lvxinpeng1996@126.com',
    python_requires='<3',
    install_requires=[
        'arrow==0.15.7',
        'attrs==19.3.0',
        'Automat==20.2.0',
        'backports.functools-lru-cache==1.6.1',
        'cffi==1.14.0',
        'constantly==15.1.0',
        'cryptography==2.9.2',
        'cssselect==1.1.0',
        'hyperlink==19.0.0',
        'idna==2.9',
        'incremental==17.5.0',
        'lxml==4.5.0',
        'parsel==1.6.0',
        'pyasn1==0.4.8',
        'pyasn1-modules==0.2.8',
        'pycparser==2.20',
        'PyDispatcher==2.0.5',
        'PyHamcrest==1.9.0',
        'pymongo==3.10.1',
        'PyMySQL==0.9.3',
        'python-dateutil==2.8.1',
        'queuelib==1.5.0',
        'Scrapy==1.8.0',
        'service-identity==18.1.0',
        'six==1.15.0',
        'Twisted==20.3.0',
        'w3lib==1.21.0',
        'zope.interface==5.1.0'
    ],
)
