import time
import pyupbit
import datetime
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

access = "d"          # 본인 값으로 변경
secret = "d"          # 본인 값으로 변경
myToken = "d"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)

# 시작 메세지 슬랙 전송
post_message(myToken,"#stock", "Kazbit autotrade start")
print("Kazbit autotrade start")


while True:
  coins = ["VET", "ETC", "KMD", "DAWN", "MARO", "MANA", "BTT", "SC", "OMG", "EOS"] # "PUNDIX", "STMX", 
  for coin in coins :
 
          
      url = "https://api.upbit.com/v1/candles/minutes/15"

      querystring = {"market":"KRW-"+coin,"count":"500"}
            
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
      btc = get_balance(coin)

      def RB(coin):
        if coin == "VET":
          return 27
        elif coin == "ETC":
          return 27
        elif coin == "KMD":
          return 27
        elif coin == "DAWN":
          return 27
        elif coin == "MARO":
          return 27
        elif coin == "MANA":
          return 27
        elif coin == "BTT":
          return 25
        elif coin == "SC":
          return 25
        elif coin == "OMG":
          return 25
        elif coin == "PUNDIX":
          return 25
        elif coin == "STMX":
          return 22
        elif coin == "EOS":
          return 22
        else:
          return 0

      def RQ(coin):
        if coin == "VET":
          return 73
        elif coin == "ETC":
          return 73
        elif coin == "KMD":
          return 73
        elif coin == "DAWN":
          return 73
        elif coin == "MARO":
          return 73
        elif coin == "MANA":
          return 75
        elif coin == "BTT":
          return 73
        elif coin == "SC":
          return 73
        elif coin == "OMG":
          return 73
        elif coin == "PUNDIX":
          return 73
        elif coin == "STMX":
          return 73
        elif coin == "EOS":
          return 73
        else:
          return 0
        
      if btc == None:          
         if rsi < RB(coin):  # RSI 27 이하 일 때 매수
            krw = get_balance("KRW") 
            if krw > 5000:
               buy_result = upbit.buy_market_order("KRW-"+coin, 10000)
               time.sleep(1)

      else:
         Current_price = pyupbit.get_current_price("KRW-"+coin)
         avg_buy_price = upbit.get_avg_buy_price("KRW-"+coin)
         dif = (avg_buy_price - Current_price) / avg_buy_price
         if rsi > RQ(coin): 
            sell_result = upbit.sell_market_order("KRW-"+coin, btc)
            post_message(myToken,"#stock", coin+" sell : " +str(sell_result))
         elif dif > 0.42:
            sell_result = upbit.sell_market_order("KRW-"+coin, btc*0.995)
            post_message(myToken,"#stock", coin+" sell : " +str(sell_result))
            time.sleep(1)  
      time.sleep(1)

      
