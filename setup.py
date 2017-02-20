#!/usr/bin/env python3
from setuptools import setup #enables develop

#%% install
setup(name='mifirssi',
      version='0.1',
	  description='Scrape RSSI from Verizon MIFI',
	  author='Michael Hirsch, Ph.D.',
	  url='https://github.com/scivision/mifirssi',
      install_requires=['xvfbwrapper','dryscrape',
                'pandas','matplotlib'],
      packages=['mifirssi'],
	  )

