#!/usr/bin/env python
req = ['numpy','pandas','matplotlib','seaborn','python-dateutil']
pipreq = ['webkit-server','xvfbwrapper','dryscrape']
import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e:
    pip.main(['install'] + req)
pip.main(['install'] + pipreq)
#
from setuptools import setup #enables develop

#%% install
setup(name='mifirssi',
      packages=['mifirssi'],
      version='0.1',
	  description='Scrape RSSI from Verizon MIFI',
	  author='Michael Hirsch, Ph.D.',
	  url='https://github.com/scivision/mifirssi',
	  )

