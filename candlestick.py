import re
import requests
import pandas as pd
import datetime
from datetime import datetime, timedelta
import json
import time
import numpy as np
from dateutil.parser import parse
import plotly.graph_objs as go
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import plotly.io as pio
import os
from plotly.tools import FigureFactory as FF

__builders = dict()
__default_ohlc = ['open', 'high', 'low', 'close']
Profit=dict()


def __get_file_name(class_name):
    res = re.findall('[A-Z][^A-Z]*', class_name)
    return '_'.join([cur.lower() for cur in res])


def __load_module(module_path):
    p = module_path.rfind('.') + 1
    super_module = module_path[p:]
    try:
        module = __import__(module_path, fromlist=[super_module], level=0)
        return module
    except ImportError as e:
        raise e


def __get_class_by_name(class_name):
    file_name = __get_file_name(class_name)
    mod_name = 'candlestick.patterns.' + file_name

    if mod_name not in __builders:
        module = __load_module(mod_name)
        __builders[mod_name] = module
    else:
        module = __builders[mod_name]
    return getattr(module, class_name)


def __create_object(class_name, target):
    return __get_class_by_name(class_name)(target=target)

def approximateEqual(a, b):
    left=abs(round((a-b)*100)/100)
    right=round(a*100)/100000    
    return left <= right;

def bullish_hanging_man(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    bullhm = __create_object('BullishHangingMan', target)
    return bullhm.has_pattern(candles_df, ohlc, is_reversed)

def bearish_harami_cross(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    bullharm = __create_object('BearishHaramiCross', target)
    return bullharm.has_pattern(candles_df, ohlc, is_reversed)

def bearish_spinning_top(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    bearishspinningtop = __create_object('BearishSpinningTop', target)
    return bearishspinningtop.has_pattern(candles_df, ohlc, is_reversed)


def hanging_man(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    bearhm = __create_object('HangingMan', target)
    return bearhm.has_pattern(candles_df, ohlc, is_reversed)


def bearish_harami(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    bear_harami = __create_object('BearishHarami', target)
    return bear_harami.has_pattern(candles_df, ohlc, is_reversed)


def bullish_harami(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    bull_harami = __create_object('BullishHarami', target)
    return bull_harami.has_pattern(candles_df, ohlc, is_reversed)


def gravestone_doji(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    gs_doji = __create_object('GravestoneDoji', target)
    return gs_doji.has_pattern(candles_df, ohlc, is_reversed)


def dark_cloud_cover(candles_df,
                     ohlc=__default_ohlc,
                     is_reversed=False,
                     target=None):
    dcc = __create_object('DarkCloudCover', target)
    return dcc.has_pattern(candles_df, ohlc, is_reversed)


def doji(candles_df,
         ohlc=__default_ohlc,
         is_reversed=False,
         target=None):
    doji = __create_object('Doji', target)
    return doji.has_pattern(candles_df, ohlc, is_reversed)


def doji_star(candles_df,
              ohlc=__default_ohlc,
              is_reversed=False,
              target=None):
    doji = __create_object('DojiStar', target)
    return doji.has_pattern(candles_df, ohlc, is_reversed)


def dragonfly_doji(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    doji = __create_object('DragonflyDoji', target)
    return doji.has_pattern(candles_df, ohlc, is_reversed)


def bearish_engulfing(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BearishEngulfing', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)


def bullish_engulfing(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BullishEngulfing', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)


def hammer(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('Hammer', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)


def inverted_hammer(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('InvertedHammer', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)


def morning_star(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('MorningStar', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)


def morning_star_doji(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('MorningStarDoji', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)


def piercing_pattern(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('PiercingPattern', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)


def rain_drop(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('RainDrop', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)


def rain_drop_doji(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('RainDropDoji', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)


def star(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('Star', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)


def shooting_star(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ShootingStar', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bearish_inverted_hammer_stick(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BearishInvertedHammerStick', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def bearish_marbozu(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('BearishMarbozu', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def three_inside_up(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ThreeInsideUp', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def three_inside_down(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ThreeInsideDown', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def three_outside_up(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ThreeOutsideUp', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def three_outside_down(candles_df,
                   ohlc=__default_ohlc,
                   is_reversed=False,
                   target=None):
    cndl = __create_object('ThreeOutsideDown', target)
    return cndl.has_pattern(candles_df, ohlc, is_reversed)

def MaRound(n):
    return round(n*100/100,2)
	

def getGoldPivots1(Open,High,Low,Close,Set,Option,Details):
    Points={}
    #pivot,re1,re2,re3,re4,su1,su2,su3,su4,High,Close,Low
    #Open=32170
    #High=32298
    #Low=31871
    #Close=31948
    if(Option==4):
        pivot= MaRound((Open+High+Low+Close)/4)
    else:
        pivot= MaRound((Close+High+Low)/3)
    if(Set=="C"):
        R1 = MaRound(Close+(High-Low)*(1.1/12))
        S1 = MaRound(Close-(High-Low)*(1.1/12))
    elif(Set=="D"):
        R1 = MaRound(2*pivot-Low)
        S1 = MaRound(2*pivot-High)
    Range=High-Low
    R2=MaRound(pivot+Range)
    S2=MaRound(pivot-Range)
    R3=MaRound(pivot+(Range*2))
    S3=MaRound(pivot-(Range*2))
    R4=MaRound(pivot+(Range*3))   
    S4=MaRound(pivot-(Range*3))
    
    
    pivotmR1=MaRound((R1+pivot)/2)
    pivotmS1=MaRound((S1+pivot)/2)
    R1mR2=MaRound((R1+R2)/2)
    
    R2mR3=MaRound((R3+R2)/2)
    R3mR4=MaRound((R3+R4)/2)
    S1mS2=MaRound((S1+S2)/2)
    
    S2mS3=MaRound((S3+S2)/2)
    
    S3mS4=MaRound((S3+S4)/2)
    
    #S2=2*pivot-High
    #R1=2*pivot+Low
    
    
    
    Points["IPivot"]=pivot
    if((Details=="Major") or (Details=="All")):
        Points["H4"]=R4
        Points["H3"]=R3    
        Points["H2"]=R2    
        Points["H1"]=R1    
        Points["L4"]=S4    
        Points["L3"]=S3    
        Points["L2"]=S2    
        Points["L1"]=S1    
    if((Details=="Mid") or (Details=="All")):
        Points["H3M1"]=R3mR4
        Points["H2M1"]=R2mR3
        Points["H1M1"]=R1mR2
        Points["H0M1"]=pivotmR1
        Points["L3M1"]=S3mS4
        Points["L2M1"]=S2mS3
        Points["L1M1"]=S1mS2
        Points["L0M1"]=pivotmS1
    if((Details=="Minor") or (Details=="All")):
        Points["H0M0"]=MaRound((pivotmR1+pivot)/2)
        Points["H0M2"]=MaRound((pivotmR1+R1)/2)
        Points["H1M0"]=MaRound((R1+R1mR2)/2)
        Points["H1M2"]=MaRound((R2+R1mR2)/2)
        Points["H2M0"]=MaRound((R2+R2mR3)/2)
        Points["H2M2"]=MaRound((R3+R2mR3)/2)
        Points["H3M0"]=MaRound((R3+R3mR4)/2)
        Points["H3M2"]=MaRound((R4+R3mR4)/2)
        Points["L0M0"]=MaRound((pivotmS1+pivot)/2)
        Points["L0M2"]=MaRound((pivotmS1+S1)/2)
        Points["L1M0"]=MaRound((S1+S1mS2)/2)
        Points["L1M2"]=MaRound((S2+S1mS2)/2)
        Points["L2M0"]=MaRound((S2+S2mS3)/2)
        Points["L2M2"]=MaRound((S3+S2mS3)/2)
        Points["L3M0"]=MaRound((S3+S3mS4)/2)
        Points["L3M2"]=MaRound((S4+S3mS4)/2)
    return Points

def Check(tdaily,Signal,DateIndex,Margin,Stoploss,SearchData):
    SingleStatus={}

    #global Profit
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


def datediff(d1, d2):
    return abs((d2 - d1).seconds)


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

def CreateLinesV1(date1,date2,value,color,style):
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
    if(style==1):
        Line['dash']='dot'
    elif(style==2):
        Line['dash']='dash'
    elif(style==3):
        Line['dash']='longdash'
    elif(style==4):
        Line['dash']='dashdot'
    else:
        Line['dash']='solid'
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
	
def getResultData(CData):
    NewDataSetAr=[]
    i=1
    #i=1126
    while(i<len(CData)):
        DataSet={}
        DataSet['Date']=CData['Date'][i]
        O=CData['open'][i]
        H=CData['high'][i]
        L=CData['low'][i]
        C=CData['close'][i]
        O1=CData['open'][i-1]
        H1=CData['high'][i-1]
        L1=CData['low'][i-1]
        C1=CData['close'][i-1]
        if((C-O)>0):
            CurrentCandlePercent=(C-O)/O*10000
            CurrentCandleColour="G"
        else:
            CurrentCandlePercent=(O-C)/C*10000
            CurrentCandleColour="R"
        if((C1-O1)>0):
            PreviousCandlePercent=(C1-O1)/O1*10000
            PreviousCandleColour="G"
        else:
            PreviousCandlePercent=(O1-C1)/C1*10000
            PreviousCandleColour="R"
        DataSet['PCC']=PreviousCandleColour
        DataSet['PCP']=round(PreviousCandlePercent,2)
        DataSet['CCC']=CurrentCandleColour
        DataSet['CCP']=round(CurrentCandlePercent,2)
        
        if(CurrentCandleColour=='G'):
            LDIFF=(L-L1)/L*100
            DataSet['LDIFF']=round((L-L1)/L*10000,2)
        else:
            LDIFF=(L1-L)/L1*100
            DataSet['LDIFF']=round((L1-L)/L1*10000,2)
            
        #or (C1==H) or (C1==L) its giving incorrect answer
        if (((C1==O) ) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameOpen']=True
        else:
            DataSet['SameOpen']=False
        if ((L1==L) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameLow']=True
        else:
            DataSet['SameLow']=False
        if ((H1==H) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameHigh']=True
        else:
            DataSet['SameHigh']=False
        tolerance=O*0.008/10 
        if (((O-tolerance) <=C1 <= (O+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameOpenT']=True
        else:
            DataSet['SameOpenT']=False
        
        tolerance=L1*0.008/10 
        if (((L1-tolerance) <= L <= (L1+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameLowT']=True
        else:
            DataSet['SameLowT']=False
        
        tolerance=L1*0.008/10 
        if (((L-tolerance) <= L1 <= (L+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameLowT2']=True
        else:
            DataSet['SameLowT2']=False
            
        tolerance=L1*0.008/10 
        if (((L1>=L+tolerance) or (L1<=L-tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameLowT1']=True
        else:
            DataSet['SameLowT1']=False
        
        
        tolerance=C1*0.008/10
        if (((C1-tolerance) <= C <= (C1+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameCloseT']=True
        else:
            DataSet['SameCloseT']=False
        
        tolerance=H1*0.008/10 
        if (((H-tolerance) <= H1 <= (H+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameHighT']=True
        else:
            DataSet['SameHighT']=False
        
        tolerance=H1*0.008/10 
        if (((H1-tolerance) <= H <= (H1+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameHighT1']=True
        else:
            DataSet['SameHighT1']=False
            
        tolerance=H1*0.008/10 
        if (((H1-tolerance) <= O <= (H1+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameOvsH1']=True
        else:
            DataSet['SameOvsH1']=False
            
        tolerance=H*0.008/10 
        if (((H-tolerance) <= C1 <= (H+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameC1vsH']=True
        else:
            DataSet['SameC1vsH']=False
            
        tolerance=H*(0.008/10*2) 
        if (((H-tolerance) <= C1 <= (H+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameC1vsH2']=True
        else:
            DataSet['SameC1vsH2']=False
            
        tolerance=L1*0.008/10 
        if (((L1-tolerance) <= O <= (L1+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameOvsL1']=True
        else:
            DataSet['SameOvsL1']=False
            
        tolerance=L*0.008/10 
        if (((L-tolerance) <= C1 <= (L+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameC1vsL']=True
        else:
            DataSet['SameC1vsL']=False
            
        tolerance=L*(0.008/10*2) 
        if (((L-tolerance) <= C1 <= (L+tolerance)) and (PreviousCandleColour!=CurrentCandleColour)):
            DataSet['SameC1vsL2']=True
        else:
            DataSet['SameC1vsL2']=False
            
        
        if(CurrentCandleColour=='G'):
            DataSet['PDIFF']=round(PreviousCandlePercent/CurrentCandlePercent*100,2)
        else:
            DataSet['PDIFF']=round(CurrentCandlePercent/PreviousCandlePercent*100,2)
        
        NewDataSetAr.append(DataSet)
        i=i+1
    
    Test=pd.DataFrame(NewDataSetAr)
    
    iResults1=pd.merge(Test, CData, how='outer', indicator='Exist') 
    return iResults1

def MParseDate(Date):
    ts = (np.datetime64(pd.to_datetime(Date)) - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    return N1(N1(datetime.utcfromtimestamp(ts),'5H',"+"),"30M","+")

def getLiveDataFromZerodha(Symbol,Interval):
#    global Candle30Min
#    global Candle15Min
#    global Candle5Min
    StrTimeIntervals=['minute','3minute','5minute','15minute','30minute']
    for TimeInterval in StrTimeIntervals:
        if(TimeInterval==Interval):
            if(Symbol=="GOLD"):
                SymbolID="54015239"
            else:
                SymbolID="53869575"
            if(Interval=="minute"):
                Candles = requests.get('https://kitecharts-aws.zerodha.com/api/chart/'+SymbolID+'/'+TimeInterval+'?public_token=Pb0MyvJ435vcAjx5fxCTtEV0oD0wdcwT&user_id=RM5678&api_key=kitefront&access_token=mwFtysT9JpZk6B7ZOUH4AqbrJkhUlTnC&from=2019-04-08&to=2019-12-05&ciqrandom=1549306657305') #GOLD
            else:
                Candles = requests.get('https://kitecharts-aws.zerodha.com/api/chart/'+SymbolID+'/'+TimeInterval+'?public_token=Pb0MyvJ435vcAjx5fxCTtEV0oD0wdcwT&user_id=RM5678&api_key=kitefront&access_token=mwFtysT9JpZk6B7ZOUH4AqbrJkhUlTnC&from=2019-01-08&to=2019-12-05&ciqrandom=1549306657305') #GOLD
            Candles_dict = Candles.json()['data']['candles']
            Candles_df = pd.DataFrame(Candles_dict,columns=['Date', 'open', 'high', 'low', 'close', 'V'])
			#candles5min_df['T'] = pd.to_datetime(candles5min_df['T'], unit='ms')
			#List_ = list(Candles_df['Date'])
			#List_ = [parse(x) for x in List_]
			#Candles_df['Date']=pd.Series([x for x in List_],index=Candles_df.index)
            List_ = list(Candles_df['Date'])
		#List_ = [parse(x).strftime for x in List_]
            List_ = [datetime.strptime(MParseDate(x).strftime("%m/%d/%Y %I:%M %p"), "%m/%d/%Y %I:%M %p") for x in List_]
            Candles_df['Date']=pd.Series([x for x in List_],index=Candles_df.index)
            Candle=Candles_df			
            List_ = list(Candle['Date'])
            Candle['Hour'] = pd.Series([x.hour for x in List_],index=Candle.index)
            return Candle

def GetEODDataFromMCX(Symbol,PivotType,OHLC):
    rURL="https://www.mcxindia.com/backpage.aspx/GetCommoditywiseBhavCopy"
    #PayLoad="{'Symbol':'CRUDEOIL','Expiry':'19FEB2019','FromDate':'','ToDate':'','InstrumentName':'FUTCOM'}"
    if(Symbol=="GOLD"):
        PayLoad="{'Symbol':'GOLD','Expiry':'05JUN2019','FromDate':'','ToDate':'','InstrumentName':'FUTCOM'}"
    else:
        PayLoad="{'Symbol':'SILVER','Expiry':'03MAY2019','FromDate':'','ToDate':'','InstrumentName':'FUTCOM'}"
    #PayLoad="{'Symbol':'CRUDEOIL','Expiry':'19MAR2019','FromDate':'','ToDate':'','InstrumentName':'FUTCOM'}"
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
    Data1=Candles_df.iloc[:40][['Symbol','Date','Open','High','Low','Close']]
    i=-1
    Pivot=[]
    while(i<len(Data1)-1):
        i=i+1
		#Res=getPivots(CrudeData1.iloc[i]['High'],CrudeData1.iloc[i]['Low'],CrudeData1.iloc[i]['Price'])
        Res=getGoldPivots1(Data1.iloc[i]['Open'],Data1.iloc[i]['High'],Data1.iloc[i]['Low'],Data1.iloc[i]['Close'],PivotType,OHLC,"All")
		#Res=getGoldPivots1(CrudeData1.iloc[i]['Open'],CrudeData1.iloc[i]['High'],CrudeData1.iloc[i]['Low'],CrudeData1.iloc[i]['Price'])
		#Res['Date']=CrudeData1.iloc[i]['Date']    
		#Pivot.append(Res)
        Res['Date']=Data1.iloc[i]['Date']
        Pivot.append(Res)
    List_ = list(Data1['Date'])
    List_ = [datetime.strptime(parse(x).strftime("%m/%d/%Y %I:%M %p"), "%m/%d/%Y %I:%M %p") for x in List_]
    Data1['Date']=pd.Series([x for x in List_],index=Data1.index)
    Pivotdf=pd.read_json(json.dumps(Pivot))    
    CrudeData=Data1.merge(Pivotdf)
    return CrudeData
				
			
    
def DisplayCandles(CrudeData,DateIndex,Candle30Min,Candle15Min,Symbol,OverRide):
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
            Lines.append(CreateLinesV1(date1,date2,Lower,'rgb(0, 0, 255)',1))
            AxisText.append("L"+str(even)+ "M ["+str(Lower)+"]")
            AxisValue.append(Lower)
            
            AxisX.append(CurrentDate(N1(date2,"10M","-")))
        even=even+1
        
    even=1
    for Higher in HigherMList:
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if(h+Tolerance>Higher):
            #plt.axhline(y=Higher,linewidth=1, color='g',linestyle=ls)
            Lines.append(CreateLinesV1(date1,date2,Higher,'rgb(0, 255, 0)',1))
            AxisText.append("H"+str(even)+ "M ["+str(Higher)+"]")
            AxisValue.append(Higher)
            AxisX.append(CurrentDate(N1(date2,"10M","-")))#            
        even=even+1 
        
    for Lower in LowerMinList:
        #Lower=LowerList[even]
        if(even%2==0):
            ls="--"
        else:
            ls="-."
        if((l-Tolerance)<Lower): #Change from 0.5 to 0.1
            Lines.append(CreateLinesV1(date1,date2,Lower,'rgb(0, 90, 255)',3))
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
            Lines.append(CreateLinesV1(date1,date2,Higher,'rgb(90, 255, 0)',3))
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
    plot(fig, filename=Symbol+"-IN-"+date1.strftime("%b-%d")+"V2.html",auto_open=False)
    print(Symbol+"-IN-"+date1.strftime("%b-%d")+"V2.html")
