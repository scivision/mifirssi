#!/usr/bin/env python3
from setuptools import setup #enables develop
import subprocess


with open('README.rst','r') as f:
	  long_description = f.read()

#%% install
setup(name='mifirssi',
      version='0.1',
	  description='Scrape RSSI from Verizon MIFI',
	  long_description=long_description,
	  author='Michael Hirsch',
	  url='https://github.com/scivision/mifirssi',
      install_requires=['dryscrape'],
      packages=['mifirssi'],
	  )

try:
    subprocess.run(['conda','install','--yes','--quiet','--file','requirements.txt']) #don't use os.environ
except Exception as e:
    print('you will need to install packages in requirements.txt  {}'.format(e))
