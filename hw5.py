import os
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.api import Holt 
from statsmodels.tsa.stattools import adfuller

#Arda Sertkaya
#2293520

#I renamed the csv file for Madrid's data to madrid.csv for simplicity.
#reading Madrid's csv file but only Mean TemperatureC and CET(dates) columns.
filename = os.getcwd() + "\\madrid.csv"
df_madrid = pd.read_csv(filename, usecols=['Mean TemperatureC' , 'CET'])
#setting index in a datetime datatype
df_madrid['CET'] = pd.to_datetime(df_madrid['CET'])
df_madrid = df_madrid.set_index('CET')
#changing column name to temp-madrid
df_madridnew = df_madrid.rename(columns={'Mean TemperatureC': 'temp-madrid'})

#resampling and getting monthly average
mmavg = df_madridnew.resample('M').mean()

#dropping nan values after resampling
mmavg.dropna(inplace=True)

#reading Brazil's csv file with specific colums such as temp and date since file is too large.

filename = os.getcwd() + "\\sudeste.csv"
df_brazil = pd.read_csv(filename, usecols=['temp' , 'date'])
#First I need the Index in a datetime datatype
df_brazil['date'] = pd.to_datetime(df_brazil['date'])
#Index needs to be a DatetimeIndex in order to resample
df_brazil = df_brazil.set_index('date')
#changing column name
df_brazilnew = df_brazil.rename(columns={'temp': 'temp-brazil'})
#dropping 0's as they are nonvalues
df_brazilnewd = df_brazilnew.loc[~(df_brazilnew==0).all(axis=1)]

#resampling and getting monthly average
bmavg = df_brazilnewd.resample('M').mean()

#dropping nan values after resampling
bmavg.dropna(inplace=True)

#decomposing to see trends
def decomp(frame,name,f,mod='Additive'):
    #frame['Date'] = pd.to_datetime(frame['Date'])
    series = frame[name]
    array = np.asarray(series, dtype=float)
    result = sm.tsa.seasonal_decompose(array,freq=f,model=mod,two_sided=False)
    # Additive model means y(t) = Level + Trend + Seasonality + Noise
    result.plot()
    plt.show() 
    return result


#Testing to see stationary
def test_stationarity(timeseries):
    #Determing rolling statistics
    rolmean = pd.Series(timeseries).rolling(window=12).mean()
    rolstd = pd.Series(timeseries).rolling(window=12).std()
    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    #Perform Dickey-Fuller test:
    print("Results of Dickey-Fuller Test:")
    array = np.asarray(timeseries, dtype='float')
    np.nan_to_num(array,copy=False)
    dftest = adfuller(array, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)

#testing brazil
seriesname = 'temp-brazil'
result = decomp(bmavg,seriesname,f=12)
test_stationarity(result.trend)
#test_stationarity(result.seasonal)

#testing madrid
seriesname = 'temp-madrid'
result = decomp(mmavg,seriesname, f=12)
test_stationarity(result.trend)
#test_stationarity(result.seasonal)

#There is seasonality in both datasets. When it is decomposed and eliminated
#we can see in both datasets that there is an increasing trend after time 195
#By Dickey-Fuller Test we can see that temp Brazil data have a p-value > 0.05
#so that it is non-stationary but Madrid data have p-value <= 0.05 so data is
#stationary.


