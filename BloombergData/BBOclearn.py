# Merge Ask prices and Bid prices
# Some data may do not have a trade column

import pandas as pd
import numpy  as np

def AB_Merge(data,type):
    ask_table = data[data.BBO.str.contains('ASK')]
    bid_table = data[data.BBO.str.contains('BID')]
    trade_table = data[data.BBO.str.contains('TRADE')]

    time_a = list(ask_table)[0]
    time_b = list(bid_table)[0]
    time_t = list(trade_table)[0]
    ask_tick = ask_table.groupby(time_a)
    bid_tick = bid_table.groupby(time_b)
    trade_tick = trade_table.groupby(time_t)
    ask_price = ask_tick['Price'].mean()
    bid_price = bid_tick['Price'].mean()
    trade_price = trade_tick['Price'].mean()
    ask_size = ask_tick['Size'].sum()
    bid_size = bid_tick['Size'].sum()
    trade_size = trade_tick['Size'].sum()
    ask_ = pd.DataFrame({'Ask_Price': ask_price, 'Ask_Size': ask_size},index = ask_price.index)
    bid_ = pd.DataFrame({'Bid_Price': bid_price, 'Bid_Size': bid_size},index = bid_price.index)
    trade_ = pd.DataFrame({'Trade_Price': trade_price, 'Trade_Size': trade_size}, index = trade_price.index)

    # Merge tick data
    nbbo_ = pd.merge(ask_,bid_,left_index = True, right_index = True, how = 'outer')
    nbbo_['Time_Index'] = pd.to_datetime(nbbo_.index)
    nbbo_ =  nbbo_.set_index('Time_Index',1)

    # Resample
    # We need to save the data after resampling
    # This is one way we did here, it may not efficiency but works
    nbbo = nbbo_.resample('s').fillna(method = None)

    nbbo['Ask_Price'] = nbbo['Ask_Price'].ffill()
    nbbo['Bid_Price'] = nbbo['Bid_Price'].ffill()
    nbbo['Ask_Size'] = nbbo['Ask_Size'].fillna(value = 0)
    nbbo['Bid_Size'] = nbbo['Bid_Size'].fillna(value = 0)

    nbbo[type + '_Price'] = 0.5*(nbbo['Ask_Price'] + nbbo['Bid_Price'])
    nbbo = nbbo.drop(['Ask_Price','Bid_Price','Ask_Size','Bid_Size'],1)

    if (type == 'Call' or type == 'Put'):
        return nbbo
    else:
        return (nbbo,trade_)


def nbbo_frame(asset,call,put):
    asset_call = pd.merge(asset,call, left_index = True, right_index = True, how = 'left')
    asset_call_put = pd.merge(asset_call, put, left_index = True, right_index = True, how = 'left')
    return(asset_call_put.dropna())
















