#!/usr/bin/env python
install_requires = ['numpy','pandas','matplotlib','seaborn','python-dateutil','webkit-server','xvfbwrapper','dryscrape']

from setuptools import setup,find_packages

#%% install
setup(name='mifirssi',
      packages=find_packages(),
      version='0.1.0',
	  description='Scrape RSSI from Verizon MIFI',
	  author='Michael Hirsch, Ph.D.',
	  url='https://github.com/scivision/mifirssi',
      install_requires=install_requires,
      python_requires='>=3.6',
	  )

