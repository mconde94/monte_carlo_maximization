import scipy
import pylab
import pandas as pd
import numpy as np
import fcts

args = {

    'file_name': 'SandPConstantDollars.dat',
    'window' : 0.001,
    'lag' : 2
}


def read_file_dat(file_name, sep=' '):
    data = []
    with open(file_name, 'r') as f:
        d = f.readlines()
        for i in d:
            k = i.rstrip().split(sep)
            data.append([float(i) if fcts.is_float(i) else fcts.try_to_fct(i, int, default=0) for i in k])

    data = np.array(data, dtype='O')
    df = pd.DataFrame(columns = ['day','price'])
    df['day'] = data[:, 0]
    df['day'] = df['day'].apply(lambda x: fcts.try_to_fct(x,int))
    df['price'] = data[:, 1]
    df['price'] = df['price'].apply(lambda x: fcts.try_to_fct(x,float))
    pylab.plot(df['day'], df['price'])
    pylab.show()
    return df['day'], df['price']

def PlotPHistogram(data, nbins=252):
    out =  pylab.hist(data, bins=nbins)
    pylab.show()
    return out

Volatitily= lambda data: data.var()


def main():
    pylab.figure(1)
    t, SP = read_file_dat(args['file_name'])
    diffs = 100*SP.diff(periods = args['lag'])

    pylab.figure(2)
    pylab.plot(t , diffs)
    pylab.show()

    pylab.figure(3)
    hist = PlotPHistogram(diffs)

    pylab.figure(4)
    log_diffs = np.log(diffs).diff(periods = args['lag'])
    log_hist = PlotPHistogram(log_diffs)

    pylab.figure(5)
    lags = [*range(1000)]
    volatilities = np.array([Volatitily(100*SP.diff(periods = lag)) for lag in lags])
    lags = np.array(lags)
    pylab.plot(lags,volatilities)
    pylab.show()