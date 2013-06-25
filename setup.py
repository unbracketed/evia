"""
Evia
-------------

A library of utilities for working with cryptocurrency markets
"""
from setuptools import setup


setup(
    name='evia',
    version='0.1',
    url='http://github.com/unbracketed/evia',
    license='BSD',
    author='Brian Luft',
    author_email='brian@unbracketed.com',
    description='A library of utilities for working with cryptocurrency markets',
    long_description=__doc__,
    packages=['evia'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'ws4py',
        'sqlalchemy'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)