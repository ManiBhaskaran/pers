# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 15:59:39 2019

@author: lalitha
"""

import datetime
import pandas as pd
import json
from datetime import datetime, timedelta



rURL="https://www.mcxindia.com/backpage.aspx/GetCommoditywiseBhavCopy"
PayLoad="{'Symbol':'CRUDEOIL','Expiry':'19FEB2019','FromDate':'','ToDate':'','InstrumentName':'FUTCOM'}"
#Data="curr_id=8849&smlID=300060&header=Crude+Oil+WTI+Futures+Historical+Data&st_date=03%2F02%2F2006&end_date=02%2F02%2F2020&interval_sec=Daily&sort_col=date&sort_ord=DESC&action=historical_data"
#https://in.investing.com/instruments/HistoricalDataAjax
PatternRead= requests.post(rURL,
                                  headers={#'Cookie':'adBlockerNewUserDomains=1545933873; optimizelyEndUserId=oeu1545933885326r0.8381196045732737; _ga=GA1.2.1293495785.1545933889; __gads=ID=d6c605f22775c384:T=1545933894:S=ALNI_MbV20pH_Ga4kGvz2QBdrKhnTQtDsg; __qca=P0-530564802-1545933894749; r_p_s_n=1; G_ENABLED_IDPS=google; _gid=GA1.2.2065111802.1547570711; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A3%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A49774%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A32%3A%22%2Fcommodities%2Fcrude-oil%3Fcid%3D49774%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228849%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Fcommodities%2Fcrude-oil%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228830%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A17%3A%22%2Fcommodities%2Fgold%22%3B%7D%7D%7D%7D; PHPSESSID=t127q9ns2htigac1b5j8lr2tdg; geoC=IN; comment_notification_204870192=1; gtmFired=OK; StickySession=id.51537812219.831in.investing.com; billboardCounter_56=1; nyxDorf=MDFkNWcvMG03YGBtN3pmZTJnNGs0LTI5YGY%3D; _fbp=fb.1.1547680426904.1355133887; ses_id=Nng3dm5hMDg0cGpsNGU1NzRhZDcyMmFjYmJhazo%2FZHJlcTQ6ZTIwdmFuaiRubTklMjQ3NjM3ZmYxM2JrO2xnMjZlNzZuPTBtNDdqZTQzNWE0Y2Q5MjJhamIxYWo6aWQ%2FZTc0N2UxMGZhZGpgbjM5YzIgNyszd2Z3MWNiMjt6ZyA2OTd2bj0wPzRhajA0NTVlNGFkOTI1YTJiamEwOmtkfGUu',
                                           'Referer':'https://www.mcxindia.com/market-data/bhavcopy',
                                           'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                                           ,'X-Requested-With': 'XMLHttpRequest'
                                           ,"Content-Type": "application/json"
                                           },
                                          data=PayLoad
                                  ) #GOLD
#PatternRead.text
PatternRead.json()['d']['Data']
Candles_df = pd.DataFrame(PatternRead.json()['d']['Data'])#Candles_dict,columns=['Date', 'open', 'high', 'low', 'close', 'V'])
Candles=Candles_df.iloc[:20]

Candles_df.iloc[:20][['Symbol','Date','Open','High','Low','Close']]
Candles_df.dtypes
#List_ = list(Candles_df['Date'])
#List_ = [datetime.strptime(MParseDate(x).strftime("%m/%d/%Y %I:%M %p"), "%m/%d/%Y %I:%M %p") for x in List_]
#Candles_df['Date']=pd.Series([x for x in List_],index=Candles_df.index)
#Candles_dict = Candles.json()['data']['candles']
#CrudeData1 = pd.read_html(PatternRead.text)[0]