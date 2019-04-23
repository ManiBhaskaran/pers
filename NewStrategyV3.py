# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 08:01:35 2019

@author: lalitha
"""
import math
from candlestick import candlestick
import datetime
import pandas as pd
import json
import time
#from datetime import timedelta  
from datetime import datetime, timedelta
import requests
from dateutil.parser import parse
import plotly.graph_objs as go
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import plotly.io as pio
import os
from plotly.tools import FigureFactory as FF

from datetime import datetime

        
def ProcessCandles(Df):
    #Df = candlestick.bearish_engulfing(Df)
    #Df = candlestick.bullish_engulfing(Df)
    Df = candlestick.three_inside_up(Df)
    Df = candlestick.three_inside_down(Df)
    Df = candlestick.three_outside_up(Df)
    Df = candlestick.three_outside_down(Df)
    Df['MovingAverageDown']=Df['low'].rolling(window=10).mean()
    Df['MovingAverageUp']=Df['high'].rolling(window=10).mean()
    Df['MovingAverage']=Df['close'].rolling(window=10).mean()
    #Df = candlestick.doji_star(Df)
    #Df = candlestick.bearish_harami(Df)
    #Df = candlestick.bullish_harami(Df)
    #Df = candlestick.doji(Df)

    return Df






def extractResultData(iResults1,date1,date2):
    global iResults
    iResults = iResults1[(iResults1['Date'] >= date1) & (iResults1['Date'] <= date2)]
    return iResults


    
def DisplayCandles1(CrudeData,DateIndex,Candle30Min,Candle15Min,Symbol):
#    global ResultMerge
#    global AnnotationsAr
#    getLiveData()    
    
    date1=parse(CrudeData.iloc[DateIndex-1]['Date'].strftime("%Y-%m-%d 04:00"))
    print(date1)
    if(OverRide==True):
        CurrentDate1=CrudeData.iloc[DateIndex]['Date']
        if((CurrentDate1.weekday()==4) ):
            date1=parse(N1(CurrentDate1,"3D","+").strftime("%Y-%m-%d 04:00"))
        #date1= parse("2019-02-04 04:00")
        #d2= parse("2019-01-30 03:00")
    #print("After " )
    
    #date1 = parse("2019-01-29 04:00")
    #date5 = parse("2019-01-30 12:30")
    date2 = N1(date1,"23H","+")
    
    print( str(date1) + " ----- " + str(date2))
    
    date3=parse(CrudeData.iloc[DateIndex]['Date'].strftime("%Y-%m-%d 04:00"))
    date4 = N1(date3,"23H","+")
    #date4 = parse("2019-01-30 12:30")
    
    
    #date1=N1(date1,"1D","-")
    #date2=N1(date2,"1D","-")
    
    
    # every monday
    
    quotes=Candle30Min    
    quotes15=Candle15Min
    
    #CrudeDf30Min.dtypes
    #quotes = pd.read_csv('SampleYData.csv',
    #                     index_col=0,
    #                     parse_dates=True,
    #                     infer_datetime_format=True)
    
    # select desired range of dates
    quotes = quotes[(quotes['Date'] >= date1) & (quotes['Date'] <= date2)]
    quotes15=quotes15[(quotes15['Date'] >= date1) & (quotes15['Date'] <= date2)]
    
#    iquotes = Candle30Min[(Candle30Min['Date'] >= date3) & (Candle30Min['Date'] <= date4)]
#    h=quotes['high'].max()
#    l=quotes['low'].min()
#    
#    
#    
#    ih=iquotes['high'].max()
#    il=iquotes['low'].min()
#    ic=iquotes['close'].iloc[-1]
#    iChartData=getPivots(ih,il,ic)
#    
#    #Merging the values to the Parent data
#    iChartData1={}
#    #iChartData1=iChartData
#    iChartData1['Date']=CrudeData.iloc[DateIndex]['Date'].strftime("%Y-%m-%d")#CrudeData.iloc[3+DateIndex]['Date']
#    iChartData1['AClose']=ic
#    iChartData1['APivot']=iChartData['Pivot']
#    i=1
#    while(i<=6):
#        iChartData1['AH'+str(i)]=iChartData['H'+str(i)]
#        iChartData1['AL'+str(i)]=iChartData['L'+str(i)]
#        i=i+1
#    
#    a=[]
#    a.append(iChartData1)
#    #pd.read_json(json.dumps(a)).dtypes
#    TestResult=pd.read_json(pd.Series(a).to_json(orient='values'))
#    ResultMerge=CrudeData.merge(TestResult)
    #ResultMerge=CrudeData.merge(pd.read_json(json.dumps(a)))
    #ResultMerge.iloc[0]
    
    #.......
    
#    iPivot=iChartData['Pivot']
#    iPriceList=list(iChartData.values())
#    iLowerList=iPriceList[7:]
#    iHigherList=iPriceList[1:7]
#    
    
    
    

    
    Lines=[]
    AnnotationsAr=[]
    Layout={}
    AxisText=[]
    AxisValue=[]
    AxisX=[]
    h=quotes['high'].max()
    l=quotes['low'].min()
    LowerList=[]
    HigherList=[]
    LowerMList=[]
    HigherMList=[]
    LowerMinList=[]
    HigherMinList=[]
    i=1
    while(i<=4):
        LowerList.append(CrudeData.iloc[DateIndex]['L'+str(i)])
        HigherList.append(CrudeData.iloc[DateIndex]['H'+str(i)])
        LowerMList.append(CrudeData.iloc[DateIndex]['L'+str(i-1)+"M1"])
        HigherMList.append(CrudeData.iloc[DateIndex]['H'+str(i-1)+"M1"])
        LowerMinList.append(CrudeData.iloc[DateIndex]['L'+str(i-1)+"M0"])
        LowerMinList.append(CrudeData.iloc[DateIndex]['L'+str(i-1)+"M2"])
        HigherMinList.append(CrudeData.iloc[DateIndex]['H'+str(i-1)+"M0"])
        HigherMinList.append(CrudeData.iloc[DateIndex]['H'+str(i-1)+"M2"])
        
        i=i+1
    Pivot=CrudeData.iloc[DateIndex]['IPivot']    
    Lines.append(CreateLines(date1,date2,Pivot,'rgb(255, 0, 0)',False))
    AxisText.append("Pivot ["+str(Pivot)+"]")
    AxisValue.append(Pivot)
        
    #plt.axhline(y=Pivot,linewidth=1, color='y',linestyle=":")
    #Diff=LowerList[4]-LowerList[3]
    Tolerance=round(l*0.25/100,0)
    even=1
    for Lower in LowerList:
        #Lower=LowerList[even]
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if((l-Tolerance)<Lower): #Change from 0.5 to 0.1
            Lines.append(CreateLines(date1,date2,Lower,'rgb(0, 0, 255)',False))
            AxisText.append("L"+str(even)+ " ["+str(Lower)+"]")
            AxisValue.append(Lower)
            
            AxisX.append(CurrentDate(N1(date1,"10M","-")))
        even=even+1
        
    even=1
    for Higher in HigherList:
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if(h+Tolerance>Higher):
            #plt.axhline(y=Higher,linewidth=1, color='g',linestyle=ls)
            Lines.append(CreateLines(date1,date2,Higher,'rgb(0, 255, 0)',False))
            AxisText.append("H"+str(even)+ " ["+str(Higher)+"]")
            AxisValue.append(Higher)
            AxisX.append(CurrentDate(N1(date1,"10M","-")))#            
        even=even+1 
    even=1
    for Lower in LowerMList:
        #Lower=LowerList[even]
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if((l-Tolerance)<Lower): #Change from 0.5 to 0.1
            Lines.append(CreateLines(date1,date2,Lower,'rgb(0, 0, 255)',True))
            AxisText.append("L"+str(even)+ "M ["+str(Lower)+"]")
            AxisValue.append(Lower)
            
            AxisX.append(CurrentDate(N1(date1,"10M","-")))
        even=even+1
        
    even=1
    for Higher in HigherMList:
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if(h+Tolerance>Higher):
            #plt.axhline(y=Higher,linewidth=1, color='g',linestyle=ls)
            Lines.append(CreateLines(date1,date2,Higher,'rgb(0, 255, 0)',True))
            AxisText.append("H"+str(even)+ "M ["+str(Higher)+"]")
            AxisValue.append(Higher)
            AxisX.append(CurrentDate(N1(date1,"10M","-")))#            
        even=even+1 
        
    for Lower in LowerMinList:
        #Lower=LowerList[even]
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if((l-Tolerance)<Lower): #Change from 0.5 to 0.1
            Lines.append(CreateLines(date1,date2,Lower,'rgb(0, 0, 255)',True))
            AxisText.append("L"+str(even)+ "Min ["+str(Lower)+"]")
            AxisValue.append(Lower)
            
            AxisX.append(CurrentDate(N1(date1,"10M","-")))
        even=even+1
        
    for Higher in HigherMinList:
        #Lower=LowerList[even]
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if((h+Tolerance)>Higher): #Change from 0.5 to 0.1
            Lines.append(CreateLines(date1,date2,Higher,'rgb(0, 255, 0)',True))
            AxisText.append("H"+str(even)+ "Min ["+str(Higher)+"]")
            AxisValue.append(Higher)
            
            AxisX.append(CurrentDate(N1(date1,"10M","-")))
        even=even+1
        
    trace0 = go.Scatter(x=AxisX,y=AxisValue,text=AxisText, mode='text')
    AxisText=[]
    AxisValue=[]
    AxisX=[]

    
    
    
        
        
    zi=0
    #while(zi<len(AxisValue)):
    #    AxisX.append(CurrentDate(date1))
    #    zi=zi+1
    
    
#    List_ = list(quotes['Date'])
#    #List_ = [N1(N1(x,"5H","+"),"30M","+") for x in List_]
#        
#    trace = go.Candlestick(x=List_,
#                           open=quotes['open'],
#                           high=quotes['high'],
#                           low=quotes['low'],
#                           close=quotes['close'])

    List_ = list(quotes15['Date'])
    trace = go.Candlestick(x=List_,
                           open=quotes15['open'],
                           high=quotes15['high'],
                           low=quotes15['low'],
                           close=quotes15['close'])    

    data=[trace,trace0]

    Layout["shapes"]=Lines
    Layout["annotations"]=AnnotationsAr
   
    
    #annotations
    
    fig = {
        'data': data,'layout': Layout
    }
    #,'layout': Layout
    #plt.axhline(y=Close,linewidth=1, color='b',linestyle="-")
    #pio.write_image(fig, 'fig1.png')
    #plot(fig,filename="Chart.html")
    plot(fig, filename="html/"+Symbol+"-IN-"+date1.strftime("%b-%d")+"V2.html",auto_open=False)
    print(Symbol+"-IN-"+date1.strftime("%b-%d")+"V2.html")
    
##getPivots
#rURL="https://in.investing.com/instruments/HistoricalDataAjax"
#Data="curr_id=8849&smlID=300060&header=Crude+Oil+WTI+Futures+Historical+Data&st_date=03%2F02%2F2006&end_date=02%2F02%2F2020&interval_sec=Daily&sort_col=date&sort_ord=DESC&action=historical_data"
##https://in.investing.com/instruments/HistoricalDataAjax
#PatternRead= requests.post(rURL,
#                                  headers={#'Cookie':'adBlockerNewUserDomains=1545933873; optimizelyEndUserId=oeu1545933885326r0.8381196045732737; _ga=GA1.2.1293495785.1545933889; __gads=ID=d6c605f22775c384:T=1545933894:S=ALNI_MbV20pH_Ga4kGvz2QBdrKhnTQtDsg; __qca=P0-530564802-1545933894749; r_p_s_n=1; G_ENABLED_IDPS=google; _gid=GA1.2.2065111802.1547570711; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A3%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A49774%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A32%3A%22%2Fcommodities%2Fcrude-oil%3Fcid%3D49774%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228849%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Fcommodities%2Fcrude-oil%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228830%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A17%3A%22%2Fcommodities%2Fgold%22%3B%7D%7D%7D%7D; PHPSESSID=t127q9ns2htigac1b5j8lr2tdg; geoC=IN; comment_notification_204870192=1; gtmFired=OK; StickySession=id.51537812219.831in.investing.com; billboardCounter_56=1; nyxDorf=MDFkNWcvMG03YGBtN3pmZTJnNGs0LTI5YGY%3D; _fbp=fb.1.1547680426904.1355133887; ses_id=Nng3dm5hMDg0cGpsNGU1NzRhZDcyMmFjYmJhazo%2FZHJlcTQ6ZTIwdmFuaiRubTklMjQ3NjM3ZmYxM2JrO2xnMjZlNzZuPTBtNDdqZTQzNWE0Y2Q5MjJhamIxYWo6aWQ%2FZTc0N2UxMGZhZGpgbjM5YzIgNyszd2Z3MWNiMjt6ZyA2OTd2bj0wPzRhajA0NTVlNGFkOTI1YTJiamEwOmtkfGUu',
#                                           'Referer':'https://in.investing.com/commodities/crude-oil-historical-data',
#                                           'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
#                                           ,'X-Requested-With': 'XMLHttpRequest'
#                                           ,"Content-Type": "application/x-www-form-urlencoded"
#                                           },
#                                          data=Data
#                                  ) #GOLD
#PatternRead.text
#CrudeData1 = pd.read_html(PatternRead.text)[0]
#i=-1
#Pivot=[]
#while(i<len(CrudeData1)-1):
#    i=i+1
#    #Res=getPivots(CrudeData1.iloc[i]['High'],CrudeData1.iloc[i]['Low'],CrudeData1.iloc[i]['Price'])
#    Res=getGoldPivots1(CrudeData1.iloc[i]['Open'],CrudeData1.iloc[i]['High'],CrudeData1.iloc[i]['Low'],CrudeData1.iloc[i]['Price'],"C",3,"All")
#    #getGoldPivots1(Open,High,Low,Close,Set,Option,Details)
#    #Res['Date']=CrudeData1.iloc[i]['Date']    
#    #Pivot.append(Res)
#    Res['Date']=CrudeData1.iloc[i]['Date']
#    Pivot.append(Res)
#
#List_ = list(CrudeData1['Date'])
#List_ = [datetime.strptime(parse(x).strftime("%m/%d/%Y %I:%M %p"), "%m/%d/%Y %I:%M %p") for x in List_]
#CrudeData1['Date']=pd.Series([x for x in List_],index=CrudeData1.index)
#Pivotdf=pd.read_json(json.dumps(Pivot))    
#CrudeData=CrudeData1.merge(Pivotdf)
#
#arSellCandles=[]
#arBuyCandles=[]
    
#def GetEODDataFromMCX():
#    rURL="https://www.mcxindia.com/backpage.aspx/GetCommoditywiseBhavCopy"
#    #PayLoad="{'Symbol':'CRUDEOIL','Expiry':'19FEB2019','FromDate':'','ToDate':'','InstrumentName':'FUTCOM'}"
#    if(Symbol=="GOLD"):
#        PayLoad="{'Symbol':'GOLD','Expiry':'05JUN2019','FromDate':'','ToDate':'','InstrumentName':'FUTCOM'}"
#    else:
#        PayLoad="{'Symbol':'SILVER','Expiry':'03MAY2019','FromDate':'','ToDate':'','InstrumentName':'FUTCOM'}"
#    #PayLoad="{'Symbol':'CRUDEOIL','Expiry':'19MAR2019','FromDate':'','ToDate':'','InstrumentName':'FUTCOM'}"
#    #Data="curr_id=8849&smlID=300060&header=Crude+Oil+WTI+Futures+Historical+Data&st_date=03%2F02%2F2006&end_date=02%2F02%2F2020&interval_sec=Daily&sort_col=date&sort_ord=DESC&action=historical_data"
#    #https://in.investing.com/instruments/HistoricalDataAjax
#    PatternRead= requests.post(rURL,
#                                      headers={#'Cookie':'adBlockerNewUserDomains=1545933873; optimizelyEndUserId=oeu1545933885326r0.8381196045732737; _ga=GA1.2.1293495785.1545933889; __gads=ID=d6c605f22775c384:T=1545933894:S=ALNI_MbV20pH_Ga4kGvz2QBdrKhnTQtDsg; __qca=P0-530564802-1545933894749; r_p_s_n=1; G_ENABLED_IDPS=google; _gid=GA1.2.2065111802.1547570711; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A3%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A49774%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A32%3A%22%2Fcommodities%2Fcrude-oil%3Fcid%3D49774%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228849%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Fcommodities%2Fcrude-oil%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228830%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A17%3A%22%2Fcommodities%2Fgold%22%3B%7D%7D%7D%7D; PHPSESSID=t127q9ns2htigac1b5j8lr2tdg; geoC=IN; comment_notification_204870192=1; gtmFired=OK; StickySession=id.51537812219.831in.investing.com; billboardCounter_56=1; nyxDorf=MDFkNWcvMG03YGBtN3pmZTJnNGs0LTI5YGY%3D; _fbp=fb.1.1547680426904.1355133887; ses_id=Nng3dm5hMDg0cGpsNGU1NzRhZDcyMmFjYmJhazo%2FZHJlcTQ6ZTIwdmFuaiRubTklMjQ3NjM3ZmYxM2JrO2xnMjZlNzZuPTBtNDdqZTQzNWE0Y2Q5MjJhamIxYWo6aWQ%2FZTc0N2UxMGZhZGpgbjM5YzIgNyszd2Z3MWNiMjt6ZyA2OTd2bj0wPzRhajA0NTVlNGFkOTI1YTJiamEwOmtkfGUu',
#                                               'Referer':'https://www.mcxindia.com/market-data/bhavcopy',
#                                               'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
#                                               ,'X-Requested-With': 'XMLHttpRequest'
#                                               ,"Content-Type": "application/json"
#                                               },
#                                              data=PayLoad
#                                      ) #GOLD
#    #PatternRead.text
#    PatternRead.json()['d']['Data']
#    Candles_df = pd.DataFrame(PatternRead.json()['d']['Data'])#Candles_dict,columns=['Date', 'open', 'high', 'low', 'close', 'V'])
#    return Candles_df.iloc[:40][['Symbol','Date','Open','High','Low','Close']]

#Data1=GetEODDataFromMCX()
#i=-1
#Pivot=[]
#while(i<len(Data1)-1):
#    i=i+1
#    #Res=getPivots(CrudeData1.iloc[i]['High'],CrudeData1.iloc[i]['Low'],CrudeData1.iloc[i]['Price'])
#    Res=getGoldPivots1(Data1.iloc[i]['Open'],Data1.iloc[i]['High'],Data1.iloc[i]['Low'],Data1.iloc[i]['Close'],"D",4,"All")
#    #Res=getGoldPivots1(CrudeData1.iloc[i]['Open'],CrudeData1.iloc[i]['High'],CrudeData1.iloc[i]['Low'],CrudeData1.iloc[i]['Price'])
#    #Res['Date']=CrudeData1.iloc[i]['Date']    
#    #Pivot.append(Res)
#    Res['Date']=Data1.iloc[i]['Date']
#    Pivot.append(Res)
#
#List_ = list(Data1['Date'])
#List_ = [datetime.strptime(parse(x).strftime("%m/%d/%Y %I:%M %p"), "%m/%d/%Y %I:%M %p") for x in List_]
#Data1['Date']=pd.Series([x for x in List_],index=Data1.index)
#Pivotdf=pd.read_json(json.dumps(Pivot))    
#CrudeData=Data1.merge(Pivotdf)
#CrudeData.iloc[1]
#
    
def ChartWithBreakOut(History,DataIndex,Candle15Min,Candle30Min,Symbol):
    #ChartWithBreakOut(GoldHistoryV1,DataIndex,GoldCandle15Min,GoldCandle30Min,Symbol+"V1")
#    History=GoldHistoryV1
#    Candle15Min=GoldCandle15Min
#    Candle30Min=GoldCandle30Min
    #Symbol=Symbol+"V1"
    candlestick.BreakOutSignals=[]
    candlestick.BreakOutLines=[]
    Temp=Candle15Min
    if(DataIndex==0):
        Date1=parse(candlestick.N1(History.iloc[DataIndex]['Date'],"1D","+").strftime("%Y-%m-%d 04:00"))
        Date2 = candlestick.N1(Date1,"23H","+")
        Temp1=Temp[(Temp['Date']>Date1) & (Temp['Date']<Date2)]
    else:
        Date1=History.iloc[DataIndex-1]['Date'].strftime("%Y-%m-%d 00:00")
        Date2=History.iloc[DataIndex-1]['Date'].strftime("%Y-%m-%d 23:30")
        Temp1=Temp[(Temp['Date']>parse(Date1)) & (Temp['Date']<parse(Date2))]
    quotes=Temp1
    PHigh=History.iloc[DataIndex]['High']
    PLow=History.iloc[DataIndex]['Low']
    ii=1
    Signals=[]
    Breakout=False
    Index=0
    while(ii<len(quotes)):
        Dlow=min(list(quotes['low'])[0:ii])
        Dhigh=max(list(quotes['high'])[0:ii])
        ii=ii+1
        if(candlestick.BreakOut(PHigh,PLow,Dhigh,Dlow,quotes.iloc[ii-1]['Date'])==True):
            if(Index==0):
                #print( " - " +str(quotes.iloc[ii-1]['Date'])+" Breakout Signal")
                Index=ii-1
            Breakout=True            
    BreakOutChartData=[]
    if(Breakout):
        print( " - " +str(quotes.iloc[Index-1]['Date'])+" Breakout Signal")
        BreakOutData=pd.DataFrame(candlestick.BreakOutSignals)
        #BreakOutChartData=candlestick.drawBreakOutChart(BreakOutData,Symbol+"V1.html",quotes,quotes.iloc[Index-1]['Date'],quotes.iloc[Index-1]['close'])
    Breakout=False
    candlestick.DisplayCandles(History,DataIndex,Candle30Min,Candle15Min,Symbol,False,Breakout,BreakOutChartData)
    
def getSpecificData(History,Temp,DataIndex):
    if(DataIndex==0):
        Date1=parse(candlestick.N1(History.iloc[DataIndex]['Date'],"1D","+").strftime("%Y-%m-%d 04:00"))
        Date2 = candlestick.N1(Date1,"23H","+")
        Temp1=Temp[(Temp['Date']>Date1) & (Temp['Date']<Date2)]
    else:
        Date1=History.iloc[DataIndex-1]['Date'].strftime("%Y-%m-%d 00:00")
        Date2=History.iloc[DataIndex-1]['Date'].strftime("%Y-%m-%d 23:30")
        Temp1=Temp[(Temp['Date']>parse(Date1)) & (Temp['Date']<parse(Date2))]
    return Temp1   

def getSpecificData1(History,Temp,DataIndex,Incr):
    if(DataIndex==0):
        Date1=parse(candlestick.N1(History.iloc[DataIndex]['Date'],str(Incr)+"D","+").strftime("%Y-%m-%d 04:00"))
        Date2 = candlestick.N1(Date1,"23H","+")
        Temp1=Temp[(Temp['Date']>Date1) & (Temp['Date']<Date2)]
    else:
        Date1=History.iloc[DataIndex-1]['Date'].strftime("%Y-%m-%d 00:00")
        Date2=History.iloc[DataIndex-1]['Date'].strftime("%Y-%m-%d 23:30")
        Temp1=Temp[(Temp['Date']>parse(Date1)) & (Temp['Date']<parse(Date2))]
    return Temp1 

def isInRange(History,DateIndex,Value,AllList,decimal,percentage):
    fPH=History.iloc[DateIndex]['High']
    fPL=History.iloc[DateIndex]['Low']
    Range=fPH-fPL
    
    tolerance=round(Range*percentage,decimal)
    for List in AllList:
        if(List-tolerance <= round(Value,decimal) <= List+tolerance):
            #print(str(Range*percentage)+" = " + str(List))
            return True
    return False
        
def getDoji(Candle1Min,DataIndex,History,Percent):
    
    Temp=Candle1Min[(Candle1Min['Doji']==True) & (Candle1Min['open']==Candle1Min['close'])]
    if(DataIndex==0):
        Date1=parse(candlestick.N1(History.iloc[DataIndex]['Date'],"1D","+").strftime("%Y-%m-%d 04:00"))
        Date2 = candlestick.N1(Date1,"23H","+")
        Temp1=Temp[(Temp['Date']>Date1) & (Temp['Date']<Date2)]
    else:
        Date1=History.iloc[DataIndex-1]['Date'].strftime("%Y-%m-%d 00:00")
        Date2=History.iloc[DataIndex-1]['Date'].strftime("%Y-%m-%d 23:30")
        Temp1=Temp[(Temp['Date']>parse(Date1)) & (Temp['Date']<parse(Date2))]
        
    History.iloc[DataIndex]['Date']
    
    i=0
    #tolerance=round(History.iloc[DataIndex]['Open']*Percent/10,2)
    Range=History.iloc[DataIndex]['High']-History.iloc[DataIndex]['Low']
    tolerance=round(Range*Percent,2)
    while(i<len(Temp1)):
        for Range in list(History.iloc[DataIndex])[6:]:
            O=Temp1.iloc[i]['open']
            H=Temp1.iloc[i]['high']
            L=Temp1.iloc[i]['low']
            if(Range-tolerance <= O <= Range+tolerance):
                #print(str(Range) + " - " + str(Temp1.iloc[i]['Date'])+ " - " + str(O) + " - " + str(i))
                indx=Temp1.index[i]
                #print(indx)
                #print(Temp1.iloc[i].Index)
                if((indx-10)>0):
                    Highs=Candle1Min.iloc[indx-10:indx-1]['high'].max()
                    #print(Candle1Min.iloc[indx-10:indx]['high'])
                    Lows=Candle1Min.iloc[indx-10:indx-1]['low'].max()                    
                    print(str(Range) + " - " + str(Temp1.iloc[i]['Date'])+ " - " + str(O) + " - " + str(Highs) +" - "+str(H>Highs) + " - " + str(Lows)+" - "+ str(L<Lows))
        i=i+1


def BreakOut(previousDayHigh,previousDayLow,todayHigh,todayLow):
    #global Signals
    Signal={}
#previousDayHigh=199.5
#previousDayLow=194.4
#todayHigh=194.65
#todayLow=192.75
    profitPercent =0.7*.01
    stopLossPercent=0.8*.01
    mulFactor1 = 0.45
    mulFactor2 = 0.75
    factor1 = mulFactor1 * (previousDayHigh - previousDayLow)
    factor2 = mulFactor2 * (previousDayHigh - previousDayLow)
    buyAt =0
    buyTarget =0
    buyStopLoss =0
    sellAt =0
    sellTarget =0
    sellStopLoss =0
    NoData=False
    message=" ==> "
    if ((todayHigh - todayLow) < factor1):
        buyAt = todayLow + factor1;
        buyTarget = todayLow + factor1 + (todayLow + factor1) * profitPercent;
        buyStopLoss = todayLow + factor1 - (todayLow + factor1) * stopLossPercent;
        sellAt = todayHigh - factor1;
        sellTarget = todayHigh - factor1 - (todayHigh - factor1) * profitPercent;
        sellStopLoss = todayHigh - factor1 + (todayHigh - factor1) * stopLossPercent
    elif(((todayHigh - todayLow) > factor1) and ((todayHigh - todayLow) < factor2)):
        buyAt = todayLow + factor2;
        buyTarget = todayLow + factor2 + (todayLow + factor2) * profitPercent;
        buyStopLoss = todayLow + factor2 - (todayLow + factor2) * stopLossPercent;
        sellAt = todayHigh - factor2;
        sellTarget = todayHigh - factor2 - (todayHigh - factor2) * profitPercent;
        sellStopLoss = todayHigh - factor2 + (todayHigh - factor2) * stopLossPercent
    else:
        NoData=True
    Signal["WHigh"]=todayHigh
    Signal["WLow"]=todayLow
    Signal['Buy']=math.ceil(buyAt* 100) / 100
    Signal['BuyT']=math.ceil(buyTarget* 100) / 100
    Signal['BuySL']=math.ceil(buyStopLoss* 100) / 100
    Signal['Sell']=math.ceil(sellAt* 100) / 100
    Signal['SellT']=math.ceil(sellTarget* 100) / 100
    Signal['SellSL']=math.ceil(sellStopLoss* 100) / 100
    Signal['BreakOut']=True
    message = message + "\tBuy At " + str(math.ceil(buyAt * 100) / 100) + ". Target = " + str(math.ceil(buyTarget * 100) / 100) + ". Stoploss = " + str(math.ceil(buyStopLoss * 100) / 100) + "\n"
    message = message + "\t\tSell At " + str(math.ceil(sellAt * 100) / 100) + ". Target = " + str(math.ceil(sellTarget * 100) / 100) + ". Stoploss = " + str(math.ceil(sellStopLoss * 100) / 100) + ""
    #print(message)
    if(buyAt!=0):
        Signal['BreakOut']=False
        #BreakOutSignals.append(Signal)
        #print(message)
    return Signal

fibMS={}
AllList=[]
def test(CrudeData,DateIndex,decimal):
    #CrudeData=LeadHistoryV1
    #DateIndex=DataIndex
    #decimal=3
    global AllList
    LowerList=[]
    HigherList=[]
    LowerMList=[]
    HigherMList=[]
    LowerMinList=[]
    HigherMinList=[]
    i=1
    #print(CrudeData.iloc[DateIndex]['Date'])
    AllList=list(CrudeData.iloc[DateIndex])[6:]
    while(i<=4):
        LowerList.append(CrudeData.iloc[DateIndex]['L'+str(i)])
        HigherList.append(CrudeData.iloc[DateIndex]['H'+str(i)])
        LowerMList.append(CrudeData.iloc[DateIndex]['L'+str(i-1)+"M1"])
        HigherMList.append(CrudeData.iloc[DateIndex]['H'+str(i-1)+"M1"])
        LowerMinList.append(CrudeData.iloc[DateIndex]['L'+str(i-1)+"M0"])
        LowerMinList.append(CrudeData.iloc[DateIndex]['L'+str(i-1)+"M2"])
        HigherMinList.append(CrudeData.iloc[DateIndex]['H'+str(i-1)+"M0"])
        HigherMinList.append(CrudeData.iloc[DateIndex]['H'+str(i-1)+"M2"])        
        i=i+1
    PH=CrudeData.iloc[DateIndex-1]['High']
    PL=CrudeData.iloc[DateIndex-1]['Low']
    fPH=CrudeData.iloc[DateIndex]['High']
    fPL=CrudeData.iloc[DateIndex]['Low']
#    
#    l=0
#    while(l<len(LowerList)):
#        h=0
#        while(h<len(HigherList)):
#            S=BreakOut(PH,PL,HigherList[h],LowerList[l])
#            if(S['BreakOut']==True):
#                print("Expected BreakOut at Low:"+str(LowerList[l])+"\tHigher : "+str(HigherList[h]))
#            
#            h=h+1
#        l=l+1
#    
#    l=0
#    while(l<len(LowerList)):
#        h=0
#        while(h<len(HigherMList)):
#            S=BreakOut(PH,PL,HigherMList[h],LowerList[l])
#            #if(S['BreakOut']==True):
#            print(str(S['BreakOut'])+ " - "  + " = " +str(LowerList[l])+"\tHigher : "+str(HigherMList[h]))
#            
#            h=h+1
#        l=l+1
#    
#    l=0
#    while(l<len(LowerList)):
#        h=0
#        while(h<len(HigherMinList)):
#            S=BreakOut(PH,PL,HigherMinList[h],LowerList[l])
#            #if(S['BreakOut']==True):
#            print(str(S['BreakOut'])+ " - "  + " = " +str(LowerList[l])+"\tHigher : "+str(HigherMinList[h]))
#            
#            h=h+1
#        l=l+1
#        
#    l=0
#    while(l<len(LowerList)):
#        h=0
#        while(h<len(HigherMinList)):
#            S=BreakOut(PH,PL,HigherMinList[h],LowerList[l])
#            #if(S['BreakOut']==True):
#            if(S['BreakOut']):
#                print(str(S['BreakOut'])+ " - "  + " = " +str(LowerList[l])+"\tHigher : "+str(HigherMinList[h]))
#            #print(S)
#            h=h+1
#        
#        l=l+1
    
    Fibs=fibupper(fPH-fPL,fPL)
    #getKey(Fibs,31585)
    #Fibs[-618]
    fibseries = [1, 236, 382, 500, 618, 786, 1000, 1236,1382, 1500, 1618, 2000,2236,-236, -382, -500, -618, -786, -1000, -1236,-1382,-1500, -1618, -2000,-2236]
    for fib in fibseries:
        if(fib==1):
            fibMS[0]=round(Fibs[fib],decimal)
        else:
            fibMS[fib]=round(Fibs[fib],decimal)
    Range=fPH-fPL
    tolerance=round(Range*.04,decimal)
#    Percent=0.003        
    #tolerance=round(CrudeData.iloc[DateIndex]['Open']*Percent/10,2)
    for fibM in fibMS:
        #print(str(fibMS[fibM]))
        #fibM=-618
        #List=math.floor(round(31582.5,decimal))
        for List in AllList:
            if(fibMS[fibM]-tolerance <= round(List,decimal) <= fibMS[fibM]+tolerance):
                t=1

GoldExpiry="05JUN2019"
SilverExpiry="03MAY2019"
ZincExpiry="30APR2019"
LeadExpiry="30APR2019"
PivotType="D"
OHLC=4
DataIndex=11
#Symbol="Silver" 
Symbol="GOLD"
GoldHistoryV1=candlestick.GetEODDataFromMCX(Symbol,PivotType,OHLC,GoldExpiry)
GoldHistoryV2=candlestick.GetEODDataFromMCX(Symbol,PivotType,3,GoldExpiry)
GoldHistoryV3=candlestick.GetEODDataFromMCX(Symbol,"C",3,GoldExpiry)
GoldHistoryV4=candlestick.GetEODDataFromMCX(Symbol,"C",4,GoldExpiry)
GoldCandle15Min=candlestick.getLiveDataFromZerodha(Symbol,"15minute")
GoldCandle1Min=candlestick.getLiveDataFromZerodha(Symbol,"minute")
GoldCandle3Min=candlestick.getLiveDataFromZerodha(Symbol,"3minute")
GoldCandle5Min=candlestick.getLiveDataFromZerodha(Symbol,"5minute")
GoldCandle30Min=candlestick.getLiveDataFromZerodha(Symbol,"30minute")
ChartWithBreakOut(GoldHistoryV1,DataIndex,GoldCandle15Min,GoldCandle30Min,Symbol+"V1")
ChartWithBreakOut(GoldHistoryV2,DataIndex,GoldCandle15Min,GoldCandle30Min,Symbol+"V2")
ChartWithBreakOut(GoldHistoryV3,DataIndex,GoldCandle15Min,GoldCandle30Min,Symbol+"V3")
ChartWithBreakOut(GoldHistoryV4,DataIndex,GoldCandle15Min,GoldCandle30Min,Symbol+"V4")



Symbol="LEAD"
LeadHistoryV1=candlestick.GetEODDataFromMCX(Symbol,PivotType,OHLC,LeadExpiry)
LeadHistoryV2=candlestick.GetEODDataFromMCX(Symbol,PivotType,3,LeadExpiry)
LeadHistoryV3=candlestick.GetEODDataFromMCX(Symbol,"C",3,LeadExpiry)
LeadHistoryV4=candlestick.GetEODDataFromMCX(Symbol,"C",4,LeadExpiry)




LeadCandle1Min=candlestick.getLiveDataFromZerodha(Symbol,"minute")
LeadCandle3Min=candlestick.getLiveDataFromZerodha(Symbol,"3minute")
LeadCandle5Min=candlestick.getLiveDataFromZerodha(Symbol,"5minute")
LeadCandle15Min=candlestick.getLiveDataFromZerodha(Symbol,"15minute")
LeadCandle30Min=candlestick.getLiveDataFromZerodha(Symbol,"30minute")
ChartWithBreakOut(LeadHistoryV2,DataIndex,LeadCandle5Min,LeadCandle30Min,Symbol+"V2")
ChartWithBreakOut(LeadHistoryV1,DataIndex,LeadCandle5Min,LeadCandle30Min,Symbol+"V1")
#DataIndex=0
#candlestick.DisplayCandles(GoldHistoryV1,DataIndex,GoldCandle30Min,GoldCandle15Min,Symbol+"V1",False)
#candlestick.DisplayCandles(GoldHistoryV2,DataIndex,GoldCandle30Min,GoldCandle15Min,Symbol+"V2",False)
#candlestick.DisplayCandles(GoldHistoryV3,DataIndex,GoldCandle30Min,GoldCandle15Min,Symbol+"V3",False)
#candlestick.DisplayCandles(GoldHistoryV4,DataIndex,GoldCandle30Min,GoldCandle15Min,Symbol+"V4",False)
#
Symbol="SILVER"
PivotType="D"
OHLC=4

SilverHistory=candlestick.GetEODDataFromMCX(Symbol,PivotType,OHLC,SilverExpiry)
SilverHistoryV2=candlestick.GetEODDataFromMCX(Symbol,PivotType,3,SilverExpiry)
SilverHistoryV3=candlestick.GetEODDataFromMCX(Symbol,"C",3,SilverExpiry)
SilverHistoryV4=candlestick.GetEODDataFromMCX(Symbol,"C",4,SilverExpiry)
SilverCandle15Min=candlestick.getLiveDataFromZerodha(Symbol,"15minute")
SilverCandle1Min=candlestick.getLiveDataFromZerodha(Symbol,"minute")
SilverCandle3Min=candlestick.getLiveDataFromZerodha(Symbol,"3minute")
SilverCandle5Min=candlestick.getLiveDataFromZerodha(Symbol,"5minute")
SilverCandle30Min=candlestick.getLiveDataFromZerodha(Symbol,"30minute")
ChartWithBreakOut(SilverHistory,DataIndex,SilverCandle15Min,SilverCandle30Min,Symbol+"V1")
ChartWithBreakOut(SilverHistoryV2,DataIndex,SilverCandle15Min,SilverCandle30Min,Symbol+"V2")
ChartWithBreakOut(SilverHistoryV3,DataIndex,SilverCandle15Min,SilverCandle30Min,Symbol+"V3")
ChartWithBreakOut(SilverHistoryV4,DataIndex,SilverCandle15Min,SilverCandle30Min,Symbol+"V4")
##DataIndex=2
#candlestick.DisplayCandles(SilverHistory,DataIndex,SilverCandle30Min,SilverCandle15Min,Symbol+"V1",False)
#candlestick.DisplayCandles(SilverHistoryV2,DataIndex,SilverCandle30Min,SilverCandle15Min,Symbol+"V2",False)
#candlestick.DisplayCandles(SilverHistoryV3,DataIndex,SilverCandle30Min,SilverCandle15Min,Symbol+"V3",False)
#candlestick.DisplayCandles(SilverHistoryV4,DataIndex,SilverCandle30Min,SilverCandle15Min,Symbol+"V4",False)
#
#
#################
GoldCandle1Min=candlestick.doji(GoldCandle1Min)
GoldCandle3Min=candlestick.doji(GoldCandle3Min)
GoldCandle5Min=candlestick.doji(GoldCandle5Min)
GoldCandle15Min=candlestick.doji(GoldCandle15Min)
GoldCandle30Min=candlestick.doji(GoldCandle30Min)
GoldCandle1Min=candlestick.doji_star(GoldCandle1Min)
GoldCandle1Min=candlestick.gravestone_doji(GoldCandle1Min)
GoldCandle1Min=candlestick.dragonfly_doji(GoldCandle1Min)

#GoldCandle3Min=candlestick.doji_star(GoldCandle3Min)
#GoldCandle3Min=candlestick.gravestone_doji(GoldCandle3Min)
#GoldCandle3Min=candlestick.dragonfly_doji(GoldCandle3Min)


#GoldCandle5Min=candlestick.doji_star(GoldCandle5Min)
#GoldCandle5Min=candlestick.gravestone_doji(GoldCandle5Min)
#GoldCandle5Min=candlestick.dragonfly_doji(GoldCandle5Min)

Candle1Min=SilverCandle1Min
Candle1Min.columns
#Temp=Candle1Min[(Candle1Min['DojiStar']==True)] & (Candle1Min['open']==Candle1Min['close'])]
#Temp=Candle1Min[(Candle1Min['DragonflyDoji']==True)]# & (Candle1Min['open']==Candle1Min['close'])]
#Temp=Candle1Min[(Candle1Min['GravestoneDoji']==True) & (Candle1Min['open']==Candle1Min['close'])]


SilverCandle1Min=candlestick.doji(SilverCandle1Min)
SilverCandle3Min=candlestick.doji(SilverCandle3Min)
SilverCandle5Min=candlestick.doji(SilverCandle5Min)
SilverCandle15Min=candlestick.doji(SilverCandle15Min)
SilverCandle30Min=candlestick.doji(SilverCandle30Min)
SilverCandle1Min=candlestick.doji_star(SilverCandle1Min)
SilverCandle1Min=candlestick.gravestone_doji(SilverCandle1Min)
SilverCandle1Min=candlestick.dragonfly_doji(SilverCandle1Min)

#GoldCandle1Min[GoldCandle1Min['Doji']==True]
#GoldCandle1Min[GoldCandle1Min['DojiStar']==True]
#GoldCandle1Min[GoldCandle1Min['GravestoneDoji']==True]
#GoldCandle1Min[GoldCandle1Min['DragonflyDoji']==True]

LeadCandle1Min=candlestick.doji(LeadCandle1Min)
LeadCandle3Min=candlestick.doji(LeadCandle3Min)
LeadCandle5Min=candlestick.doji(LeadCandle5Min)
LeadCandle15Min=candlestick.doji(LeadCandle15Min)
Candle1Min=LeadCandle1Min
Temp=Candle1Min[(Candle1Min['Doji']==True) & (Candle1Min['open']==Candle1Min['close'])]
Temp.iloc[0]['open']*0.003/10
getDoji(LeadCandle1Min,DataIndex,LeadHistoryV1,0.003)
getDoji(LeadCandle3Min,DataIndex,LeadHistoryV1,0.003*1.5)
getDoji(LeadCandle5Min,DataIndex,LeadHistoryV1,0.003*2.5)
getDoji(LeadCandle15Min,DataIndex,LeadHistoryV1,0.003)


getDoji(GoldCandle1Min,DataIndex,GoldHistoryV2,0.003)
getDoji(GoldCandle3Min,DataIndex,GoldHistoryV2,0.003*1.5)
getDoji(GoldCandle5Min,DataIndex,GoldHistoryV2,0.003*2.5)
getDoji(GoldCandle15Min,DataIndex,GoldHistoryV2,0.003*5)

getDoji(GoldCandle5Min,DataIndex,GoldHistoryV2,0.05)

getDoji(SilverCandle1Min,DataIndex,SilverHistoryV2,0.003)
getDoji(SilverCandle1Min,DataIndex,SilverHistoryV3,0.003)
getDoji(SilverCandle1Min,DataIndex,SilverHistoryV4,0.003)
getDoji(SilverCandle3Min,DataIndex,SilverHistoryV2,0.003*3)
getDoji(SilverCandle5Min,DataIndex,SilverHistoryV2,0.05)

#AllList=list(CrudeData.iloc[DateIndex])[6:]

DataIndex=0
#test(LeadHistoryV1,DataIndex,3)
#test(LeadHistoryV2,DataIndex,3)
#LeadHistoryV1.iloc[DataIndex]
#test(SilverHistory,8)
#test(GoldHistoryV1,8)
#test(SilverHistoryV2,8)
#test(GoldHistoryV2,8)
#
Messages=[]
DataIndex=5
TProfit=0
while(DataIndex<=10):
    SilverHistory.iloc[DataIndex]['Date']
    test(SilverHistory,DataIndex,0)
    SF1=AllList
    test(SilverHistoryV2,DataIndex,0)
    SF2=AllList
    SF3=fibMS
    
    test(GoldHistoryV1,DataIndex,0)
    GF1=AllList
    test(GoldHistoryV2,DataIndex,0)
    GF2=AllList
    GF3=fibMS
    
    GoldData=getSpecificData(GoldHistoryV1,GoldCandle5Min,DataIndex)
    SilverData=getSpecificData(SilverHistoryV2,SilverCandle5Min,DataIndex)
    
    #GoldData=getSpecificData1(GoldHistoryV1,GoldCandle5Min,DataIndex,4)
    #SilverData=getSpecificData1(SilverHistoryV2,SilverCandle5Min,DataIndex,4)

    GoldData['high'][:3]
    i=0
    LastFoundIndex=-1
    LastFoundSignal=""
    fPH=SilverHistoryV2.iloc[DataIndex]['High']
    fPL=SilverHistoryV2.iloc[DataIndex]['Low']
    SRange=fPH-fPL    
    Stolerance=round(SRange*.01,0)
    fPH=GoldHistoryV1.iloc[DataIndex]['High']
    fPL=GoldHistoryV1.iloc[DataIndex]['Low']
    GRange=fPH-fPL    
    Gtolerance=round(GRange*.01,0)
    GMargin=round(GRange*.25,0)
    GStoploss=round(GRange*.3,0)
    if(GMargin>100):
        GMargin=100
        GStoploss=110
        
    while(i<len(GoldData)):
        if(i>10):
            j=i-10
        else:
            j=i
        SLL=SilverData['low'][j:i+1].min()
        SHH=SilverData['high'][j:i+1].max()
        SL=SilverData.iloc[i]['low']
        SH=SilverData.iloc[i]['high']
        SO=SilverData.iloc[i]['open']
        SC=SilverData.iloc[i]['close']
        
        GLL=GoldData['low'][j:i+1].min()
        GHH=GoldData['high'][j:i+1].max()
        GL=GoldData.iloc[i]['low']
        GH=GoldData.iloc[i]['high']
        GO=GoldData.iloc[i]['open']
        GC=GoldData.iloc[i]['close']
        if(LastFoundIndex!=-1):        
            SPL=SilverData.iloc[LastFoundIndex]['low']
            SPH=SilverData.iloc[LastFoundIndex]['high']
            SPO=SilverData.iloc[LastFoundIndex]['open']
            SPC=SilverData.iloc[LastFoundIndex]['close']
            GPO=GoldData.iloc[LastFoundIndex]['open']
            GPC=GoldData.iloc[LastFoundIndex]['close']
            GPL=GoldData.iloc[LastFoundIndex]['low']
            GPH=GoldData.iloc[LastFoundIndex]['high']
            SPO1=SilverData.iloc[LastFoundIndex-1]['open']
            SPC1=SilverData.iloc[LastFoundIndex-1]['close']
            GPO1=GoldData.iloc[LastFoundIndex-1]['open']
            GPC1=GoldData.iloc[LastFoundIndex-1]['close']
            
            Transaction=""
            Reliability=False
            Data=GoldData    
            
            DateIndex=i
            #Margin=0.002
            #Stoploss=0.002            
            SearchData=GoldCandle5Min
            
            if((SL>SPL) and (GL>GPL)):
                
                Transaction="Buy"
                Reliability= (((GO>GC)==False) and ((SO>SC)==False) and ((GPO1>GPC1)==True) and ((SPO1>SPC1)==True))
                Reliability= (Reliability or 
                              (
                                      ((GO>GC)==False) and ((SO>SC)==False) and 
                                      ((GPO1>GPC1)==False) and ((SPO1>SPC1)==False) and 
                                      ((GPO>GPC)==False) and ((SPO>SPC)==False)
                                      )
                              )
                if ((Transaction!="") and Reliability):
                    if(GO==GC):
                        Transaction="Sell"
                        
                    Result=candlestick.Check(Data,Transaction,DateIndex,GMargin,GStoploss,SearchData)
                    print(str(SilverData.iloc[i]['Date']) + "\t"+Transaction+"1   \t" + str(GO>GC) + "\t"+str(SO>SC) + " - " + str(Result['Profit']))
                    Messages.append(str(SilverData.iloc[i]['Date']) +Transaction+"1   \t" + str(GPO1>GPC1) + " < " + str(GPO>GPC) +" < " +str(GO>GC) + "\t==\t"+str(SO>SC)+" > "+str(SPO>SPC)+" > "+str(SPO1>SPC1) + " -\t " + str(Result['Profit']) + " - " + str(GO==GC))
                    
                    TProfit=Result['Profit']+TProfit
            if((SH<SPH) and (GH<GPH)):
                #print(str(SilverData.iloc[i]['Date']) +" Sell \t" + str(GO>GC) + "\t"+str(SO>SC))
                Transaction="Sell"
                Reliability= (((GO>GC)==True) and ((SO>SC)==True) and ((GPO1>GPC1)==False) and ((SPO1>SPC1)==False))
                Reliability= (Reliability or 
                              (
                                      ((GO>GC)==True) and ((SO>SC)==True) and 
                                      ((GPO1>GPC1)==True) and ((SPO1>SPC1)==True) and 
                                      ((GPO>GPC)==True) and ((SPO>SPC)==True)
                                      )
                              )
                if ((Transaction!="") and Reliability):
                    Result=candlestick.Check(Data,Transaction,DateIndex,GMargin,GStoploss,SearchData)
                    print(str(SilverData.iloc[i]['Date']) +" Sell  \t" + str(GO>GC) + "\t"+str(SO>SC) + " - " + str(Result['Profit']))
                    Messages.append(str(SilverData.iloc[i]['Date']) +" Sell  \t" + str(GPO1>GPC1) + " < " + str(GPO>GPC) +" < " +str(GO>GC) + "\t==\t"+str(SO>SC)+" > "+str(SPO>SPC)+" > "+str(SPO1>SPC1) + " -\t " + str(Result['Profit']) + " - " + str(GO==GC))
                    TProfit=Result['Profit']+TProfit
            if(LastFoundSignal=="Buy" and ( (SPL-Stolerance <= SL <= SPL+Stolerance) or (GPL-Gtolerance <= GL <= GPL+Gtolerance))):
                print(str(SilverData.iloc[i]['Date']) +" BUYY \t" + str(GO>GC) + "\t"+str(SO>SC))            
            if(LastFoundSignal=="Sell" and ( (SH-Stolerance <= SPH <= SH+Stolerance) or (GH-Gtolerance <= GPH <= GH+Gtolerance))):
                print(str(SilverData.iloc[i]['Date']) +" SELLK \t" + str(GO>GC) + "\t"+str(SO>SC))
            
            
            
                
            LastFoundIndex=-1
            LastFoundSignal=""
        SResult1=False;SResult2=False;SResult3=False
        GResult1=False;GResult2=False;GResult3=False
        if(SL==SLL):
            SResult1=isInRange(SilverHistoryV2,DataIndex,SL,SF1,0,0.03)        
            SResult2=isInRange(SilverHistoryV2,DataIndex,SL,SF2,0,0.03)
            SResult3=isInRange(SilverHistoryV2,DataIndex,SL,SF3,0,0.03)
            LastFoundSignal="Buy"
        else:
            if(SH==SHH):
                SResult1=isInRange(SilverHistoryV2,DataIndex,SH,SF1,0,0.03)        
                SResult2=isInRange(SilverHistoryV2,DataIndex,SH,SF2,0,0.03)
                SResult3=isInRange(SilverHistoryV2,DataIndex,SH,SF3,0,0.03)       
                LastFoundSignal="Sell"
        
        if(GL==GLL):
            GResult1=isInRange(GoldHistoryV1,DataIndex,GL,GF1,0,0.03)        
            GResult2=isInRange(GoldHistoryV1,DataIndex,GL,GF2,0,0.03)        
            GResult3=isInRange(GoldHistoryV1,DataIndex,GL,GF3,0,0.03)        
            LastFoundSignal="Buy"
        else:
            if(GH==GHH):
                GResult1=isInRange(GoldHistoryV1,DataIndex,GH,GF1,0,0.03)        
                GResult2=isInRange(GoldHistoryV1,DataIndex,GH,GF2,0,0.03)        
                GResult3=isInRange(GoldHistoryV1,DataIndex,GH,GF3,0,0.03)
                LastFoundSignal="Sell"
        
        if(((SResult1==True)| (SResult2==True)| (SResult3==True)) and ((GResult1==True)| (GResult2==True)| (GResult3==True))):
            #print(SilverData.iloc[i]['Date'])
            LastFoundIndex=i
        
        i=i+1
    DataIndex=DataIndex+1

for Message in Messages:
    print(Message)
print(TProfit)
#
#test(GoldHistoryV1,DataIndex,0)
#test(GoldHistoryV2,DataIndex,0)
#GoldHistoryV1.iloc[DataIndex]
##AllList
#test(SilverHistoryV3,DataIndex,0)
#test(GoldHistoryV3,DataIndex,0)


            #if(fibMS[fibM]==List):
            #if(Range-tolerance <= O <= Range+tolerance):
#uncomment                print("\t"+str(fibM)+ "\t - \t" +str(round(fibMS[fibM],2)) + " \t - \t" + str(round(List,decimal))+" \t "+str(round(fibMS[fibM]-List,decimal)))
    #fibMS[]            
#    Range=fPH-fPL
#    tolerance=round(Range*.01,2)
#    Percent=0.003        
#    #tolerance=round(CrudeData.iloc[DateIndex]['Open']*Percent/10,2)
#    for fibM in fibMS:
#        #print(str(fibMS[fibM]))
#        for List in AllList:
#            #if(fibMS[fibM]-tolerance <= List <= fibMS[fibM]+tolerance):
#            if(fibMS[fibM]==List):
#            #if(Range-tolerance <= O <= Range+tolerance):
#                print(str(fibM)+ " - " +str(fibMS[fibM]) + " - " + str(List))    
#    
        #print(str(fib) + " - " + str(Fibs[fib]))
    #getKey(Fibs,fib)
      #BreakOut(PH,PL,LowerList[l],HigherMinList[h])  
##DataIndex=2
#candlestick.DisplayCandles(SilverHistory,DataIndex,SilverCandle30Min,SilverCandle15Min,Symbol+"V1",False)
#candlestick.DisplayCandles(SilverHistoryV2,DataIndex,SilverCandle30Min,SilverCandle15Min,Symbol+"V2",False)
#candlestick.DisplayCandles(SilverHistoryV3,DataIndex,SilverCandle30Min,SilverCandle15Min,Symbol+"V3",False)
#candlestick.DisplayCandles(SilverHistoryV4,DataIndex,SilverCandle30Min,SilverCandle15Min,Symbol+"V4",False)
#
#
#################
#GoldCandle1Min=candlestick.doji(GoldCandle1Min)
#GoldCandle1Min=candlestick.doji_star(GoldCandle1Min)
#GoldCandle1Min=candlestick.gravestone_doji(GoldCandle1Min)
#GoldCandle1Min=candlestick.dragonfly_doji(GoldCandle1Min)
#
#SilverCandle1Min=candlestick.doji(SilverCandle1Min)
#SilverCandle3Min=candlestick.doji(SilverCandle3Min)
#SilverCandle5Min=candlestick.doji(SilverCandle5Min)
#SilverCandle1Min=candlestick.doji_star(SilverCandle1Min)
#SilverCandle1Min=candlestick.gravestone_doji(SilverCandle1Min)
#SilverCandle1Min=candlestick.dragonfly_doji(SilverCandle1Min)
#
##GoldCandle1Min[GoldCandle1Min['Doji']==True]
##GoldCandle1Min[GoldCandle1Min['DojiStar']==True]
##GoldCandle1Min[GoldCandle1Min['GravestoneDoji']==True]
##GoldCandle1Min[GoldCandle1Min['DragonflyDoji']==True]
#getDoji(GoldCandle1Min,DataIndex,GoldHistoryV2,0.003)
#getDoji(SilverCandle1Min,DataIndex,SilverHistoryV2,0.003)
#getDoji(SilverCandle1Min,DataIndex,SilverHistoryV3,0.003)
#getDoji(SilverCandle1Min,DataIndex,SilverHistoryV4,0.003)
#getDoji(SilverCandle3Min,DataIndex,SilverHistoryV2,0.003*3)
#getDoji(SilverCandle5Min,DataIndex,SilverHistoryV2,0.003*5)
#

#Candle1Min=GoldCandle15Min
#History=GoldHistoryV1
#Temp=GoldCandle15Min


#    drawChart("LeadTest-"+quotes.iloc[Index]['Date'].strftime("%d-%b")+".html")
#ll1=ll1+1 
#candlestick.BreakOutLines    
#GoldCandle1Min.columns

#candlestick.BreakOut(PHigh,PLow,31865,31719,quotes.iloc[ii-1]['Date'])
###########

#TSilver=SilverCandle15Min[['Date','open']]
#TGold=GoldCandle15Min[['Date','open']]
#TGold.columns=['DATE','GOLDOPEN']
#TSilver.columns=['DATE','SilverOPEN']
#TResult=TGold.merge(TSilver)
#TResult['Diff']=round(TResult['SilverOPEN']/TResult['GOLDOPEN'],2)
#TResult.groupby('Diff').count()
#TResult[['Diff']==1.31]
#    
#OverRide=False
#DateIndex=5 #Current Date Set the value to 1 ..3 for monday
#DisplayCandles()
#Monday=True
#if(Monday):
#    OverRide=True
#    DateIndex=DateIndex+1
####Change it to True for Monday
##### Change it only for monday For WeekDay Start DataIndex should be 2
##OverRide=True
###########################################################################
# #For Monday it is 3
#
##############################################################################
#StartTime=datetime.now()
##DisplayCandles()
##pd.DataFrame(arBuyCandles)[['Date','Transaction','Price']]
##pd.DataFrame(arSellCandles)[['Date','Transaction','Price']]
#loopi=0
#while(loopi<1):
##    StartTime=datetime.now()
#    DisplayCandles()
#    loopi=loopi+1
#    print("Waiting......")    
#    time.sleep(120)



#
#c=Data2[(Data2["Pivot"]<Data2["L1"]) & (Data2['Pivot']<Data2['L2'])]
#d=Data2[(Data2["Pivot"]<Data2["L1"]) & (Data2['Pivot']<Data2['L2']) & (Data2['H1']<Data2['L2'])]
#e=Data2[(Data2["Pivot"]<Data2["L1"]) & (Data2['Pivot']<Data2['L2']) & (Data2['H1']>Data2['L2'])]
#i=1
#print(str(d.iloc[i]['Date']) + " - " + str((d.iloc[i]['L2']+d.iloc[i]['H1'])/2))
#
#j=5
#print(str(e.iloc[j]['Date']) + " - " + str((e.iloc[j]['L2']+e.iloc[j]['Pivot'])/2))
#e.iloc[j]
#g=Data2[(Data2["H1"]<Data2["H2"])]
#ig=4
#print(str(g.iloc[ig]['Date']) + " - " + str((g.iloc[ig]['L2']+g.iloc[ig]['H1'])/2))
#
#
#f=Data2[(Data2["Pivot"]>Data2["L1"]) & (Data2['Pivot']>Data2['L2'])  & ((Data2['H3']+Data2['H2'])/2<Data2["Pivot"])]
#f.iloc[0]
#(f.iloc[0]['H3']+f.iloc[0]['H1'])/2
#########################################
#


#def swing_detection(ii,high,low):
#    #ii=8
#    index=ii#-7
#    swing_high = False
#    swing_low = False
#    start = (index*2) - 1 # -1 so we have an even number of
#    swing_point_high = high[index]
#    swing_point_low = low[index]
#    
#    i=0
#    while(i<start): 
#    #Swing Highs
#    #for i in start
#        swing_high = True
#        if (i < index): 
#            if (high[i] > swing_point_high) :
#                swing_high = False
#                break
#        # Have to do checks before pivot and after seperately because we can get
#        # two highs of the same value in a row. Notice the > and >= difference
#        if (i > index):
#            if (high[i] >= swing_point_high): 
#                swing_high = False
#                break
#        i=i+1
#        
#   #Swing lows
#    i=0
#    while(i<start):
#        swing_low = True
#        if (i < index):
#            if (low[i] < swing_point_low ):
#                swing_low = False
#                break  
#        # Have to do checks before pivot and after seperately because we can get
#        # two lows of the same value in a row. Notice the > and >= difference
#        if (i > index):
#            if (low[i] <= swing_point_low):
#                swing_low = False
#                break
#        i=i+1
#        
#    return swing_high, swing_low
#
#j=1
#h=g['high']
#l=g['low']
#while(j<len(g)):
#    a=swing_detection(j,h,l)
#    if(a[0] or a[1]):
#        print(str(g.iloc[j]['Date']) + " - "+ str(a[0]) + " - " + str(a[1]) )
