from datetime import datetime
from MetaTrader5 import *
import matplotlib.pyplot as plt
from pytz import timezone
import plotly.graph_objects as go
import pandas as pd

# Timezone config
utc_tz = timezone('UTC')

# Connect to MT 5
MT5Initialize()
# Waiting for MT 5 establishes the connection to the trade server and sync the environment
MT5WaitForTerminal()

# Request connection status and parameters
print(MT5TerminalInfo())
# Get data on MT 5 version
print(MT5Version())

####################################################################################################################
# Functions to get ticks

def getTicks_StartDate_XTicks(currencyPair):
    #Request 1000 ticks from X currency pair            #(Year, Month, Day, Hour), Ticks
    currencyPair_ticks = MT5CopyTicksFrom(currencyPair, datetime(2019, 7, 30, 0), 1000, MT5_COPY_TICKS_ALL)
    # DATA processing
    print('{}(', len(currencyPair_ticks), ')'.format(currencyPair))
    for val in currencyPair_ticks[:10]: print(val)
    return currencyPair_ticks

def getTicks_DateTimeFrame(currencyPair):
    #Request ticks from X currency pair within 2019, 7, 30, 13:00 - 2019, 7, 31 13:00
    currencyPair_ticks = MT5CopyTicksRange(currencyPair, datetime(2019, 7, 30, 13), datetime(2019, 7, 31, 13), MT5_COPY_TICKS_ALL)
    print('{}(', len(currencyPair_ticks), ')'.format(currencyPair))
    for val in currencyPair_ticks[:10]: print(val)
    return currencyPair_ticks

####################################################################################################################
# Function to get rates
## Get bars from different symbols and currency pairs in a number of ways

def getRates_StartDate_TM1_XTicks(currencyPair):

    currencyPair_ticks = MT5CopyRatesFrom(currencyPair, MT5_TIMEFRAME_M1, datetime(2017, 2, 8, 15), 1000)
    print('eurusd_rates(', len(currencyPair_ticks), ')')
    for val in currencyPair_ticks[:10]: print(val)
    return currencyPair_ticks

def getRates_TM1_XTicks(currencyPair):
    currencyPair_rates = MT5CopyRatesFromPos(currencyPair, MT5_TIMEFRAME_M30, 0, 1000)
    print('eurrub_rates(', len(currencyPair_rates), ')')
    for val in currencyPair_rates[:10]: print(val)
    return currencyPair_rates

def getRates_TM1_DateTimeFrame(currencyPair):
    currencyPair_ticks = MT5CopyRatesRange(currencyPair, MT5_TIMEFRAME_H1, datetime(2019, 1, 1, 13), datetime(2019, 1, 1, 13))
    print('{}(', len(currencyPair_ticks), ')'.format(currencyPair))
    for val in currencyPair_ticks[:10]: print(val)
    return currencyPair_ticks


####################################################################################################################
#Functions ti plot candlesticks, ticks

def plotCandlesticks(data_rates):
    df = pd.DataFrame(list(data_rates))
    #print(df.head(2))
    fig = go.Figure(data=[go.Candlestick(x=df[0], #time
                    open=df[1], high=df[3], #open, high
                    low=df[2], close=df[4]) #low, close
                         ])
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()

def plotTicks(data):
    # Plotting ticks
    x_time = [x.time.astimezone(utc_tz) for x in data]
    # Prepare Bid and Ask arrays
    bid = [y.bid for y in data]
    ask = [y.ask for y in data]

    # Draw ticks on the chart
    plt.plot(x_time, ask, 'r-', label='ask')
    plt.plot(x_time, bid, 'g-', label='bid')
    # Set legends
    plt.legend(loc='upper left')
    # Header of chart
    plt.title('EURUSD ticks')

    # Display the chart
    plt.show()

####################################################################################################################
#Calling function to get data
#Others: #AUSUSE, #EURAUD, #EURRUB

#Retrun: Bis, ASK, Last, Volume
EURUSD_ticks = getTicks_DateTimeFrame("EURUSD")
#EURUSD_ticks = getTicks_StartDate_XTicks("EURUSD")
#################################################################

#Return: Open, Low, High, Close, Tick Volume, Spread, Real Volume
#EURUSD_ticks = getRates_StartDate_TM1_XTicks("EURUSD")
#EURUSD_Rates = getRates_TM1_XTicks("EURUSD")
#EURJPY_Rates = getRates_TM1_DateTimeFrame("EURJPY")
#################################################################

#Shut down connection of MT 5
MT5Shutdown()

#Call plotting
#plotCandlesticks(EURRUB_Rates)
plotTicks(EURUSD_ticks)