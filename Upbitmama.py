import time
import pyupbit
import datetime
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


access = "키"          # 본인 값으로 변경
secret = "키"          # 본인 값으로 변경
myToken = "키"

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
post_message(myToken,"#stock", "VET autotrade start")

while True:
    try:  
        url = "https://api.upbit.com/v1/candles/minutes/15"                             # #######################################  VET

        querystring = {"market":"KRW-VET","count":"500"}

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
     
    
        btc = get_balance("VET")
        print("VET autotrade start")
        print(rsi)
    
        if btc == None:           
           if rsi < 25:  # RSI 27 이하 일 때 매수
               krw = get_balance("KRW") 
               if krw > 1950000:
                   buy_result = upbit.buy_market_order("KRW-VET", 2000000)
                   post_message(myToken,"#stock", "VET buy : " +str(buy_result))
                   time.sleep(2)

        else:
            Current_price = pyupbit.get_current_price("KRW-VET")
            avg_buy_price = upbit.get_avg_buy_price("KRW-VET")
            dif = (avg_buy_price - Current_price) / avg_buy_price
            if rsi > 73: 
                sell_result = upbit.sell_market_order("KRW-VET", btc)
                post_message(myToken,"#stock", "VET sell : " +str(sell_result))
            elif dif > 0.42:
                sell_result = upbit.sell_market_order("KRW-VET", btc*0.9995)
                post_message(myToken,"#stock", "VET sell : " +str(sell_result))
                time.sleep(1)  
            time.sleep(1)

        url = "https://api.upbit.com/v1/candles/minutes/15"                    # #######################################  ETC

        querystring = {"market":"KRW-ETC","count":"500"}

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
     
    
        btc = get_balance("ETC")
        print("ETC autotrade start")
        print(rsi)
     
        if btc == None:           
           if rsi < 25:  # RSI 27 이하 일 때 매수
               krw = get_balance("KRW") 
               if krw > 1950000:
                   buy_result = upbit.buy_market_order("KRW-ETC", 2000000)
                   post_message(myToken,"#stock", "ETC buy : " +str(buy_result))
                   time.sleep(2)

        else:
            Current_price = pyupbit.get_current_price("KRW-ETC")
            avg_buy_price = upbit.get_avg_buy_price("KRW-ETC")
            dif = (avg_buy_price - Current_price) / avg_buy_price
            if rsi > 73: 
                sell_result = upbit.sell_market_order("KRW-ETC", btc)
                post_message(myToken,"#stock", "ETC sell : " +str(sell_result))
            elif dif > 0.42:
                sell_result = upbit.sell_market_order("KRW-ETC", btc*0.9995)
                post_message(myToken,"#stock", "ETC sell : " +str(sell_result))
                time.sleep(1)  
            time.sleep(1)
        url = "https://api.upbit.com/v1/candles/minutes/15"                # #######################################  KMD

        querystring = {"market":"KRW-KMD","count":"500"}

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
     
        
        btc = get_balance("KMD")
        print("KMD autotrade start")
        print(rsi)
      
        if btc == None:           
           if rsi < 27:  # RSI 27 이하 일 때 매수
               krw = get_balance("KRW") 
               if krw > 1950000:
                   buy_result = upbit.buy_market_order("KRW-KMD", 2000000)
                   post_message(myToken,"#stock", "KMD buy : " +str(buy_result))
                   time.sleep(2)
        else:
            Current_price = pyupbit.get_current_price("KRW-KMD")
            avg_buy_price = upbit.get_avg_buy_price("KRW-KMD")
            dif = (avg_buy_price - Current_price) / avg_buy_price
            if rsi > 73:
                sell_result = upbit.sell_market_order("KRW-KMD", btc)
                post_message(myToken,"#stock", "KMD sell : " +str(sell_result))
            elif dif > 0.42:
                sell_result = upbit.sell_market_order("KRW-KMD", btc*0.9995)
                post_message(myToken,"#stock", "KMD sell : " +str(sell_result))
                time.sleep(1)  
            time.sleep(1)

        url = "https://api.upbit.com/v1/candles/minutes/15"                  # #######################################  DAWN

        querystring = {"market":"KRW-DAWN","count":"500"}

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
     
    
        btc = get_balance("DAWN")
        print("DAWN autotrade start")
        print(rsi)
       
        if btc == None:           
           if rsi < 27:  # RSI 27 이하 일 때 매수
               krw = get_balance("KRW") 
               if krw > 1950000:
                   buy_result = upbit.buy_market_order("KRW-DAWN", 2000000)
                   post_message(myToken,"#stock", "DAWN buy : " +str(buy_result))
                   time.sleep(2)
        else:
            Current_price = pyupbit.get_current_price("KRW-DAWN")
            avg_buy_price = upbit.get_avg_buy_price("KRW-DAWN")
            dif = (avg_buy_price - Current_price) / avg_buy_price
            if rsi > 73:
                sell_result = upbit.sell_market_order("KRW-DAWN", btc)
                post_message(myToken,"#stock", "DAWN sell : " +str(sell_result))
            elif dif > 0.42:
                sell_result = upbit.sell_market_order("KRW-DAWN", btc*0.9995)
                post_message(myToken,"#stock", "DAWN sell : " +str(sell_result))
                time.sleep(1)  
            time.sleep(1)

        url = "https://api.upbit.com/v1/candles/minutes/15"                     # #######################################  MARO

        querystring = {"market":"KRW-MARO","count":"500"}

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
     
    
        btc = get_balance("MARO") 
        print("MARO autotrade start")
        print(rsi)
       
        if btc == None:           
           if rsi < 27:  # RSI 27 이하 일 때 매수
               krw = get_balance("KRW") 
               if krw > 1950000:
                   buy_result = upbit.buy_market_order("KRW-MARO", 2000000)
                   post_message(myToken,"#stock", "MARO buy : " +str(buy_result))
                   time.sleep(2) 
        else:
            Current_price = pyupbit.get_current_price("KRW-MARO")
            avg_buy_price = upbit.get_avg_buy_price("KRW-MARO")
            dif = (avg_buy_price - Current_price) / avg_buy_price
            if rsi > 73:
                sell_result = upbit.sell_market_order("KRW-MARO", btc)
                post_message(myToken,"#stock", "MARO sell : " +str(sell_result))
            elif dif > 0.42:
                sell_result = upbit.sell_market_order("KRW-MARO", btc*0.9995)
                post_message(myToken,"#stock", "MARO sell : " +str(sell_result))
                time.sleep(1)  
            time.sleep(1)

        url = "https://api.upbit.com/v1/candles/minutes/15"                      # #######################################  MANA

        querystring = {"market":"KRW-MANA","count":"500"}

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
     
    
        btc = get_balance("MANA")
        print("MANA autotrade start")
        print(rsi)
       
        if btc == None:           
           if rsi < 25:  # RSI 27 이하 일 때 매수
               krw = get_balance("KRW") 
               if krw > 1950000:
                   buy_result = upbit.buy_market_order("KRW-MANA", 2000000)
                   post_message(myToken,"#stock", "MANA buy : " +str(buy_result))
                   time.sleep(2)
        else:
            Current_price = pyupbit.get_current_price("KRW-MANA")
            avg_buy_price = upbit.get_avg_buy_price("KRW-MANA")
            dif = (avg_buy_price - Current_price) / avg_buy_price
            if rsi > 73:
                sell_result = upbit.sell_market_order("KRW-MANA", btc)
                post_message(myToken,"#stock", "MANA sell : " +str(sell_result))
            elif dif > 0.42:
                sell_result = upbit.sell_market_order("KRW-MANA", btc*0.9995)
                post_message(myToken,"#stock", "MANA sell : " +str(sell_result))
                time.sleep(1)
            time.sleep(1)

        url = "https://api.upbit.com/v1/candles/minutes/15"                    # #######################################  BTT

        querystring = {"market":"KRW-BTT","count":"500"}

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
     
    
        btc = get_balance("BTT")
        print("BTT autotrade start")
        print(rsi)
     
        if btc == None:           
           if rsi < 25:  # RSI 27 이하 일 때 매수
               krw = get_balance("KRW") 
               if krw > 1950000:
                   buy_result = upbit.buy_market_order("KRW-BTT", 2000000)
                   post_message(myToken,"#stock", "BTT buy : " +str(buy_result))
                   time.sleep(2)

        else:
            Current_price = pyupbit.get_current_price("KRW-BTT")
            avg_buy_price = upbit.get_avg_buy_price("KRW-BTT")
            dif = (avg_buy_price - Current_price) / avg_buy_price
            if rsi > 73: 
                sell_result = upbit.sell_market_order("KRW-BTT", btc)
                post_message(myToken,"#stock", "BTT sell : " +str(sell_result))
            elif dif > 0.42:
                sell_result = upbit.sell_market_order("KRW-BTT", btc*0.9995)
                post_message(myToken,"#stock", "BTT sell : " +str(sell_result))
                time.sleep(1)  
            time.sleep(1)
    
        url = "https://api.upbit.com/v1/candles/minutes/15"                     # #######################################  SC

        querystring = {"market":"KRW-SC","count":"500"}

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
     
    
        btc = get_balance("SC")
        print("SC autotrade start")
        print(rsi)
      
        if btc == None:           
           if rsi < 25:  # RSI 27 이하 일 때 매수
               krw = get_balance("KRW") 
               if krw > 1950000:
                   buy_result = upbit.buy_market_order("KRW-SC", 2000000)
                   post_message(myToken,"#stock", "SC buy : " +str(buy_result))
                   time.sleep(2700)

        else:
            Current_price = pyupbit.get_current_price("KRW-SC")
            avg_buy_price = upbit.get_avg_buy_price("KRW-SC")
            dif = (avg_buy_price - Current_price) / avg_buy_price
            if rsi > 73: 
                sell_result = upbit.sell_market_order("KRW-SC", btc)
                post_message(myToken,"#stock", "SC sell : " +str(sell_result))
            elif dif > 0.42:
                sell_result = upbit.sell_market_order("KRW-SC", btc*0.9995)
                post_message(myToken,"#stock", "SC sell : " +str(sell_result))
                time.sleep(1)  
            time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken,"#stock", e)
        time.sleep(1)
 

 
