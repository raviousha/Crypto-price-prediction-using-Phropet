# -*- coding: utf-8 -*-
"""Cardano price prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/125AdlCVWseDOkGjA_wd7VL9GD9mbGVTQ
"""

!pip install yfinance

import pandas as pd
import yfinance as yf
from datetime import datetime
from datetime import timedelta
import plotly.graph_objects as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import warnings
warnings.filterwarnings('ignore')
pd.options.display.float_format = '${:,.2f}'.format

today = datetime.today().strftime('%Y-%m-%d')
start_date = '2010-01-01'
"""
change ADA to any crypto abbreviation that being served by yfinance
source can be seen from https://finance.yahoo.com/cryptocurrencies
"""
ada_df = yf.download('ADA-USD',start_date, today)
ada_df.tail()

ada_df.info()

ada_df.isnull().sum()

ada_df.reset_index(inplace=True)
ada_df.columns

df = ada_df[["Date", "Open", "High", "Close", "Low"]]
new_names = {
    "Date": "ds", 
    "Open": "y",
    "High": 'hi',
    "Close": 'cl',
    "Low": 'lo'
}
df.rename(columns=new_names, inplace=True)

df.tail()

x = df["ds"]
y = df["y"]
fig = go.Figure(data=[go.Candlestick(x=df["ds"],
                open=df['y'],
                high=df['hi'],
                low=df['lo'],
                close=df['cl'])])
#fig.add_trace(go.Scatter(x=x, y=y))
fig.update_layout(
    title_text="Crypto Price History",
)

m = Prophet(
    seasonality_mode="multiplicative"
)
m.fit(df)

future = m.make_future_dataframe(periods = 180)
future.tail()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

plot_plotly(m, forecast)

plot_components_plotly(m, forecast)
