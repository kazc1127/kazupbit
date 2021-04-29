import time
import pyupbit
import datetime
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


myToken = "키"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

post_message(myToken,"#stock","240분봉 매수 종목 검색시작")
tickers = pyupbit.get_tickers(fiat="KRW")
while True:
    def rsiindex(symbol):
        url = "https://api.upbit.com/v1/candles/minutes/240"

        querystring = {"market":symbol,"count":"500"}

        response = requests.request("GET", url, params=querystring)

        data = response.json()

        df = pd.DataFrame(data)

        df=df.reindex(index=df.index[::-1]).reset_index()

        df['close']=df["trade_price"]


        def rsi(ohlc: pd.DataFrame, period: int = 9):
           ohlc["close"] = ohlc["close"]
           delta = ohlc["close"].diff()

           up, down = delta.copy(), delta.copy()
           up[up < 0] = 0
           down[down > 0] = 0

           _gain = up.ewm(com=(period - 1), min_periods=period).mean()
           _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

           RS = _gain / _loss
           return pd.Series(100 - (100 / (1 + RS)), name="{0} period RSI".format(period))

        rsi = rsi(df, 9).iloc[-1]
        time.sleep(1)   
        if rsi < 27:
         print(symbol)
         print('Upbit 240 minute RSI:', rsi)
         post_message(myToken,"#stock","240분봉 매수 타이밍"+symbol)

        
    for ticker in tickers:
        rsiindex(ticker)

        

    
  

 
