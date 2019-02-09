# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 08:01:35 2019

@author: lalitha
"""

from candlestick import candlestick
import datetime
import pandas as pd
import json
#from datetime import timedelta  
from datetime import datetime, timedelta
import requests
from ehp import *
from dateutil.parser import parse
import numpy as np
import plotly.graph_objs as go
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import plotly.io as pio
import os
from plotly.tools import FigureFactory as FF

from datetime import datetime

def MaRound(n):
    return round(n*100/100,2)

def getPivots(High,Low,Close):
    Points={}
    #pivot,re1,re2,re3,re4,su1,su2,su3,su4,High,Close,Low
    #High=54.93
    #Low=53.09
    #Close=54.23
    pivot= MaRound((High+Low+Close)/3)
    re1 = MaRound(Close+(High-Low)*(1.1/12))
    su1 = MaRound(Close-(High-Low)*(1.1/12))
    re2 = MaRound(Close+(High-Low)*(1.1/6))
    su2 = MaRound(Close-(High-Low)*(1.1/6))
    re3 = MaRound(Close+(High-Low)*(1.1/4))
    su3 = MaRound(Close-(High-Low)*(1.1/4))
    re4 = MaRound(Close+(High-Low)*(1.1/2))
    su4 = MaRound(Close-(High-Low)*(1.1/2))
    re5 = MaRound((High/Low)*Close)
    su5 = MaRound(Close-(re5-Close))
    re41 = MaRound((re5+re4)/2)
    su41 = MaRound((su5+su4)/2)    
    Points["Pivot"]=pivot
    Points["H6"]=re5
    Points["H5"]=re41
    Points["H4"]=re4
    Points["H3"]=re3
    Points["H2"]=re2
    Points["H1"]=re1
    Points["L6"]=su5
    Points["L5"]=su41
    Points["L4"]=su4
    Points["L3"]=su3
    Points["L2"]=su2
    Points["L1"]=su1
    return Points

def ProcessCandles(Df):
    Df = candlestick.bearish_engulfing(Df)
    Df = candlestick.bullish_engulfing(Df)
    Df = candlestick.three_inside_up(Df)
    Df = candlestick.three_inside_down(Df)
    Df = candlestick.three_outside_up(Df)
    Df = candlestick.three_outside_down(Df)
    Df['MovingAverageDown']=Df['low'].rolling(window=10).mean()
    Df['MovingAverageUp']=Df['high'].rolling(window=10).mean()
    Df['MovingAverage']=Df['close'].rolling(window=10).mean()
    Df['EMA10C']=pd.DataFrame.ewm(Df['close'],min_periods=10,adjust=False,span=10).mean()
    Df['EMA10O']=pd.DataFrame.ewm(Df['open'],min_periods=10,adjust=False,span=10).mean()
    Df['EMA10H']=pd.DataFrame.ewm(Df['high'],min_periods=10,adjust=False,span=10).mean()
    Df['EMA10L']=pd.DataFrame.ewm(Df['low'],min_periods=10,adjust=False,span=10).mean()
    return Df

def Check(tdaily,Signal,DateIndex,Margin,Stoploss,SearchData):
    SingleStatus={}
    global Profit
    #tdaily=CrudeDf30Min
    #SearchData=CrudeDf15Min
    #Margin=0.005
    #DateIndex=482
    #Signal="Buy"
    DefaultDate=datetime.now()
    tdaily['BuyTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['BuyTargetTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['BuyStopLossTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['SellTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['SellTargetTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['SellStopLossTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['LastPrice']=pd.Series(None,index=tdaily.index)
    tdaily['BuyHit']=pd.Series(0,index=tdaily.index)
    tdaily['SellHit']=pd.Series(0,index=tdaily.index)
#if True:
    #daily.iloc[DateIndex]['Date']
    tdaily.iloc[DateIndex]
    aDate=list(tdaily[DateIndex+1:][:1]['Date'])[0]
    #print(aDate)
    LastDate=parse(tdaily.iloc[DateIndex]['Date'].strftime('%Y-%m-%d 23:59:00')) 
    #print(LastDate)
    #SpecificDate=data[ (data['Date/Time']>daily.iloc[DateIndex-1]['Date']) 
    #& (data['Date/Time']<daily.iloc[DateIndex-2]['Date'])]
    SpecificDate=SearchData[(SearchData['Date']>=aDate) & (SearchData['Date']<LastDate)]
    #(data['Date']>daily.iloc[100]['Date'] and
    #data.set_index('Date/Time')
    #SpecificDate['Date/Time']
    #print(len(SpecificDate))
    isBuyProcess=True
    isSellProcess=True
    
    Tollerance=.01
    #if(Signal=="Buy"):
    #BuyP=tdaily.iloc[DateIndex]['close']+Tollerance
    BuyP=tdaily.iloc[DateIndex+1]['open']
    BuyT=BuyP*(1+Margin)
    #BuySL=tdaily.iloc[DateIndex-2]['low']
    BuySL=BuyP*(1-Stoploss)
    
    BuyPT=SpecificDate[(SpecificDate['high']>=BuyP-Tollerance) & (SpecificDate['low']<=BuyP+Tollerance)]
    BuyTT=SpecificDate[(SpecificDate['high']>=BuyT-Tollerance) & (SpecificDate['low']<=BuyT+Tollerance)]
    BuySLT=SpecificDate[(SpecificDate['high']>=BuySL-Tollerance) & (SpecificDate['low']<=BuySL+Tollerance)]
    
#else:    
    #SellP=tdaily.iloc[DateIndex]['close']-Tollerance
    SellP=tdaily.iloc[DateIndex+1]['open']
    SellT=SellP*(1-Margin)
    #SellSL=tdaily.iloc[DateIndex-2]['high']
    SellSL=SellP*(1+Stoploss)
    
    SellPT=SpecificDate[(SpecificDate['high']>=SellP-Tollerance) & (SpecificDate['low']<=SellP+Tollerance)]
    SellTT=SpecificDate[(SpecificDate['high']>=SellT-Tollerance) & (SpecificDate['low']<=SellT+Tollerance)]
    SellSLT=SpecificDate[(SpecificDate['high']>=SellSL-Tollerance) & (SpecificDate['low']<=SellSL+Tollerance)]
    #data=data1
    #data.loc[SpecificDate]['Date/Time']
    
    SingleStatus['Date']=tdaily.iloc[DateIndex]['Date'].strftime("%m/%d/%Y %I:%M %p")
    SingleStatus['Percentage']=Margin
    if(Signal=="Buy"):
        SingleStatus['Signal']="Buy"        
        SingleStatus['Price']=BuyP       
        SingleStatus['Target']=BuyT      
        SingleStatus['StopLoss']=BuySL        
        isSellProcess=False
        print(str(BuyP) +  "  ===============  " + str(BuyT) + " ======== "+ str(BuySL))
    else:
        isBuyProcess=False
        SingleStatus['Signal']="Sell"
        SingleStatus['Price']=SellP       
        SingleStatus['Target']=SellT      
        SingleStatus['StopLoss']=SellSL 
        print(str(SellP) +  "  ===============  " + str(SellT) + " ======== "+ str(SellSL))
    
    
    
    BuyHit=False
    SellHit=False
    LastPriceBuyHit=False
    LastPriceSellHit=False
    LastPriceHit=False
    LastPrice=0
    #if len(BuyPT)>0:
    #    print("Buy Price At : " + str(BuyPT.iloc[0]['Date/Time']))
    #    if len(BuyTT)>0:
    #        print("Buy Target At : "+ str(BuyTT.iloc[0]['Date/Time']))
    #        print("Total Profit :" + str(BuyT-BuyP))
    #    if len(BuySLT)>0:
    #        print("Buy Stop loss At : " + str(BuySLT.iloc[0]['Date']))
    #        print("Total Loss:" + str(BuySL-BuyP))
    
    

    #if( len(BuyPT)>0 and len(SellPT)>0):
    #    isBuyProcess=(BuyPT.iloc[0]['Date']<SellPT.iloc[0]['Date'])
    #    isSellProcess=(BuyPT.iloc[0]['Date']>SellPT.iloc[0]['Date'])
   
    if(len(BuyPT)>0):
        tdaily['BuyTime'][DateIndex]=BuyPT.iloc[0]['Date']
        if(Signal=="Buy"):
            SingleStatus['Time']=BuyPT.iloc[0]['Date'].strftime("%m/%d/%Y %I:%M %p")
    if(len(BuyTT)>0):
        tdaily['BuyTargetTime'][DateIndex]=BuyTT.iloc[0]['Date']
        if(Signal=="Buy"):
            SingleStatus['TargetTime']=BuyTT.iloc[0]['Date'].strftime("%m/%d/%Y %I:%M %p")
    if(len(BuySLT)>0):
        tdaily['BuyStopLossTime'][DateIndex]=BuySLT.iloc[0]['Date']    
        if(Signal=="Buy"):
            SingleStatus['StopLossTime']=BuySLT.iloc[0]['Date'].strftime("%m/%d/%Y %I:%M %p")
    if(len(SellPT)>0):
        tdaily['SellTime'][DateIndex]=SellPT.iloc[0]['Date']
        if(Signal=="Sell"):
            SingleStatus['Time']=SellPT.iloc[0]['Date'].strftime("%m/%d/%Y %I:%M %p")
    if(len(SellTT)>0):
        tdaily['SellTargetTime'][DateIndex]=SellTT.iloc[0]['Date']
        if(Signal=="Sell"):
            SingleStatus['TargetTime']=SellTT.iloc[0]['Date'].strftime("%m/%d/%Y %I:%M %p")
    if(len(SellSLT)>0):
        tdaily['SellStopLossTime'][DateIndex]=SellSLT.iloc[0]['Date']    
        if(Signal=="Sell"):
            SingleStatus['StopLossTime']=SellSLT.iloc[0]['Date'].strftime("%m/%d/%Y %I:%M %p")
            
        
    if (len(BuyPT)>0 and isBuyProcess):
        print("Buy Price at : " + str(BuyPT.iloc[0]['Date']))
        tdaily['BuyTime'][DateIndex]=BuyPT.iloc[0]['Date']
        if len(BuyTT)>0:
            print("Buy Target at : " + str(BuyTT.iloc[0]['Date']))
            tdaily['BuyTargetTime'][DateIndex]=BuyTT.iloc[0]['Date']
            if len(BuySLT)<=0:
                if(BuyPT.iloc[0]['Date']<=BuyTT.iloc[0]['Date']):
                    print("*********Buy Total Profit :" + str(BuyT-BuyP))
                    BuyHit=True
                    tdaily['BuyHit'][DateIndex]=BuyT-BuyP
                else:
                    print("Total Value : "+ str(SpecificDate.iloc[len(SpecificDate)-1]['open']-BuyP))
                    tdaily['BuyHit'][DateIndex]=SpecificDate.iloc[len(SpecificDate)-1]['open']-BuyP
                    LastPriceHit=True
                    LastPrice=SpecificDate.iloc[len(SpecificDate)-1]['open']
            else:
                if(BuyPT.iloc[0]['Date']<=BuyTT.iloc[0]['Date']) and (BuyTT.iloc[0]['Date']<=BuySLT.iloc[0]['Date']):
                    print("*****Buy Total Profit :" + str(BuyT-BuyP))
                    BuyHit=True
                    tdaily['BuyHit'][DateIndex]=BuyT-BuyP
                else:
                    print("100 Buy Stop Losst at : "+str(BuySLT.iloc[0]['Date']))
                    tdaily['BuyStopLossTime'][DateIndex]=BuySLT.iloc[0]['Date']
                    if((BuyPT.iloc[0]['Date']<=BuyTT.iloc[0]['Date']) and (BuySLT.iloc[0]['Date']<=BuyTT.iloc[0]['Date'])):
                        print("100.1 Buy Total Loss:" + str(BuySL-BuyP))
                        BuyHit=False
                        tdaily['BuyHit'][DateIndex]=BuyT-BuyP
                    else:
                        print("Buy Total loss :" + str(BuyT-BuyP))
                        BuyHit=True
                        tdaily['BuyHit'][DateIndex]=BuySL-BuyP
            
        elif (len(BuySLT)>0):
            print("2Buy Stop Loss at : " + str(BuySLT.iloc[0]['Date']))
            tdaily['BuyStopLossTime'][DateIndex]=BuySLT.iloc[0]['Date']
            print("Buy Total loss :" + str(BuySL-BuyP))
            tdaily['BuyHit'][DateIndex]=BuySL-BuyP
            if len(BuyTT)>0:
                if(BuySLT.iloc[0]['Date']<=BuyTT.iloc[0]['Date']):
                    print("Buy Total loss :" + str(BuySL-BuyP))
                    tdaily['BuyHit'][DateIndex]=BuySL-BuyP
                    tdaily['BuyStopLossTime'][DateIndex]=BuySLT.iloc[0]['Date']
        else:
            print("Total Value : "+ str(SpecificDate.iloc[len(SpecificDate)-1]['open']-BuyP))
            tdaily['BuyHit'][DateIndex]=SpecificDate.iloc[len(SpecificDate)-1]['open']-BuyP
            LastPriceHit=True
            LastPrice=SpecificDate.iloc[len(SpecificDate)-1]['open']
            
    if len(SpecificDate) >0:       
        tdaily['LastPrice'][DateIndex]=SpecificDate.iloc[len(SpecificDate)-1]['open']
        #LastPriceHit=True
        #LastPrice=SpecificDate.iloc[len(SpecificDate)-1]['open']
    
    if (isSellProcess and len(SellPT)>0):
        print("Sell Price at : " + str(SellPT.iloc[0]['Date']))
        tdaily['SellTime'][DateIndex]=SellPT.iloc[0]['Date']
        if len(SellTT)>0:
            print("Sell Target at : " + str(SellTT.iloc[0]['Date']))
            
            tdaily['SellTargetTime'][DateIndex]=SellTT.iloc[0]['Date']
            if len(SellSLT)<=0:
                if(SellPT.iloc[0]['Date']<=SellTT.iloc[0]['Date']):
                    print("Sell Total Profit :" + str(SellP-SellT))
                    SellHit=True
                    tdaily['SellHit'][DateIndex]=SellP-SellT
                else:
                    print("Total Value : "+ str(SellP-SpecificDate.iloc[len(SpecificDate)-1]['open']))
                    tdaily['SellHit'][DateIndex]=SpecificDate.iloc[len(SpecificDate)-1]['open']-SellP
                    LastPriceHit=True
                    LastPrice=SpecificDate.iloc[len(SpecificDate)-1]['open']
            else:                
                if(SellPT.iloc[0]['Date']<=SellTT.iloc[0]['Date']) and (SellTT.iloc[0]['Date']<=SellSLT.iloc[0]['Date']):
                    print("Sell Total Profit :" + str(SellP-SellT))
                    SellHit=True
                    tdaily['SellHit'][DateIndex]=SellP-SellT
                else:    
                    print("Sell Stop Losst at 6: "+str(SellSLT.iloc[0]['Date']))
                    tdaily['SellStopLossTime'][DateIndex]=SellSLT.iloc[0]['Date']
                    if((SellPT.iloc[0]['Date']<=SellTT.iloc[0]['Date']) & (SellSLT.iloc[0]['Date']<=SellTT.iloc[0]['Date'])):
                        print("Sell Total loss 7:" + str(SellSL-SellP))
                        tdaily['SellHit'][DateIndex]=SellP-SellT
                    else:
                        
                        print("Sell Total Profit :-" + str(SellP-SellT))                        
                        SellHit=True
                        tdaily['SellHit'][DateIndex]=SellP-SellSL
            
        elif (len(SellSLT)>0):
            print("Sell Stop Loss at : " + str(SellSLT.iloc[0]['Date']))
            tdaily['SellStopLossTime'][DateIndex]=SellSLT.iloc[0]['Date']
            print("Sell Total loss 8:" + str(SellP-SellSL))
            tdaily['SellHit'][DateIndex]=SellP-SellSL
            if len(SellTT)>0:
                if(SellSLT.iloc[0]['Date']<=SellTT.iloc[0]['Date']):
                    print("Sell Total loss 9:" + str(SellP-SellSL))
                    tdaily['SellHit'][DateIndex]=SellP-SellSL
        else:
            print("Total Value : "+ str(SellP-SpecificDate.iloc[len(SpecificDate)-1]['open']))
            tdaily['SellHit'][DateIndex]=SpecificDate.iloc[len(SpecificDate)-1]['open']-SellP
            LastPriceHit=True
            LastPrice=SpecificDate.iloc[len(SpecificDate)-1]['open']
    
    if(Signal=="Buy"):
        if(BuyHit==True):
            SingleStatus['Hit']="Hit"
            SingleStatus['Profit']=BuyT-BuyP
            Profit=Profit+(BuyT-BuyP)
        else:
            if(LastPriceHit==True):
                SingleStatus['LastPrice']=LastPrice
                if(LastPrice>BuyP):
                    BuyHit=True
                    SingleStatus['Hit']="LastPrice-Profit"                    
                    SingleStatus['Profit']=LastPrice-BuyP
                    
                    Profit=Profit+(LastPrice-BuyP)
                else:
                    SingleStatus['Hit']="LastPrice-Loss"                    
                    SingleStatus['Profit']=LastPrice-BuyP
                    Profit=Profit+(LastPrice-BuyP)
            else:
                SingleStatus['Hit']="StopLoss"
                Profit=Profit+(BuySL-BuyP)
                SingleStatus['Profit']=(BuySL-BuyP)
        #return BuyHit
    else:
        if(SellHit==True):
            SingleStatus['Hit']="Hit"
            SingleStatus['Profit']=(SellP-SellT)
            Profit=Profit+(SellP-SellT)
        else:
            if(LastPriceHit==True):
                SingleStatus['LastPrice']=LastPrice
                if(LastPrice<BuyP):
                    SellHit=True
                    SingleStatus['Hit']="LastPrice-Profit"                    
                    SingleStatus['Profit']=(BuyP-LastPrice)
                    Profit=Profit+(BuyP-LastPrice)
                else:
                    SingleStatus['Hit']="LastPriceHit-Loss"
                    SingleStatus['Profit']=(BuyP-LastPrice)
                    Profit=Profit+(BuyP-LastPrice)
            else:
                SingleStatus['Hit']="StopLoss"
                Profit=Profit+(SellP-SellSL)
                SingleStatus['Profit']=(SellP-SellSL)
        #return SellHit
    return SingleStatus


def approximateEqual1(a, b):
    left=abs(round((a-b)*100)/100)
    right=round(a*100)/100000    
    return left <= right;



def N1(date,s,Operation):
    seconds_per_unit = {"S": 1, "M": 60, "H": 3600, "D": 86400, "W": 604800}
    if (Operation=="+"):
        return date+timedelta(seconds=int(s[:-1]) * seconds_per_unit[s[-1]])
    else:
        return date-timedelta(seconds=int(s[:-1]) * seconds_per_unit[s[-1]])
        
def ProcessCandles(Df):
    Df = candlestick.bearish_engulfing(Df)
    Df = candlestick.bullish_engulfing(Df)
    Df = candlestick.three_inside_up(Df)
    Df = candlestick.three_inside_down(Df)
    Df = candlestick.three_outside_up(Df)
    Df = candlestick.three_outside_down(Df)
    Df['MovingAverageDown']=Df['low'].rolling(window=10).mean()
    Df['MovingAverageUp']=Df['high'].rolling(window=10).mean()
    Df['MovingAverage']=Df['close'].rolling(window=10).mean()
    Df = candlestick.doji_star(Df)
    Df = candlestick.bearish_harami(Df)
    Df = candlestick.bullish_harami(Df)
    Df = candlestick.doji(Df)

    return Df


def datediff(d1, d2):
    #d1 = datetime.strptime(d1, "%Y-%m-%d")
    #d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).seconds)

def Filter30MinUPCandles(FilteredCandles,iPatternName,CandleType,Size,quotes):        
    ai=0
    while(ai<len(FilteredCandles)):
        RealPattern=False
        ImageRealPattern=False
        print("**************   "+CandleType+"    *****************")
    #if(5==5):
        LastCandles=quotes[quotes['Date']<FilteredCandles.iloc[ai]['Date']]
    #print(FilteredCandles.iloc[ai]['Date'])
        LastLow=LastCandles.iloc[-5:]['low'].min()
        LastHigh=LastCandles.iloc[-5:]['high'].max()
        #print(FilteredCandles.iloc[ai]['Date'])
        LastCandleMinute=0#LastCandles.iloc[len(LastCandles)-1]['Date'].minute
        if((LastCandleMinute==0) | (LastCandleMinute==30) | (True)):
            
            PatternName=""
            if(LastLow>=ResultMerge.iloc[0]['L6'] and LastLow<=ResultMerge.iloc[0]['L1']):            
                PatternName=""
                if(LastLow>=ResultMerge.iloc[0]['L6'] and LastLow<=ResultMerge.iloc[0]['L5']):
                    PatternName="L6"
                elif(LastLow>=ResultMerge.iloc[0]['L5'] and LastLow<=ResultMerge.iloc[0]['L4']):
                    PatternName="L5"
                elif(LastLow>=ResultMerge.iloc[0]['L4'] and LastLow<=ResultMerge.iloc[0]['L3']):
                    PatternName="L4"
                elif(LastLow>=ResultMerge.iloc[0]['L3'] and LastLow<=ResultMerge.iloc[0]['L2']):
                    PatternName="L3"
                elif(LastLow>=ResultMerge.iloc[0]['L2'] and LastLow<=ResultMerge.iloc[0]['L1']):
                    PatternName="L2"
                else:
                    PatternName="L1"
                #print(PatternName + "  -  Valid Pattern")
                RealPattern=True
            
            if(PatternName==""):
                if(LastLow<=ResultMerge.iloc[0]['APivot'] and LastLow>=ResultMerge.iloc[0]['Price']):
                    print("Valid Pattern on Close -1")
                if(LastLow<=ResultMerge.iloc[0]['Price'] and LastLow<=ResultMerge.iloc[0]['H1']):
                    print("Valid Pattern on Close -2")
                
            if(LastLow>=ResultMerge.iloc[0]['AL6'] and LastLow<=ResultMerge.iloc[0]['AL1']):
                imaginaryPatternName=""
                if(LastLow>=ResultMerge.iloc[0]['AL6'] and LastLow<=ResultMerge.iloc[0]['AL5']):
                    imaginaryPatternName="AL6"
                elif(LastLow>=ResultMerge.iloc[0]['AL5'] and LastLow<=ResultMerge.iloc[0]['AL4']):
                    imaginaryPatternName="AL5"
                elif(LastLow>=ResultMerge.iloc[0]['AL4'] and LastLow<=ResultMerge.iloc[0]['AL3']):
                    imaginaryPatternName="AL4"
                elif(LastLow>=ResultMerge.iloc[0]['AL3'] and LastLow<=ResultMerge.iloc[0]['AL2']):
                    imaginaryPatternName="AL3"
                elif(LastLow>=ResultMerge.iloc[0]['AL2'] and LastLow<=ResultMerge.iloc[0]['AL1']):
                    imaginaryPatternName="AL2"
                
                else:
                    imaginaryPatternName="AL1"        
                #print(PatternName + "  -  Imaginary Valid Pattern")
                ImageRealPattern=True
            
            #print( " - LastLow = "+str(LastLow))
            #print("Candle Close = "+str(FilteredCandles.iloc[ai]['close']))
            #print("Pivot = "+str(ResultMerge.iloc[0]['Pivot']))
            #print("APivot = "+str(ResultMerge.iloc[0]['APivot']))
            
            #print("L1 = "+str(ResultMerge.iloc[0]['L1']))
            #print("L6 = "+str(ResultMerge.iloc[0]['L6']))
            #print("AL1 = "+str(ResultMerge.iloc[0]['AL1']))
            #print("AL6 = "+str(ResultMerge.iloc[0]['AL6']))
            if((ImageRealPattern==True) & (RealPattern==True)):
                AnnotationsAr.append(CreateAnnotations(FilteredCandles.iloc[ai]['Date'],FilteredCandles.iloc[ai]['low'],iPatternName,'rgb(0, 255, 50)',3*Size))
                print(FilteredCandles.iloc[ai]['Date'])
                print(PatternName + "  -  Valid Pattern")
                print(imaginaryPatternName + "  -  Imaginary Valid Pattern")
                print("Last Minute= "+str(LastCandleMinute))        
                print("Candle Close = "+str(FilteredCandles.iloc[ai]['close']))
        ai=ai+1
    print("**************   "+CandleType+"    *****************")
    return True

def Filter30MinDownCandles(FilteredCandles,iPatternName,CandleType,Size,quotes): 
    ai=0
    print("**************   "+CandleType+"    *****************")
    while(ai<len(FilteredCandles)):
        RealPattern=False
        ImageRealPattern=False
    #if(5==5):
        LastCandles=quotes[quotes['Date']<FilteredCandles.iloc[ai]['Date']]
    #print(FilteredCandles.iloc[ai]['Date'])
        LastHigh=LastCandles.iloc[-5:]['high'].max()
        LastCandleMinute=0#LastCandles.iloc[len(LastCandles)-1]['Date'].minute
        if((LastCandleMinute==0) | (LastCandleMinute==30) | (True)):
        
            if(LastHigh>=ResultMerge.iloc[0]['H1'] and LastHigh<=ResultMerge.iloc[0]['H6']):
                
                #print("test")
                PatternName=""
                if(LastHigh>=ResultMerge.iloc[0]['H1'] and LastHigh<=ResultMerge.iloc[0]['H2']):
                    PatternName="H1"
                elif(LastHigh>=ResultMerge.iloc[0]['H2'] and LastHigh<=ResultMerge.iloc[0]['H3']):
                    PatternName="H2"
                elif(LastHigh>=ResultMerge.iloc[0]['H3'] and LastHigh<=ResultMerge.iloc[0]['H4']):
                    PatternName="H3"        
                elif(LastHigh>=ResultMerge.iloc[0]['H4'] and LastHigh<=ResultMerge.iloc[0]['H5']):
                    PatternName="H4"
                elif(LastHigh>=ResultMerge.iloc[0]['H5'] and LastHigh<=ResultMerge.iloc[0]['H6']):
                    PatternName="H5"
                else:
                    PatternName="H6"
                #print(FilteredCandles.iloc[ai]['Date'])
                #print(PatternName + "  -  Valid Pattern")
                RealPattern=True
            if(LastHigh>=ResultMerge.iloc[0]['AH1'] and LastHigh<=ResultMerge.iloc[0]['AH6']):
                imaginaryPatternName=""
                if(LastHigh>=ResultMerge.iloc[0]['AH1'] and LastHigh<=ResultMerge.iloc[0]['AH2']):
                    imaginaryPatternName="AH1"
                elif(LastHigh>=ResultMerge.iloc[0]['AH2'] and LastHigh<=ResultMerge.iloc[0]['AH3']):
                    imaginaryPatternName="AH2"
                elif(LastHigh>=ResultMerge.iloc[0]['AH3'] and LastHigh<=ResultMerge.iloc[0]['AH4']):
                    imaginaryPatternName="AH3"
                elif(LastHigh>=ResultMerge.iloc[0]['AH4'] and LastHigh<=ResultMerge.iloc[0]['AH5']):
                    imaginaryPatternName="AH4"
                elif(LastHigh>=ResultMerge.iloc[0]['AH5'] and LastHigh<=ResultMerge.iloc[0]['AH6']):
                    imaginaryPatternName="AH5"
                else:
                    imaginaryPatternName="AH6"        
                #print(imaginaryPatternName + "  -  Imaginary Valid Pattern")
                ImageRealPattern=True
            
            
            #print("H1 = "+str(ResultMerge.iloc[0]['H1']))
            #print("H6 = "+str(ResultMerge.iloc[0]['H6']))
            #print("AH1 = "+str(ResultMerge.iloc[0]['AH1']))
            #print("AH6 = "+str(ResultMerge.iloc[0]['AH6']))
            if((ImageRealPattern==True) & (RealPattern==True)):
                AnnotationsAr.append(CreateAnnotations(FilteredCandles.iloc[ai]['Date'],FilteredCandles.iloc[ai]['high'],iPatternName,'rgb(255, 0, 50)',-3*Size))
                print(FilteredCandles.iloc[ai]['Date'])
                print(PatternName + "  -  Valid Pattern")
                print(imaginaryPatternName + "  -  Imaginary Valid Pattern")
                print("Last minute = "+str(LastCandleMinute))        
                print("Candle Close = "+str(FilteredCandles.iloc[ai]['close']))
        ai=ai+1
    print("**************   "+CandleType+"    *****************")
    return True

def getLiveData():
    global CrudeDf30Min
    global CrudeDf15Min
    TimeIntervals=[900,1800]
    URLDict={}
    StrTimeIntervals=['15M','30M']
    CrudeURL='https://in.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=8849&pair_id_for_news=8849&chart_type=candlestick&pair_interval=INTERVAL&candle_count=CNT&events=patterns_only&volume_series=yes&period='
#ZincURL='https://in.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=49794&pair_id_for_news=49794&chart_type=candlestick&pair_interval=INTERVAL&candle_count=CNT&events=patterns_only&volume_series=yes'
#LeadURL='https://in.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=49784&pair_id_for_news=49784&chart_type=candlestick&pair_interval=INTERVAL&candle_count=CNT&events=patterns_only&volume_series=yes'
#GoldURL='https://in.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=49778&pair_id_for_news=49778&chart_type=candlestick&pair_interval=INTERVAL&candle_count=CNT&events=patterns_only&volume_series=yes'
#URL=GoldURL
#URL=LeadURL
#URL=CrudeURL
    URLDict['Crude']=CrudeURL
#URLDict['Lead']=LeadURL
#URLDict['Zinc']=ZincURL
#URLDict['Gold']=GoldURL
    CrudeDf30Min={}
    CrudeDf15Min={}

    FirstDataSet=True
    for URL1 in URLDict:
        #print(URLDict[URL1])
        URL=URLDict[URL1]
        #N1(Res.index[0],'15M','-')
    
        # Find candles where inverted hammer is detected
        cnt=500
        Index=-1
        #if(True):
        for TimeInterval in TimeIntervals:
            Index=Index+1
        #TimeInterval=TimeIntervals[Index]
            rURL=URL.replace('INTERVAL',str(TimeInterval))
            rURL=rURL.replace('CNT',str(cnt))
        #print(rURL)
            PatternRead= requests.get(rURL,
                                  headers={#'Cookie':'adBlockerNewUserDomains=1545933873; optimizelyEndUserId=oeu1545933885326r0.8381196045732737; _ga=GA1.2.1293495785.1545933889; __gads=ID=d6c605f22775c384:T=1545933894:S=ALNI_MbV20pH_Ga4kGvz2QBdrKhnTQtDsg; __qca=P0-530564802-1545933894749; r_p_s_n=1; G_ENABLED_IDPS=google; _gid=GA1.2.2065111802.1547570711; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A3%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A49774%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A32%3A%22%2Fcommodities%2Fcrude-oil%3Fcid%3D49774%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228849%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Fcommodities%2Fcrude-oil%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228830%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A17%3A%22%2Fcommodities%2Fgold%22%3B%7D%7D%7D%7D; PHPSESSID=t127q9ns2htigac1b5j8lr2tdg; geoC=IN; comment_notification_204870192=1; gtmFired=OK; StickySession=id.51537812219.831in.investing.com; billboardCounter_56=1; nyxDorf=MDFkNWcvMG03YGBtN3pmZTJnNGs0LTI5YGY%3D; _fbp=fb.1.1547680426904.1355133887; ses_id=Nng3dm5hMDg0cGpsNGU1NzRhZDcyMmFjYmJhazo%2FZHJlcTQ6ZTIwdmFuaiRubTklMjQ3NjM3ZmYxM2JrO2xnMjZlNzZuPTBtNDdqZTQzNWE0Y2Q5MjJhamIxYWo6aWQ%2FZTc0N2UxMGZhZGpgbjM5YzIgNyszd2Z3MWNiMjt6ZyA2OTd2bj0wPzRhajA0NTVlNGFkOTI1YTJiamEwOmtkfGUu',
                                           'Referer':'https://in.investing.com/commodities/crude-oil-candlestick',
                                           'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                                           ,'X-Requested-With': 'XMLHttpRequest'
                                           }
                                  ) #GOLD
        #from lxml.html import parse
            Candles=PatternRead.json()['candles']
            DataSet=pd.DataFrame(data=Candles,columns=['Date','open','high','low','close','volume','volume1'])
        
            List_ = list(DataSet['Date'])
        #List_ = [parse(x).strftime for x in List_]
            List_ = [datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S') for x in List_]
            DataSet['Date']=pd.Series([x for x in List_],index=DataSet.index)
            if(TimeInterval==900):
                CrudeDf15Min=DataSet
                DataSet1=DataSet.sort_values(by='Date',ascending=False)
                CrudeDf15Min.to_csv("C:\ReadMoneycontrol\Crude\\Crude15Min_Output_Raw.csv",sep=',',encoding='utf-8')    


                CrudeDf15Min=ProcessCandles(CrudeDf15Min)
            elif(TimeInterval==1800):
                CrudeDf30Min=DataSet
                DataSet1=DataSet.sort_values(by='Date',ascending=False)
                CrudeDf30Min.to_csv("C:\ReadMoneycontrol\Crude\\Crude30Min_Output_Raw.csv",sep=',',encoding='utf-8')                    
                CrudeDf30Min=ProcessCandles(CrudeDf30Min)

    List_ = list(CrudeDf30Min['Date'])
#parse(List_[0] ).hour
    CrudeDf30Min['Hour'] = pd.Series([parse(x).hour for x in List_],index=CrudeDf30Min.index)


    List_ = list(CrudeDf15Min['Date'])
#parse(List_[0] ).hour
    CrudeDf15Min['Hour'] = pd.Series([parse(x).hour for x in List_],index=CrudeDf15Min.index)

#a=pd.DataFrame.ewm(CrudeDf30Min['close'],min_periods=10,adjust=False,span=10).mean()
#CrudeDf30Min

    List_ = list(CrudeDf15Min['Date'])
#List_ = [parse(x).strftime for x in List_]
    List_ = [datetime.strptime(parse(x).strftime("%m/%d/%Y %I:%M %p"), "%m/%d/%Y %I:%M %p") for x in List_]
    CrudeDf15Min['Date']=pd.Series([x for x in List_],index=CrudeDf15Min.index)

    List_ = list(CrudeDf30Min['Date'])
#List_ = [parse(x).strftime for x in List_]
    List_ = [datetime.strptime(parse(x).strftime("%m/%d/%Y %I:%M %p"), "%m/%d/%Y %I:%M %p") for x in List_]
    CrudeDf30Min['Date']=pd.Series([x for x in List_],index=CrudeDf30Min.index)

    CrudeDf15Min.to_csv("C:\ReadMoneycontrol\Crude\\"+datetime.now().strftime("%Y-%m-%d")+"Crude15Min_Output.csv",sep=',',encoding='utf-8')                    
    CrudeDf30Min.to_csv("C:\ReadMoneycontrol\Crude\\"+datetime.now().strftime("%Y-%m-%d")+"Crude30Min_Output.csv",sep=',',encoding='utf-8')                    
    return True

def CurrentDate(D1):
    return N1(N1(D1,"5H","+"),"30M","+")

def CreateLines(date1,date2,value,color,style):
    Lines=[]
    Line={}
    ShapesL={}
    ShapesL['x0']=CurrentDate(date1)
    ShapesL['y0']=value
    ShapesL['x1']=CurrentDate(date2)
    ShapesL['y1']=value
    ShapesL['type']="line"
    ShapesL['opacity']=1
    Line['color']=color
    Line['width']=2
    if(style==True):
        Line['dash']='dot'
    #Line['style']="dot" #dashdot #("solid", "dot", "dash", "longdash", "dashdot", or    "longdashdot")
    ShapesL['line']=Line
    return ShapesL

def CreateAnnotations(date1,y,text,color,arrow):
    Annotations={}
    Annotations['x']=date1#CurrentDate(date1)
    Annotations['y']=y
    Annotations['xref']="x"
    Annotations['yref']="y"
    Annotations['showarrow']=True
    Annotations['text']=text
    Annotations['ax']=0
    Annotations['ay']=20*arrow
    Annotations['arrowhead']=1
    Annotations['arrowcolor']=color
    return Annotations
    
def DisplayCandles():
    global ResultMerge
    global AnnotationsAr
    getLiveData() 
    d1= parse("2019-01-29 04:00")
    d2= parse("2019-01-30 03:00")
    quotes1=CrudeDf30Min
    quotes1 = quotes1[(quotes1['Date'] >= d1) & (quotes1['Date'] <= d2)]
    h1=quotes1['high'].max()
    l1=quotes1['low'].min()
    c1=quotes1['close'].iloc[-1]
    c2=CrudeData.iloc[3]['Price']
    h2=CrudeData.iloc[3]['High']
    l2=CrudeData.iloc[3]['Low']
    g=getPivots((h1+h2)/2,(l1+l2)/2,(c2+c2)/2)
    
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
    
    quotes=CrudeDf30Min
    quotes['MovingAverageLow']=quotes['low'].rolling(window=10).mean()
    quotes['MovingAverageHigh']=quotes['high'].rolling(window=10).mean()
    quotes['MovingAverageLow2']=quotes['low'].rolling(window=3).mean()
    quotes['MovingAverageHigh2']=quotes['high'].rolling(window=3).mean()
    
    quotes15=CrudeDf15Min
    
    #CrudeDf30Min.dtypes
    #quotes = pd.read_csv('SampleYData.csv',
    #                     index_col=0,
    #                     parse_dates=True,
    #                     infer_datetime_format=True)
    
    # select desired range of dates
    quotes = quotes[(quotes['Date'] >= date1) & (quotes['Date'] <= date2)]
    quotes15=quotes15[(quotes15['Date'] >= date1) & (quotes15['Date'] <= date2)]
    
    iquotes = CrudeDf30Min[(CrudeDf30Min['Date'] >= date3) & (CrudeDf30Min['Date'] <= date4)]
    h=quotes['high'].max()
    l=quotes['low'].min()
    
    
    
    ih=iquotes['high'].max()
    il=iquotes['low'].min()
    ic=iquotes['close'].iloc[-1]
    iChartData=getPivots(ih,il,ic)
    
    #Merging the values to the Parent data
    iChartData1={}
    #iChartData1=iChartData
    iChartData1['Date']=CrudeData.iloc[DateIndex]['Date'].strftime("%Y-%m-%d")#CrudeData.iloc[3+DateIndex]['Date']
    iChartData1['AClose']=ic
    iChartData1['APivot']=iChartData['Pivot']
    i=1
    while(i<=6):
        iChartData1['AH'+str(i)]=iChartData['H'+str(i)]
        iChartData1['AL'+str(i)]=iChartData['L'+str(i)]
        i=i+1
    
    a=[]
    a.append(iChartData1)
    #pd.read_json(json.dumps(a)).dtypes
    ResultMerge=CrudeData.merge(pd.read_json(json.dumps(a)))
    ResultMerge.iloc[0]
    
    #.......
    
    iPivot=iChartData['Pivot']
    iPriceList=list(iChartData.values())
    iLowerList=iPriceList[7:]
    iHigherList=iPriceList[1:7]
    
    
    
    
    PriceList=list(CrudeData.iloc[DateIndex])
    Close=CrudeData.iloc[DateIndex]['Price']
    LowerList=PriceList[13:-1]
    HigherList=PriceList[7:-7]
    Pivot=PriceList[len(PriceList)-1]
    
    Lines=[]
    AnnotationsAr=[]
    Layout={}
    AxisText=[]
    AxisValue=[]
    AxisX=[]
    Lines.append(CreateLines(date1,date2,Close,'rgb(255, 0, 0)',False))
    AxisText.append("PreviousClose")
    AxisValue.append(Close)
    Lines.append(CreateLines(date1,date2,Pivot,'rgb(255, 0, 0)',False))
    AxisText.append("Pivot")
    AxisValue.append(Pivot)
    
    #plt.axhline(y=Pivot,linewidth=1, color='y',linestyle=":")
    
    even=1
    for Lower in LowerList:
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if((l-0.5)<Lower):
            Lines.append(CreateLines(date1,date2,Lower,'rgb(0, 0, 255)',False))
            AxisText.append("L"+str(even)+ " ["+str(Lower)+"]")
            AxisValue.append(Lower)
            AxisX.append(CurrentDate(N1(date1,"10M","-")))
            #plt.axhline(y=Lower,linewidth=1, color='r',linestyle=ls)
        even=even+1
        
    even=1
    for Higher in HigherList:
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if(h+0.5>Higher):
            #plt.axhline(y=Higher,linewidth=1, color='g',linestyle=ls)
            Lines.append(CreateLines(date1,date2,Higher,'rgb(0, 255, 0)',False))
            AxisText.append("H"+str(even)+ " ["+str(Higher)+"]")
            AxisValue.append(Higher)
            AxisX.append(CurrentDate(N1(date1,"10M","-")))
        even=even+1   
    
    trace0 = go.Scatter(x=AxisX,y=AxisValue,text=AxisText, mode='text')
    AxisText=[]
    AxisValue=[]
    AxisX=[]
    
    DiplayPrevious=False
    if(DiplayPrevious):
        PriceList=list(CrudeData.iloc[DateIndex-1])
        #Close=CrudeData.iloc[DateIndex-1]['Price']
        LowerList=PriceList[13:-1]
        HigherList=PriceList[7:-7]
        Pivot=PriceList[len(PriceList)-1]     
        even=1
        for Lower in LowerList:
            if(even%2==0):
                ls="--"
            else:
                ls="-."
            if((l-0.5)<Lower):
                Lines.append(CreateLines(date1,date2,Lower,'rgb(0, 100, 255)',False))
                AxisText.append("PL"+str(even)+ " ["+str(Lower)+"]")
                AxisValue.append(Lower)
                AxisX.append(CurrentDate(N1(date2,"20M","+")))
                #plt.axhline(y=Lower,linewidth=1, color='r',linestyle=ls)
            even=even+1
            
        even=1
        for Higher in HigherList:
            if(even%2==0):
                ls="--"
            else:
                ls="-."
            if(h+0.5>Higher):
                #plt.axhline(y=Higher,linewidth=1, color='g',linestyle=ls)
                Lines.append(CreateLines(date1,date2,Higher,'rgb(0, 255, 100)',False))
                AxisText.append("PH"+str(even)+ " ["+str(Higher)+"]")
                AxisValue.append(Higher)
                AxisX.append(CurrentDate(N1(date2,"20M","+")))
            even=even+1 
            
        trace1 = go.Scatter(x=AxisX,y=AxisValue,text=AxisText, mode='text')
        AxisText=[]
        AxisValue=[]
        AxisX=[]
            

    
        
    
    even=1
    for Lower in iLowerList:
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if((l-0.5)<Lower):
            Lines.append(CreateLines(date1,date2,Lower,'rgb(0, 0, 255)',True))
            AxisText.append("AL"+str(7-even)+ " ["+str(Lower)+"]")
            AxisValue.append(Lower)
            AxisX.append(CurrentDate(N1(date1,"1H","-")))
            #plt.axhline(y=Lower,linewidth=1, color='r',linestyle=ls)
        even=even+1
        
    even=1
    for Higher in iHigherList:
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if(h+0.5>Higher):
            #plt.axhline(y=Higher,linewidth=1, color='g',linestyle=ls)
            Lines.append(CreateLines(date1,date2,Higher,'rgb(0, 255, 0)',True))
            AxisText.append("AH"+str(7-even)+ " ["+str(Higher)+"]")
            AxisValue.append(Higher)
            AxisX.append(CurrentDate(N1(date1,"1H","-")))
        even=even+1
    trace2 = go.Scatter(x=AxisX,y=AxisValue,text=AxisText, mode='text')
    #AxisText=[]
    #AxisValue=[]
    #AxisX=[]
    
    
        
        
    zi=0
    #while(zi<len(AxisValue)):
    #    AxisX.append(CurrentDate(date1))
    #    zi=zi+1
    
    
    List_ = list(quotes15['Date'])
    #List_ = [N1(N1(x,"5H","+"),"30M","+") for x in List_]
        
    trace = go.Candlestick(x=List_,
                           open=quotes15['open'],
                           high=quotes15['high'],
                           low=quotes15['low'],
                           close=quotes15['close'])
    
    #trace0 = go.Scatter(x=AxisX,y=AxisValue,text=AxisText, mode='text')
    
    SMAL = go.Scatter(
        x=List_,
        y=quotes['MovingAverageLow'],
        name= 'SMA',
        mode='lines'
        #line="{Line:{color='black'}}"
        )
    
    SMAH = go.Scatter(
        x=List_,
        y=quotes['MovingAverageHigh'],
        name= 'SMA1',
        mode='lines'
        #line="{Line:{color='black'}}"
        )
    
    SMAL2 = go.Scatter(
        x=List_,
        y=quotes['MovingAverageLow2'],
        name= 'SMA2',
        mode='lines'
        #line="{Line:{color='black'}}"
        )
    
    SMAH2 = go.Scatter(
        x=List_,
        y=quotes['MovingAverageHigh2'],
        name= 'SMA12',
        mode='lines'
        #line="{Line:{color='black'}}"
        )
    
    #trace1 = go.Scatter(x=list(FilteredCandles['Date']),y=list(FilteredCandles['high']),text="TUP", mode='markers')
    if(False):
        StartHour=4
        FilteredCandles=quotes[ (quotes['ThreeOutsideUp']==True)  & (quotes['Hour']>=StartHour) ]
        Annotationsi=0
        while(Annotationsi<len(FilteredCandles)):
            AnnotationsAr.append(CreateAnnotations(FilteredCandles.iloc[Annotationsi]['Date'],FilteredCandles.iloc[Annotationsi]['low'],"TOUP",'rgb(50, 255, 50)',1))
            Annotationsi=Annotationsi+1
        
        FilteredCandles=quotes[ (quotes['ThreeInsideUp']==True)  & (quotes['Hour']>=StartHour) ]
        Annotationsi=0
        while(Annotationsi<len(FilteredCandles)):
            AnnotationsAr.append(CreateAnnotations(FilteredCandles.iloc[Annotationsi]['Date'],FilteredCandles.iloc[Annotationsi]['low'],"TIUP",'rgb(50, 255, 50)',1))
            Annotationsi=Annotationsi+1
        
        FilteredCandles=quotes[ (quotes['ThreeInsideDown']==True)  & (quotes['Hour']>=StartHour) ]
        Annotationsi=0
        while(Annotationsi<len(FilteredCandles)):
            AnnotationsAr.append(CreateAnnotations(FilteredCandles.iloc[Annotationsi]['Date'],FilteredCandles.iloc[Annotationsi]['high'],"TIDown",'rgb(255, 0, 0)',-1))
            Annotationsi=Annotationsi+1
            
        FilteredCandles=quotes[ (quotes['ThreeOutsideDown']==True)  & (quotes['Hour']>=StartHour) ]
        Annotationsi=0
        while(Annotationsi<len(FilteredCandles)):
            AnnotationsAr.append(CreateAnnotations(FilteredCandles.iloc[Annotationsi]['Date'],FilteredCandles.iloc[Annotationsi]['high'],"TODown",'rgb(255, 0, 50)',-1))
            Annotationsi=Annotationsi+1
            
        FilteredCandles=quotes15[ (quotes15['ThreeOutsideUp']==True)  & (quotes15['Hour']>=StartHour) ]
        Annotationsi=0
        while(Annotationsi<len(FilteredCandles)):
            AnnotationsAr.append(CreateAnnotations(FilteredCandles.iloc[Annotationsi]['Date'],FilteredCandles.iloc[Annotationsi]['low'],"15TOUP",'rgb(50, 255, 50)',2))
            Annotationsi=Annotationsi+1
        
        FilteredCandles=quotes15[ (quotes15['ThreeInsideUp']==True)  & (quotes15['Hour']>=StartHour) ]
        Annotationsi=0
        while(Annotationsi<len(FilteredCandles)):
            AnnotationsAr.append(CreateAnnotations(FilteredCandles.iloc[Annotationsi]['Date'],FilteredCandles.iloc[Annotationsi]['low'],"15TIUP",'rgb(50, 255, 50)',2))
            Annotationsi=Annotationsi+1
        
        FilteredCandles=quotes15[ (quotes15['ThreeInsideDown']==True)  & (quotes15['Hour']>=StartHour) ]
        Annotationsi=0
        while(Annotationsi<len(FilteredCandles)):
            AnnotationsAr.append(CreateAnnotations(FilteredCandles.iloc[Annotationsi]['Date'],FilteredCandles.iloc[Annotationsi]['high'],"15TIDown",'rgb(255, 0, 0)',-2))
            Annotationsi=Annotationsi+1
            
        FilteredCandles=quotes15[ (quotes['ThreeOutsideDown']==True)  & (quotes15['Hour']>=StartHour) ]
        Annotationsi=0
        while(Annotationsi<len(FilteredCandles)):
            AnnotationsAr.append(CreateAnnotations(FilteredCandles.iloc[Annotationsi]['Date'],FilteredCandles.iloc[Annotationsi]['high'],"15TODown",'rgb(255, 0, 50)',-2))
            Annotationsi=Annotationsi+1
            
        
    #[trace].extend([trace0])
    #data=[trace,trace0,SMAL,SMAH,SMAL2,SMAH2]
    #data=[trace,trace0,trace1,trace2]
    if(DiplayPrevious):
        data=[trace,trace0,trace1,trace2]
    else:        
        data=[trace,trace0,trace2]
    #data=[trace,trace0]
    #fig = FF.create_candlestick(quotes['open'], quotes['high'], quotes['low'], quotes['close'], dates=quotes['Date'])
    # Create Line of open values
    #add_line = Scatter(x=df.index,y=df.Open,name= 'Open Vals',line=Line(color='black'))
    #fig['data'].extend([add_line])
    
    
    
    #Lines.append(CreateLines(date1,date2,53,'rgb(255, 0, 0)'))
    #Lines.append(CreateLines(date1,date2,52,'rgb(255, 0, 0)'))
    Layout["shapes"]=Lines
    Layout["annotations"]=AnnotationsAr
    
    a=[]
    a.append(iChartData1)
    #pd.read_json(json.dumps(a)).dtypes
    ResultMerge=CrudeData.merge(pd.read_json(json.dumps(a)))
    
    StartHour=4
    FilteredCandles=quotes[ (quotes['ThreeOutsideUp']==True)  & (quotes['Hour']>=StartHour) ]
    if(len(FilteredCandles)>0):
        Filter30MinUPCandles(FilteredCandles,"TOUP^^","ThreeOutsideUp",.75,quotes)
    FilteredCandles=quotes[ (quotes['ThreeInsideUp']==True)  & (quotes['Hour']>=StartHour) ]
    if(len(FilteredCandles)>0):
        Filter30MinUPCandles(FilteredCandles,"TIUP^^","ThreeInsideUp",.75,quotes)
    FilteredCandles=quotes[ (quotes['ThreeOutsideDown']==True)  & (quotes['Hour']>=StartHour) ]
    if(len(FilteredCandles)>0):
        Filter30MinDownCandles(FilteredCandles,"TIDOWN^^","ThreeInsideDown",.75,quotes)
    FilteredCandles=quotes[ (quotes['ThreeInsideDown']==True)  & (quotes['Hour']>=StartHour) ]
    if(len(FilteredCandles)>0):
        Filter30MinDownCandles(FilteredCandles,"TIDOWN^^","ThreeInsideDown",.75,quotes)
    
    if(False):
        FilteredCandles=quotes15[ (quotes15['ThreeOutsideUp']==True)  & (quotes15['Hour']>=StartHour) ]
        if(len(FilteredCandles)>0):
            Filter30MinUPCandles(FilteredCandles,"*15TOUP","ThreeOutsideUp",1.1,quotes)
        FilteredCandles=quotes15[ (quotes15['ThreeInsideUp']==True)  & (quotes15['Hour']>=StartHour) ]
        if(len(FilteredCandles)>0):
            Filter30MinUPCandles(FilteredCandles,"*15TIUP","ThreeInsideUp",1.1,quotes)
        FilteredCandles=quotes15[ (quotes15['ThreeOutsideDown']==True)  & (quotes15['Hour']>=StartHour) ]
        if(len(FilteredCandles)>0):
            Filter30MinDownCandles(FilteredCandles,"*15TIDOWN","ThreeInsideDown",1.1,quotes)
        FilteredCandles=quotes15[ (quotes15['ThreeInsideDown']==True)  & (quotes15['Hour']>=StartHour) ]
        if(len(FilteredCandles)>0):
            Filter30MinDownCandles(FilteredCandles,"*15TIDOWN","ThreeInsideDown",1.1,quotes)
            
    pi=1
    while(pi<=6):
        print("L"+str(pi)+" = " + str(ResultMerge.iloc[0]["L"+str(pi)]))
        print("H"+str(pi)+" = " + str(ResultMerge.iloc[0]["H"+str(pi)]))
        pi=pi+1
    
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
    plot(fig, filename="Crude-US-"+date1.strftime("%b-%d")+".html",auto_open=False)
    
    
#getPivots
rURL="https://in.investing.com/instruments/HistoricalDataAjax"
Data="curr_id=8849&smlID=300060&header=Crude+Oil+WTI+Futures+Historical+Data&st_date=03%2F02%2F2006&end_date=02%2F02%2F2020&interval_sec=Daily&sort_col=date&sort_ord=DESC&action=historical_data"
#https://in.investing.com/instruments/HistoricalDataAjax
PatternRead= requests.post(rURL,
                                  headers={#'Cookie':'adBlockerNewUserDomains=1545933873; optimizelyEndUserId=oeu1545933885326r0.8381196045732737; _ga=GA1.2.1293495785.1545933889; __gads=ID=d6c605f22775c384:T=1545933894:S=ALNI_MbV20pH_Ga4kGvz2QBdrKhnTQtDsg; __qca=P0-530564802-1545933894749; r_p_s_n=1; G_ENABLED_IDPS=google; _gid=GA1.2.2065111802.1547570711; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A3%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bi%3A49774%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A32%3A%22%2Fcommodities%2Fcrude-oil%3Fcid%3D49774%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228849%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Fcommodities%2Fcrude-oil%22%3B%7Di%3A2%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228830%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A17%3A%22%2Fcommodities%2Fgold%22%3B%7D%7D%7D%7D; PHPSESSID=t127q9ns2htigac1b5j8lr2tdg; geoC=IN; comment_notification_204870192=1; gtmFired=OK; StickySession=id.51537812219.831in.investing.com; billboardCounter_56=1; nyxDorf=MDFkNWcvMG03YGBtN3pmZTJnNGs0LTI5YGY%3D; _fbp=fb.1.1547680426904.1355133887; ses_id=Nng3dm5hMDg0cGpsNGU1NzRhZDcyMmFjYmJhazo%2FZHJlcTQ6ZTIwdmFuaiRubTklMjQ3NjM3ZmYxM2JrO2xnMjZlNzZuPTBtNDdqZTQzNWE0Y2Q5MjJhamIxYWo6aWQ%2FZTc0N2UxMGZhZGpgbjM5YzIgNyszd2Z3MWNiMjt6ZyA2OTd2bj0wPzRhajA0NTVlNGFkOTI1YTJiamEwOmtkfGUu',
                                           'Referer':'https://in.investing.com/commodities/crude-oil-historical-data',
                                           'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                                           ,'X-Requested-With': 'XMLHttpRequest'
                                           ,"Content-Type": "application/x-www-form-urlencoded"
                                           },
                                          data=Data
                                  ) #GOLD
PatternRead.text
CrudeData1 = pd.read_html(PatternRead.text)[0]
i=-1
Pivot=[]
while(i<len(CrudeData1)-1):
    i=i+1
    Res=getPivots(CrudeData1.iloc[i]['High'],CrudeData1.iloc[i]['Low'],CrudeData1.iloc[i]['Price'])
    Res['Date']=CrudeData1.iloc[i]['Date']
    Pivot.append(Res)

List_ = list(CrudeData1['Date'])
List_ = [datetime.strptime(parse(x).strftime("%m/%d/%Y %I:%M %p"), "%m/%d/%Y %I:%M %p") for x in List_]
CrudeData1['Date']=pd.Series([x for x in List_],index=CrudeData1.index)
Pivotdf=pd.read_json(json.dumps(Pivot))    
CrudeData=CrudeData1.merge(Pivotdf)

OverRide=False
DateIndex=1  #Current Date Set the value to 1

Monday=False
if(Monday):
    OverRide=True
    DateIndex=3
###Change it to True for Monday
#### Change it only for monday For WeekDay Start DataIndex should be 2
#OverRide=True
##########################################################################
 #For Monday it is 3

#############################################################################
StartTime=datetime.now()
DisplayCandles()

#########################################
