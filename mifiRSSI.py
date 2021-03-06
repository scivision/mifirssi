#!/usr/bin/env python
""" logs franklin Wireless MHS800L a.k.a. Verizon Ellipsis MiFi RSSI and connection status
simple example of parsing a jQuery driven site.
Not notable for efficiency.

Michael Hirsch
"""
import dryscrape #needed to get jQuery outputs
#
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
#
from mifirssi import readrssi,plotrssi
#

interval = 6 #match mifi [seconds]
baseurl = 'http://my.jetpack'
tailurl = '/about_jetpack/diagnostics.html'

def pollrssi(url,outfn,interval):
    outfn = Path(outfn).expanduser()

    dryscrape.start_xvfb()

    sess = setuphtml(url)

    outfn.write_text('time,status,rssi,sinr,bars')

    while True:
        html = sess.body()
        status,rssi,sinr,bars = parsehtml(html)
        line = f'{datetime.utcnow().strftime("%xT%X")},{status},{rssi},{sinr},{bars}\n'
        with outfn.open('a') as f:
            f.write(line)

        sleep(interval)


def setuphtml(url):
    try:
        s = dryscrape.Session(base_url=url)
    except FileNotFoundError as e:
        raise FileNotFoundError(f'pip install webkit-server    {e}')
    s.set_timeout(10)
    s.set_attribute('auto_load_images',False)
    print('waiting for page')
    s.visit(tailurl)
    print('page loaded')
    return s

def parsehtml(html):
    soup = BeautifulSoup(html,'lxml')
    #NOTE: next 2 lines may not be so efficient, but are expedient
    status = list(soup.findAll(id='NetworkStatus')[0].children)[0]
    rssi = str2num(soup,'RSSI')
    sinr = str2num(soup,'SINR')

    bars = getbars(soup)

    return status,rssi,sinr,bars

def str2num(soup,strn):
    #FIXME also candidate for speedup
    try:
        return float(list(soup.findAll(id=strn)[0].children)[0][:-3])
    except ValueError:
        return ''

def getbars(soup):
    imgs = soup.findAll('img')  # FIXME more efficient
    for i in imgs:
        try:
            if i['data-status']=='SignalStrength':
                return int(i['src'][-5])
        except KeyError:
            continue
    return ''

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-o','--outfn',help='name of .csv file to write',default='~/mifirssi.csv')
    p.add_argument('-p','--plotfn',help='name of .csv file to plot')
    p = p.parse_args()

    if p.plotfn:
        print('plotting',p.plotfn)
        dat = readrssi(p.plotfn,interval)
        plotrssi(dat)
    else: #record
        pollrssi(baseurl,p.outfn,interval)
