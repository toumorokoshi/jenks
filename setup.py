#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup

setup(name='jenks',
      version='0.1',
      description='a jenkins command-line tool',
      long_description=open('README.rst').read(),
      author='Yusuke Tsutsumi',
      author_email='yusuke@yusuketsutsumi.com',
      url='http://toumorokoshi.github.io/jenks',
      packages=find_packages(),
      install_requires=[
          'docopt>=0.6.1',
          'jenkinsapi>=0.2.18',
          'pyyaml>=3.10'
      ],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7'
      ],
      entry_points={
          'console_scripts': [
              'jenks = jenks:main'
          ]
      },
      tests_require=['mock>=1.0.1', 'nose>=1.3.0', 'httpretty==0.6.5'],
      test_suite='nose.collector'
)
