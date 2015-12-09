#!/usr/bin/env python3
""" logs franklin Wireless MHS800L a.k.a. Verizon Ellipsis MiFi RSSI and connection status
simple example of parsing a jQuery driven site.
Not notable for efficiency.

Michael Hirsch
"""
import dryscrape #needed to get jQuery outputs
dryscrape.start_xvfb()
#
from pathlib2 import Path
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
interval = 6 #match mifi
url = 'http://my.jetpack'
outfn = '~/mifirssi.csv'

def pollrssi(url,outfn,interval):
    outfn = Path(outfn).expanduser()
    
    sess = setuphtml(url)
    
    while True:
        html = sess.body()
        status,rssi,sinr,bars = parsehtml(html)
        line = '{},{},{},{},{}\n'.format(datetime.utcnow().strftime('%xT%X'),status,rssi,sinr,bars)
        with open(str(outfn),'a') as f:
            f.write(line)
            
        sleep(interval)
        

def setuphtml(url):
    s = dryscrape.Session(base_url=url)
    s.set_timeout(10) 
    s.set_attribute('auto_load_images',False)
    print('waiting for page')
    s.visit('/about_jetpack/diagnostics.html')
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
    imgs = soup.findAll('img') #FIXME more efficient
    for i in imgs:
        try:
            if i['data-status']=='SignalStrength':
                return int(i['src'][-5])
        except KeyError:
            continue
    return ''
    
if __name__ == '__main__':
    pollrssi(url,outfn,interval)