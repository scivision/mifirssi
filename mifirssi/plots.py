#!/usr/bin/env python3
from pathlib import Path
from dateutil.parser import parse
from datetime import timedelta
from pandas import read_csv,DataFrame
from numpy import nan,diff,nonzero
from matplotlib.pyplot import show,subplots
import seaborn as sns
sns.set_context('talk')

def readrssi(fn,interval):
    fn = Path(fn).expanduser()

    dat = read_csv(fn)

    t = [parse(t) for t in dat['time']]
    dt = diff(t)

    #TODO trying to handle big time jumps, different recordings to same file
    jumpind = nonzero(dt>timedelta(seconds=interval*10))[0]

    data = DataFrame(index=t[:jumpind[0]+1],data=dat.ix[:jumpind[0],1:].values,columns=dat.columns[1:])

    data['rssi'].where(data['rssi']<-10,nan,inplace=True)

    return data

def plotrssi(dat):
    t=dat.index.to_pydatetime()
    fg,axs = subplots(2,1,sharex=True)

    ax = axs[0]
    ax.plot(t,dat['sinr'].values)
    ax.set_ylabel('SINR [dB]')

    ax = ax.twinx()
    ax.plot(t,dat['rssi'].values,color='red')
    ax.set_ylabel('RSSI [dBm]')
    ax.grid(False)

    ax=axs[1]
    ax.step(t,dat['bars'].values)
    ax.set_ylabel('signal bars')

    ax.set_xlabel('time [local]')

    fg.suptitle('Verizon Mifi Signal Analysis',fontsize='xx-large')

   #fg.autofmt_xdate()

    show()