#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='mercurio',
      version='0.1',
      description='Transmits messages between the arduino box and this listener',
      long_description='Transmit messages between Arduino and this listener',
      author='Alfredo Aguirre',
      author_email='alfredo@madewithbyt.es',
      scripts=['mercurio/mercurio-run.py'],
      license='MIT',
      eurl='http://github.com/alfredo/mercurio_listener/',
      include_package_data=True,
      classifiers=[
        'Development Status :: 0.1 Alpha',
        'Intended Audience :: Makers',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
      ],
      packages=find_packages(exclude=['tests']),
      requires=['pyserial', 'clint'],
      install_requires=['pyserial', 'clint'],
      )
