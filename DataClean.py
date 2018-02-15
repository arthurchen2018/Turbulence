# This code is designed for data manipulation (Bloomberg)
# 2018-Feb-10
# McMaster University
# cheny312@mcmaster.ca

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob as glob
import BloombergData.BBOclearn as bb
from datetime import datetime

Script_path = os.path.dirname(os.path.abspath("__file__"))
in_path = 'raw_data'
os.chdir(in_path)
out_path = os.path.abspath(os.path.join(os.path.dirname("__file__"),".."))
names = glob.glob('*.csv')

# 2018010220180216ABCDE60K43Y.csv:
# [0,7) Date of event: 20180102
# Date of maturity: 20180216
# Stock symbol: ABCDE (or ABCXX, if the length of symbol string less than 5)
# Strike price: 60
# Interest rate: 1.43%
# Y: NYSE, A: NASDAQ, E:ETF, C: Commodity

for name in names:
    date = name[0:8]
    expiry = name[8:16]
    symbol = name[16:21]
    strike = name[21:name.find('K')]
    interest = name[name.find('K')+1:name.find('.csv')-1]
    data = pd.read_csv(name, delimiter=',',low_memory=False)
    ''' For large Dataset only '''
    # large_ask = data.iloc[:,0:4].copy().dropna(); large_ask.columns = ['Asset','BBO','Price','Size'];
    # large_bid = data.iloc[:,15:19].copy().dropna(); large_bid.columns = ['Asset','BBO','Price','Size'];
    # asset_ = large_ask.append(large_bid)

    asset_ = data.iloc[:,0:4].copy().dropna(); asset_.columns = ['Asset','BBO','Price','Size']
    call_ = data.iloc[:,5:9].copy().dropna(); call_.columns = ['Call','BBO','Price','Size']
    put_ = data.iloc[:,10:14].copy().dropna(); put_.columns = ['Put','BBO','Price','Size']
    call = bb.AB_Merge(call_, 'Call')
    put =  bb.AB_Merge(put_,'Put')
    [asset,trade] = bb.AB_Merge(asset_,'Asset')
    nbbo_data = bb.nbbo_frame(asset,call,put)
    nbbo_data['K'] = float(strike)
    nbbo_data['Int'] = (1 + float(interest)/100)/100
    nbbo_data['TtM'] = ((datetime.strptime(expiry, '%Y%m%d') - datetime.strptime(date, '%Y%m%d')).days)/365
    bbo_name = 'BBO' + name

#
# Script_path = os.path.dirname(os.path.abspath("__file__"))

    nbbo_data.to_csv(os.path.join(out_path,'BBO_data', bbo_name))









