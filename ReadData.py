# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 22:20:04 2018

@author: lalitha
"""

import pandas as pd
import numpy as np
import datetime
import math
import re
import matplotlib
from dateutil.parser import parse

import matplotlib.pyplot as plt
#from matplotlib.finance import quotes_historical_yahoo_ohlc
from matplotlib.lines import Line2D
#https://stackoverflow.com/questions/44810875/how-to-draw-a-classic-stock-chart-with-matplotlib
daily0=pd.read_csv('C:\ReadMoneycontrol\Crude\dailyData.csv')
List_ = list(daily0['Date'])
List_ = [datetime.datetime.strptime(parse(x).strftime("%m/%d/%Y"), "%m/%d/%Y") for x in List_]
daily0['Date']=pd.Series([x for x in List_],index=daily0.index)
daily0['Weekday']=pd.Series([x.weekday() for x in List_],index=daily0.index)

Weekday = daily0.groupby(['Weekday'])['Weekday'].count()
data1=daily0
daily0['Close-Low']=np.round(daily0['Close']-daily0['Low'])
daily0['High-Low']=np.round(daily0['High']-daily0['Low'])
#daily0['High-Low']=np.round(daily0['High']-daily0['Low'])
daily0['Ceil']=np.round(daily0['High-Low']/daily0['Close-Low'])+1

daily0['Val1'] = np.where(daily0['High-Low']/daily0['Close-Low']>2, daily0['Close-Low']*daily0['Ceil'], daily0['Close-Low'])
daily0['Val2'] = np.where(daily0['Val1']>130, daily0['Val1']/3, daily0['Val1'])# changed from 'Val1']/2 to 'Val1']/3
daily0['Val3'] = np.round(daily0['High']/daily0['Low']*daily0['Close'])
daily0['BuyP'] = np.round(1.1*daily0['Val2']/4+daily0['Close'])
daily0['BuyT'] = np.round((daily0['BuyP']+daily0['Val3'])/2)
daily0['BuySL'] = np.round(daily0['Close']-(1.1*daily0['High-Low']/4))  #=F157-(1.1*R157/4)-Y157
daily0['SellP']= np.round(daily0['Close']-(1.1*daily0['Val2']/4)) #=F157-(1.1*O157/4)+Y157
daily0['SellT']= np.round(daily0['Close']-(1.1*daily0['Val2']/math.sqrt(2))) #=F157-(1.1*O157/SQRT(2))+Z157
daily0['SellSL']= np.round(daily0['Close']+(1.1*daily0['High-Low']/4)) #=F157+(1.1*R157/4)+Y157
#=(1.1*O172/4)+F172

#=IF(R172/Q172>2,Q172*S172,Q172)

#=IF(R172/Q172>2,Q172*S172,Q172)
daily1=pd.read_csv('C:\ReadMoneycontrol\Crude\dailyData.csv')
List_ = list(daily1['Date'])
List_ = [datetime.datetime.strptime(parse(x).strftime("%m/%d/%Y"), "%m/%d/%Y") for x in List_]
daily1['Date']=pd.Series([x for x in List_],index=daily1.index)
daily1['Weekday']=pd.Series([x.weekday() for x in List_],index=daily1.index)

Weekday = daily1.groupby(['Weekday'])['Weekday'].count()
data1=daily1
daily1['Close-Low']=np.round(daily1['Close']-daily1['Low'])
daily1['HdLmC']=np.round(daily1['High']/daily1['Low']*daily1['Close'])
daily1['High-Low']=np.round(daily1['High']-daily1['Low'])
#daily1['High-Low']=np.round(daily1['High']-daily1['Low'])
daily1['Ceil']=np.round(daily1['High-Low']/daily1['Close-Low'])+1

daily1['Val1'] = np.where(daily1['High-Low']/daily1['Close-Low']>2, daily1['Close-Low']*daily1['Ceil'], daily1['Close-Low'])
daily1['Val2'] = np.where(daily1['Val1']>130, daily1['Val1']/2, daily1['Val1'])
daily1['Val3'] = np.round(daily1['High']/daily1['Low']*daily1['Close'])
daily1['BuyP'] = np.round(1.1*daily1['Close-Low']/4+daily1['Close']) #=(1.1*(Close-Low)/4)+Close
daily1['BuyT'] = np.round((daily1['BuyP']+daily1['HdLmC'])/2) #=(BuyP+HdLmC)/2
daily1['BuySL'] = np.round(daily1['Close']-(1.1*daily1['High-Low']/4))  #=Close-(1.1*(High-Low)/4)
daily1['SellP']= np.round(daily1['Close']-(1.1*daily1['Close-Low']/4)) #=Close-(1.1*(Close-Low)/4)
daily1['SellT']= np.round(daily1['Close']-(1.1*daily1['Close-Low']/math.sqrt(3))) #==Close-(1.1*(Close-Low)/SQRT(2))
daily1['SellSL']= np.round(daily1['Close']+(1.1*daily1['High-Low']/4)) #=Close+(1.1*(High-Low)/4)
#=(1.1*O172/4)+F172

#daily1['SellP']= np.round(daily1['Open']-1.1*(daily1['High']-daily1['Open'])/3) #=(1.1*(Close-Low)/4)+Close
#daily1['SellT']= np.round(daily1['SellP']-(daily1['HdLmC']-daily1['SellP'])/2) #=(BuyP+HdLmC)/2
#daily1['SellSL']= np.round(daily1['Open']+(1.1*(daily1['High']-daily1['Open'])/3))  #=Close-(1.1*(High-Low)/4)


#=IF(R172/Q172>2,Q172*S172,Q172)

daily2=pd.read_csv('C:\ReadMoneycontrol\Crude\dailyData.csv')
List_ = list(daily2['Date'])
List_ = [datetime.datetime.strptime(parse(x).strftime("%m/%d/%Y"), "%m/%d/%Y") for x in List_]
daily2['Date']=pd.Series([x for x in List_],index=daily2.index)
daily2['Weekday']=pd.Series([x.weekday() for x in List_],index=daily2.index)

Weekday = daily2.groupby(['Weekday'])['Weekday'].count()
data1=daily2
daily2['Close-Low']=np.round(daily2['Close']-daily2['Low'])
daily2['High-Low']=np.round(daily2['High']-daily2['Low'])
#daily2['High-Low']=np.round(daily2['High']-daily2['Low'])
daily2['Ceil']=np.round(daily2['High-Low']/daily2['Close-Low'])+1

daily2['Val1'] = np.where(daily2['High-Low']/daily2['Close-Low']>2, daily2['Close-Low']*daily2['Ceil'], daily2['Close-Low'])
daily2['Val2'] = np.where(daily2['Val1']>130, daily2['Val1']/3, daily2['Val1'])# changed from 'Val1']/2 to 'Val1']/3
daily2['Val3'] = np.round(daily2['High']/daily2['Low']*daily2['Close'])
daily2['BuyP'] = np.round(1.1*daily2['Val2']/4+daily2['Close'])
daily2['BuyT'] = np.round((daily2['BuyP']+daily2['Val3'])/2)
daily2['BuySL'] = np.round(daily2['Close']-(1.1*daily2['High-Low']/4))  #=F157-(1.1*R157/4)-Y157
daily2['SellP']= np.round(daily2['Close']-(1.1*daily2['Val2']/4)) #=F157-(1.1*O157/4)+Y157
daily2['SellT']= np.round(daily2['Close']-(1.1*daily2['Val2']/math.sqrt(2))) #=F157-(1.1*O157/SQRT(2))+Z157
daily2['SellSL']= np.round(daily2['Close']+(1.1*daily2['High-Low']/4)) #=F157+(1.1*R157/4)+Y157
daily2['H7'] = np.round(1.35*(daily2['High']-daily2['Low'])+daily2['Close']) #=1.35*(High-Low)+Close
daily2['H6'] = np.round(1.09*(daily2['High']-daily2['Low'])+daily2['Close']) #=1.35*(High-Low)+Close
daily2['H5'] = np.round(0.82*(daily2['High']-daily2['Low'])+daily2['Close']) #=1.35*(High-Low)+Close
daily2['H4'] = np.round(0.55*(daily2['High']-daily2['Low'])+daily2['Close']) #=1.35*(High-Low)+Close
daily2['H3'] = np.round(0.275*(daily2['High']-daily2['Low'])+daily2['Close']) #=1.35*(High-Low)+Close
daily2['H2'] = np.round(0.183*(daily2['High']-daily2['Low'])+daily2['Close']) #=1.35*(High-Low)+Close
daily2['H1'] = np.round(0.0916*(daily2['High']-daily2['Low'])+daily2['Close']) #=1.35*(High-Low)+Close
daily2['L1'] = np.round(daily2['Close']-0.0916*(daily2['High']-daily2['Low'])) #=1.35*(High-Low)+Close
daily2['L2'] = np.round(daily2['Close']-0.183*(daily2['High']-daily2['Low'])) #=1.35*(High-Low)+Close
daily2['L3'] = np.round(daily2['Close']-0.275*(daily2['High']-daily2['Low'])) #=1.35*(High-Low)+Close
daily2['L4'] = np.round(daily2['Close']-0.55*(daily2['High']-daily2['Low'])) #=1.35*(High-Low)+Close
daily2['L5'] = np.round(daily2['Close']-0.82*(daily2['High']-daily2['Low'])) #=1.35*(High-Low)+Close
daily2['L6'] = np.round(daily2['Close']-1.09*(daily2['High']-daily2['Low'])) #=1.35*(High-Low)+Close
daily2['L7'] = np.round(daily2['Close']-1.35*(daily2['High']-daily2['Low'])) #=1.35*(High-Low)+Close
i=1
while(i<len(daily2)-1):
    #i=137
    Copen=daily2.iloc[i-1]['Open']
    if Copen<daily2.iloc[i]['H3'] and Copen>daily2.iloc[i]['L3']:
        daily2['BuyP'][i-1]= daily2.iloc[i]['L3']
        daily2['BuyT'][i-1]= daily2.iloc[i]['H1']
        #daily2['BuySL'][i-1]= (daily2.iloc[i]['L4']+daily2.iloc[i]['L4'])/2#daily2.iloc[i]['L4']        
        daily2['BuySL'][i-1]= daily2.iloc[i]['L4']
        daily2['SellP'][i-1]= daily2.iloc[i]['H3']
        daily2['SellT'][i-1]= daily2.iloc[i]['L1']
        #daily2['SellSL'][i-1]= (daily2.iloc[i]['H4']+daily2.iloc[i]['H3'])/2#daily2.iloc[i]['H4']
        daily2['SellSL'][i-1]= daily2.iloc[i]['H4']
        print("First")
    elif Copen<daily2.iloc[i]['H3'] and Copen>daily2.iloc[i]['H4']:
        daily2['BuyP'][i-1]= daily2.iloc[i]['H4']
        daily2['BuyT'][i-1]= daily2.iloc[i]['H5']
        #daily2['BuySL'][i-1]= (daily2.iloc[i]['H3']+daily2.iloc[i]['H4'])/2#daily2.iloc[i]['H3']
        daily2['BuySL'][i-1]= daily2.iloc[i]['H3']
        daily2['SellP'][i-1]= daily2.iloc[i]['H3']
        daily2['SellT'][i-1]= daily2.iloc[i]['L1']
        #daily2['SellSL'][i-1]= (daily2.iloc[i]['H4']+daily2.iloc[i]['H3'])/2#daily2.iloc[i]['H4']
        daily2['SellSL'][i-1]= daily2.iloc[i]['H4']
        print("Second")
    elif Copen<daily2.iloc[i]['L3'] and Copen>daily2.iloc[i]['L4']:
        daily2['BuyP'][i-1]= daily2.iloc[i]['L3']
        daily2['BuyT'][i-1]= daily2.iloc[i]['H1']
        daily2['BuySL'][i-1]= daily2.iloc[i]['L4']
        #daily2['BuySL'][i-1]= (daily2.iloc[i]['L4']+daily2.iloc[i]['L3'])/2#daily2.iloc[i]['L4']
        daily2['SellP'][i-1]= daily2.iloc[i]['L4']
        daily2['SellT'][i-1]= daily2.iloc[i]['L5']
        daily2['SellSL'][i-1]= daily2.iloc[i]['L3']
        #daily2['SellSL'][i-1]= (daily2.iloc[i]['L3']+daily2.iloc[i]['L4'])/2#daily2.iloc[i]['L3']
        print("Third")
    elif Copen>daily2.iloc[i]['H4']:
        daily2['BuyP'][i-1]= daily2.iloc[i]['H4']
        daily2['BuyT'][i-1]= daily2.iloc[i]['H5']
        daily2['BuySL'][i-1]= daily2.iloc[i]['H3']
        #daily2['BuySL'][i-1]= (daily2.iloc[i]['H3']+daily2.iloc[i]['H4'])/2#aily2.iloc[i]['H3']
        daily2['SellP'][i-1]= daily2.iloc[i]['H3']
        daily2['SellT'][i-1]= daily2.iloc[i]['L1']
        daily2['SellSL'][i-1]=daily2.iloc[i]['H4']
        #daily2['SellSL'][i-1]= (daily2.iloc[i]['H4']+daily2.iloc[i]['H3'])/2#daily2.iloc[i]['H4']
        print("fourth")
    elif Copen<daily2.iloc[i]['L4']:
        daily2['BuyP'][i-1]= daily2.iloc[i]['L3']
        daily2['BuyT'][i-1]= daily2.iloc[i]['H1']
        daily2['BuySL'][i-1]= daily2.iloc[i]['L4']
        #daily2['BuySL'][i-1]= (daily2.iloc[i]['L4']+daily2.iloc[i]['L3'])/2#daily2.iloc[i]['L4']
        daily2['SellP'][i-1]= daily2.iloc[i]['L4']
        daily2['SellT'][i-1]= daily2.iloc[i]['L5']
        daily2['SellSL'][i-1]= daily2.iloc[i]['L4']
        #daily2['SellSL'][i-1]= (daily2.iloc[i]['L3']+daily2.iloc[i]['L4'])/2#daily2.iloc[i]['L4']
        print("fifth")
    else:
        daily2['BuyP'][i-1]= 0
        daily2['BuyT'][i-1]= 0
        daily2['BuySL'][i-1]= 0
        daily2['SellP'][i-1]= 0
        daily2['SellT'][i-1]= 0
        daily2['SellSL'][i-1]= 0 
        print("sixth")
    i=i+1
    print(i)         



#daily=daily1

data = pd.read_csv('C:\ReadMoneycontrol\Crude\CrudeOil.csv')
List_ = list(data['Date/Time'])
#List_ = [parse(x).strftime for x in List_]
List_ = [datetime.datetime.strptime(parse(x).strftime("%m/%d/%Y %I:%M %p"), "%m/%d/%Y %I:%M %p") for x in List_]
data['Date/Time']=pd.Series([x for x in List_],index=data.index)
data['starttime_date'] = pd.Series([x.date() for x in List_],index=data.index)
data['starttime_year'] = pd.Series([x.year for x in List_],index=data.index)
data['starttime_month'] = pd.Series([x.month for x in List_],index=data.index)
data['starttime_day'] = pd.Series([x.day for x in List_],index=data.index)
data['starttime_hour'] = pd.Series([x.hour for x in List_],index=data.index)

#tdaily['BuyTime']=DefaultDate
#tdaily['BuyTime'][0]=DefaultDate
#tdaily.is_copy

DateIndex=26
daily=daily1
stg1=dataTemplate()

i=0
while(i<len(stg1)):
    print(i)
    DateIndex=i
    stg1=run(stg1)
    i=i+1

daily=daily0
stg0=dataTemplate()

i=0
while(i<len(stg0)):
    print(i)
    DateIndex=i
    stg0=run(stg0)
    i=i+1


stg10=dataTemplate1()

i=0
while(i<len(stg10)):
    print(i)
    DateIndex=i
    stg10=run(stg10)
    i=i+1
    

daily=daily2
stg100=dataTemplate()

i=0
while(i<len(stg100)):
    print(i)
    DateIndex=i
    stg100=run(stg100)
    i=i+1
printme(stg100)

#Fib Strategy
i=139
daily=daily2
stg100=dataTemplate()
stg100.iloc[i]
#stg100['High'][i]=3420
#stg100['Low'][i]=3275
fUpper=fibupper(stg100['High'][i]-stg100['Low'][i],stg100['Low'][i])
fLower=fiblower(stg100['High'][i]-stg100['Low'][i],stg100['Low'][i])
fUpper[318]
FibSeries=[-1786,-1618,-1500,-1382,-1236,-1000,-786,-618,-500,-382,-236,1,236,382,500,618,786,1000,1236,1382,1500,1618,1786]
FibLevels=[]
SpecificDate=data[ (data['Date/Time']>stg100.iloc[i-1]['Date']) & (data['Date/Time']<stg100.iloc[i-2]['Date'])]
SpecificDate.iloc[0]['Open']
j=14
FibFoundAxis=[]
j=0
SameOpen=SpecificDate.groupby(['Open'])['Open'].count().reset_index(name='count').sort_values(['count'], ascending=False)
SameHigh=SpecificDate.groupby(['High'])['High'].count().reset_index(name='count').sort_values(['count'], ascending=False)

while(j<len(FibSeries)):    
    #print(str(FibSeries[j])+"\t:"+str(round(fUpper[FibSeries[j]])))
    FibLevels.append(round(fUpper[FibSeries[j]]))
    #j=j+1
    #236,382,500,618,786,1000
    Tollerance=2
    CheckmLow=SpecificDate[(SpecificDate['Low']>=round(fUpper[FibSeries[j]])-Tollerance) & (SpecificDate['Low']<=round(fUpper[FibSeries[j]])+Tollerance)]    
    if(len(CheckmLow)>0):
        print(str(FibSeries[j])+"\t:Found Low at   : "+str(CheckmLow.iloc[0]['Date/Time'])+" \t:"+str(round(fUpper[FibSeries[j]])))
        FibFoundAxis.append(round(fUpper[FibSeries[j]]))
    CheckmClose=SpecificDate[(SpecificDate['Close']>=round(fUpper[FibSeries[j]])-Tollerance) & (SpecificDate['Close']<=round(fUpper[FibSeries[j]])+Tollerance)]    
    if(len(CheckmClose)>0):
        print(str(FibSeries[j])+"\t:Found Close at   : "+str(CheckmClose.iloc[0]['Date/Time'])+"\t:"+str(round(fUpper[FibSeries[j]])))
    CheckmOpen=SpecificDate[(SpecificDate['Open']>=round(fUpper[FibSeries[j]])-Tollerance) & (SpecificDate['Open']<=round(fUpper[FibSeries[j]])+Tollerance)]    
    if(len(CheckmOpen)>0):
        print(str(FibSeries[j])+"\t:Found Open at   : "+str(CheckmOpen.iloc[0]['Date/Time'])+"\t:"+str(round(fUpper[FibSeries[j]])))
    CheckmHigh=SpecificDate[(SpecificDate['High']>=round(fUpper[FibSeries[j]])-Tollerance) & (SpecificDate['High']<=round(fUpper[FibSeries[j]])+Tollerance)]    
    if(len(CheckmClose)>0):
        print(str(FibSeries[j])+"\t:Found High at   : "+str(CheckmClose.iloc[0]['Date/Time'])+"\t:"+str(round(fUpper[FibSeries[j]])))
    
    j=j+1

iFib=0
FirstTime=True
while(iFib<len(FibFoundAxis)):
    TempOpenDF=SameOpen[(SameOpen['Open']==FibFoundAxis[iFib]) & (SameOpen['count']>2)]
    TempHighDF=SameHigh[(SameHigh['High']==FibFoundAxis[iFib]) & (SameOpen['count']>2)]
    Entered=False
    if(len(TempOpenDF)>0):
        TempOpenDateDF=SpecificDate[SpecificDate['Open']==TempOpenDF.iloc[0]['Open']]['Date/Time'].reset_index(name='Date')
        Entered=True
    if(len(TempHighDF)>0):
        TempHighDateDF=SpecificDate[SpecificDate['High']==TempHighDF.iloc[0]['High']]['Date/Time'].reset_index(name='Date')
        Entered=True
    if(len(TempOpenDateDF)>0 and len(TempHighDateDF)>0 and Entered):
        TempMergeDF=TempOpenDateDF.append(TempHighDateDF)
        TempMergeDF['Count']=pd.Series(0,index=TempMergeDF.index)
        TempMergeDF['Group']=pd.Series(iFib,index=TempMergeDF.index)
        TempMergeDF['FibValue']=pd.Series(FibFoundAxis[iFib],index=TempMergeDF.index)
        TempMergeDF=TempMergeDF.sort_values(by='Date')
        TempMergeDF=TempMergeDF.reset_index()
        if(len(TempMergeDF)>0):
            DateLoop=0
            while(DateLoop<len(TempMergeDF)):
                FirstDate=TempMergeDF.iloc[DateLoop]['Date']
                CalculatedDate=FirstDate-datetime.timedelta(minutes=8)
                iDateSeries=pd.date_range(CalculatedDate, periods=9, freq='60S')
                DateSeriesLoop=0
                while(DateSeriesLoop<len(iDateSeries)):
                    ComparisonResult=TempMergeDF[TempMergeDF['Date']==iDateSeries[DateSeriesLoop]]
                    if(len(ComparisonResult)>0):
                        TempMergeDF['Count'][DateLoop]=TempMergeDF.iloc[DateLoop]['Count']+len(ComparisonResult)
                        #TempMergeDF['Group'][DateLoop]=
                    DateSeriesLoop=DateSeriesLoop+1                    
                DateLoop=DateLoop+1
            if FirstTime:   
                TempFilteredMergeDF=TempMergeDF[TempMergeDF['Count']>5]
                FirstTime=False
            else:
                TempFilteredMergeDF=TempFilteredMergeDF.append(TempMergeDF[TempMergeDF['Count']>5])
            #=SpecificDate.groupby(['Open'])['Open'].count().reset_index(name='count').sort_values(['count'], ascending=False)
            
    #pd.date_range(TempOpenDateDF.iloc[0]['Date'], periods=5, freq='60S')
    #-datetime.timedelta(minutes=10)    
    iFib=iFib+1
#dates = matplotlib.dates.date2num(SpecificDate['Date/Time'])
#matplotlib.pyplot.plot_date(dates, SpecificDate['Open'])
    
TempFilteredMergeDF.groupby(['Group','Count','Date'])['Group'].count().reset_index(name='count').sort_values(['Date'], ascending=False)
#for ji in TempFilteredMergeDF.groupBy
TempFilteredMergeDF.sort_values(by='Count')
plt.figure()
plt.plot(SpecificDate['Date/Time'],SpecificDate['Open'])
# beautify the x-labels
plt.gcf().autofmt_xdate()
k=0
while(k<len(FibFoundAxis)):
    plt.axhline(FibFoundAxis[k], color='r', linewidth=1)
    k=k+1
plt.savefig('C:/ReadMoneycontrol/Crude/filename'+str(i)+'.png', dpi=300)
plt.show()
    
plt.figure()
plt.plot(SpecificDate['Date/Time'],SpecificDate['High'])
# beautify the x-labels
plt.gcf().autofmt_xdate()
k=0
while(k<len(FibFoundAxis)):
    plt.axhline(FibFoundAxis[k], color='r', linewidth=1)
    k=k+1
plt.show()    
plt.savefig('C:/ReadMoneycontrol/Crude/filename'+str(i)+'.png', dpi=300)
plt.show()

#
#run()
#tdaily.iloc[DateIndex]
tdaily.to_csv('C:/ReadMoneycontrol/Crude/testresults1.csv',sep=',',encoding='utf-8')
SpecificDate.to_csv('C:/ReadMoneycontrol/Crude/SpecificDate1.csv',sep=',',encoding='utf-8')
stg100.to_csv('C:/ReadMoneycontrol/Crude/testresults2.csv',sep=',',encoding='utf-8')
TempFilteredMergeDF.to_csv('C:/ReadMoneycontrol/Crude/TempFilteredMergeDF1.csv',sep=',',encoding='utf-8')
tdaily[['BuyHit','SellHit']]
  

    stg1['BuyHit'].sum()
    stg1['SellHit'].sum()

     str(stg10['BuyHit'].sum()) + "= " + str(stg10['SellHit'].sum()) + "= " + str(stg10['BuyHit'].sum() + stg10['SellHit'].sum())
     
     str(stg1['BuyHit'].sum()) + "= " + str(stg1['SellHit'].sum()) + "= " + str(stg1['BuyHit'].sum() + stg1['SellHit'].sum())
    
def printme(vstg):
    print(str(vstg['BuyHit'].sum()) + "= " + str(vstg['SellHit'].sum()) + "= " + str(vstg['BuyHit'].sum() + vstg['SellHit'].sum()))
    return True
    

def dataTemplate():
    DefaultDate=datetime.datetime.now()
    tdaily=daily[['Date','Symbol','Open','High','Low','Close','BuyP','BuyT','BuySL','SellP','SellT','SellSL']]
#pd.options.mode.chained_assignment = "warn"
#List1_ = list(daily['Date'])
#tdaily = tdaily.copy()
    tdaily['BuyTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['BuyTargetTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['BuyStopLossTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['SellTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['SellTargetTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['SellStopLossTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['LastPrice']=pd.Series(None,index=tdaily.index)
    tdaily['BuyHit']=pd.Series(0,index=tdaily.index)
    tdaily['SellHit']=pd.Series(0,index=tdaily.index)
    return tdaily

def dataTemplate1():
    DefaultDate=datetime.datetime.now()
    tdaily=daily1[['Date','Symbol','Open','High','Low','Close','BuyP','BuyT','BuySL']]
    tdaily=tdaily.join(daily0[['SellP','SellT','SellSL']])
#pd.options.mode.chained_assignment = "warn"
#List1_ = list(daily['Date'])
#tdaily = tdaily.copy()
    tdaily['BuyTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['BuyTargetTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['BuyStopLossTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['SellTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['SellTargetTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['SellStopLossTime']=pd.Series(DefaultDate,index=tdaily.index)
    tdaily['LastPrice']=pd.Series(None,index=tdaily.index)
    tdaily['BuyHit']=pd.Series(0,index=tdaily.index)
    tdaily['SellHit']=pd.Series(0,index=tdaily.index)
    return tdaily
    
def run(tdaily):
#if True:
    daily.iloc[DateIndex]['Date']
    SpecificDate=data[ (data['Date/Time']>daily.iloc[DateIndex-1]['Date']) & (data['Date/Time']<daily.iloc[DateIndex-2]['Date'])]
    
    #(data['Date/Time']>daily.iloc[100]['Date'] and
    data.set_index('Date/Time')
    SpecificDate['Date/Time']
    
    #groupby_birthyear_gender = data.groupby(['birthyear', 'gender'])['birthyear']
    
    BuyP=daily.iloc[DateIndex]['BuyP']
    BuyT=daily.iloc[DateIndex]['BuyT']
    BuySL=daily.iloc[DateIndex]['BuySL']
    
    SellP=daily.iloc[DateIndex]['SellP']
    SellT=daily.iloc[DateIndex]['SellT']
    SellSL=daily.iloc[DateIndex]['SellSL']
    #data=data1
    #data.loc[SpecificDate]['Date/Time']
    Tollerance=3
    BuyPT=SpecificDate[(SpecificDate['High']>=BuyP-Tollerance) & (SpecificDate['High']<=BuyP+Tollerance)]
    BuyTT=SpecificDate[(SpecificDate['High']>=BuyT-Tollerance) & (SpecificDate['High']<=BuyT+Tollerance)]
    BuySLT=SpecificDate[(SpecificDate['High']>=BuySL-Tollerance) & (SpecificDate['High']<=BuySL+Tollerance)]
    
    SellPT=SpecificDate[(SpecificDate['High']>=SellP-Tollerance) & (SpecificDate['High']<=SellP+Tollerance)]
    SellTT=SpecificDate[(SpecificDate['High']>=SellT-Tollerance) & (SpecificDate['High']<=SellT+Tollerance)]
    SellSLT=SpecificDate[(SpecificDate['High']>=SellSL-Tollerance) & (SpecificDate['High']<=SellSL+Tollerance)]
    
    BuyHit=False
    SellHit=False
    #if len(BuyPT)>0:
    #    print("Buy Price At : " + str(BuyPT.iloc[0]['Date/Time']))
    #    if len(BuyTT)>0:
    #        print("Buy Target At : "+ str(BuyTT.iloc[0]['Date/Time']))
    #        print("Total Profit :" + str(BuyT-BuyP))
    #    if len(BuySLT)>0:
    #        print("Buy Stop loss At : " + str(BuySLT.iloc[0]['Date/Time']))
    #        print("Total Loss:" + str(BuySL-BuyP))
    
    
    isBuyProcess=True
    isSellProcess=True
    if( len(BuyPT)>0 and len(SellPT)>0):
        isBuyProcess=(BuyPT.iloc[0]['Date/Time']<SellPT.iloc[0]['Date/Time'])
        isSellProcess=(BuyPT.iloc[0]['Date/Time']>SellPT.iloc[0]['Date/Time'])
   
    if(len(BuyPT)>0):
        tdaily['BuyTime'][DateIndex]=BuyPT.iloc[0]['Date/Time']
    if(len(BuyTT)>0):
        tdaily['BuyTargetTime'][DateIndex]=BuyTT.iloc[0]['Date/Time']
    if(len(BuySLT)>0):
        tdaily['BuyStopLossTime'][DateIndex]=BuySLT.iloc[0]['Date/Time']    
    if(len(SellPT)>0):
        tdaily['SellTime'][DateIndex]=SellPT.iloc[0]['Date/Time']
    if(len(SellTT)>0):
        tdaily['SellTargetTime'][DateIndex]=SellTT.iloc[0]['Date/Time']
    if(len(SellSLT)>0):
        tdaily['SellStopLossTime'][DateIndex]=SellSLT.iloc[0]['Date/Time']    
            
        
    if (len(BuyPT)>0 and isBuyProcess):
        print("Buy Price at : " + str(BuyPT.iloc[0]['Date/Time']))
        tdaily['BuyTime'][DateIndex]=BuyPT.iloc[0]['Date/Time']
        if len(BuyTT)>0:
            print("Buy Target at : " + str(BuyTT.iloc[0]['Date/Time']))
            tdaily['BuyTargetTime'][DateIndex]=BuyTT.iloc[0]['Date/Time']
            if len(BuySLT)<=0:
                if(BuyPT.iloc[0]['Date/Time']<BuyTT.iloc[0]['Date/Time']):
                    print("Buy Total Profit :" + str(BuyT-BuyP))
                    tdaily['BuyHit'][DateIndex]=BuyT-BuyP
                else:
                    print("Total Value : "+ str(SpecificDate.iloc[len(SpecificDate)-30]['Open']-BuyP))
                    tdaily['BuyHit'][DateIndex]=SpecificDate.iloc[len(SpecificDate)-30]['Open']-BuyP
            else:
                if(BuyPT.iloc[0]['Date/Time']<BuyTT.iloc[0]['Date/Time']) and (BuyTT.iloc[0]['Date/Time']<BuySLT.iloc[0]['Date/Time']):
                    print("Buy Total Profit :" + str(BuyT-BuyP))
                    tdaily['BuyHit'][DateIndex]=BuyT-BuyP
                else:
                    print("Buy Stop Losst at : "+str(BuySLT.iloc[0]['Date/Time']))
                    tdaily['BuyStopLossTime'][DateIndex]=BuySLT.iloc[0]['Date/Time']
                    if((BuyPT.iloc[0]['Date/Time']<BuyTT.iloc[0]['Date/Time']) and (BuySLT.iloc[0]['Date/Time']<BuyTT.iloc[0]['Date/Time'])):
                        print("Buy Total Profit :" + str(BuyT-BuyP))
                        tdaily['BuyHit'][DateIndex]=BuyT-BuyP
                    else:
                        print("Buy Total loss :" + str(BuySL-BuyP))
                        tdaily['BuyHit'][DateIndex]=BuySL-BuyP
            
        elif (len(BuySLT)>0):
            print("Buy Stop Loss at : " + str(BuySLT.iloc[0]['Date/Time']))
            tdaily['BuyStopLossTime'][DateIndex]=BuySLT.iloc[0]['Date/Time']
            print("Buy Total loss :" + str(BuySL-BuyP))
            tdaily['BuyHit'][DateIndex]=BuySL-BuyP
            if len(BuyTT)>0:
                if(BuySLT.iloc[0]['Date/Time']<BuyTT.iloc[0]['Date/Time']):
                    print("Buy Total loss :" + str(BuySL-BuyP))
                    tdaily['BuyHit'][DateIndex]=BuySL-BuyP
                    tdaily['BuyStopLossTime'][DateIndex]=BuySLT.iloc[0]['Date/Time']
        else:
            print("Total Value : "+ str(SpecificDate.iloc[len(SpecificDate)-30]['Open']-BuyP))
            tdaily['BuyHit'][DateIndex]=SpecificDate.iloc[len(SpecificDate)-30]['Open']-BuyP
            
    if len(SpecificDate) >0:       
        tdaily['LastPrice'][DateIndex]=SpecificDate.iloc[len(SpecificDate)-30]['Open']
    
    if (isSellProcess and len(SellPT)>0):
        print("Sell Price at : " + str(SellPT.iloc[0]['Date/Time']))
        tdaily['SellTime'][DateIndex]=SellPT.iloc[0]['Date/Time']
        if len(SellTT)>0:
            print("Sell Target at : " + str(SellTT.iloc[0]['Date/Time']))
            tdaily['SellTargetTime'][DateIndex]=SellTT.iloc[0]['Date/Time']
            if len(SellSLT)<=0:
                if(SellPT.iloc[0]['Date/Time']<SellTT.iloc[0]['Date/Time']):
                    print("Sell Total Profit :" + str(SellP-SellT))
                    tdaily['SellHit'][DateIndex]=SellP-SellT
                else:
                    print("Total Value : "+ str(SellP-SpecificDate.iloc[len(SpecificDate)-30]['Open']))
                    tdaily['SellHit'][DateIndex]=SpecificDate.iloc[len(SpecificDate)-30]['Open']-SellP
            else:                
                if(SellPT.iloc[0]['Date/Time']<SellTT.iloc[0]['Date/Time']) and (SellTT.iloc[0]['Date/Time']<SellSLT.iloc[0]['Date/Time']):
                    print("Sell Total Profit :" + str(SellP-SellT))
                    tdaily['SellHit'][DateIndex]=SellP-SellT
                else:    
                    print("Sell Stop Losst at 6: "+str(SellSLT.iloc[0]['Date/Time']))
                    tdaily['SellStopLossTime'][DateIndex]=SellSLT.iloc[0]['Date/Time']
                    if((SellPT.iloc[0]['Date/Time']<SellTT.iloc[0]['Date/Time']) & (SellSLT.iloc[0]['Date/Time']<SellTT.iloc[0]['Date/Time'])):
                        print("Sell Total Profit :-" + str(SellP-SellT))
                        tdaily['SellHit'][DateIndex]=SellP-SellT
                    else:
                        print("Sell Total loss 7:" + str(SellSL-SellP))
                        tdaily['SellHit'][DateIndex]=SellP-SellSL
            
        elif (len(SellSLT)>0):
            print("Sell Stop Loss at : " + str(SellSLT.iloc[0]['Date/Time']))
            tdaily['SellStopLossTime'][DateIndex]=SellSLT.iloc[0]['Date/Time']
            print("Sell Total loss 8:" + str(SellP-SellSL))
            tdaily['SellHit'][DateIndex]=SellP-SellSL
            if len(SellTT)>0:
                if(SellSLT.iloc[0]['Date/Time']<SellTT.iloc[0]['Date/Time']):
                    print("Sell Total loss 9:" + str(SellP-SellSL))
                    tdaily['SellHit'][DateIndex]=SellP-SellSL
        else:
            print("Total Value : "+ str(SellP-SpecificDate.iloc[len(SpecificDate)-30]['Open']))
            tdaily['SellHit'][DateIndex]=SpecificDate.iloc[len(SpecificDate)-30]['Open']-SellP
    
    return tdaily
        #print("No Target hit")


def fibupper(vdelta,Low):
    ulimit={}
    i=1
    while(i<=4000):
        ulimit[i]=mround(round(Low+(vdelta*i/1000),2))
        i=i+1
    i = -4000
    j=1
    while (i < 0):
        ulimit[i] = mround(round(Low + (vdelta * i / 1000), 2))
        i = i + 1
        j=j+1
    return ulimit

def fiblower(vdelta,Low):
    llimit={}
    i=1
    while(i<=2000):
        llimit[i]=mround(round(Low-(vdelta*i/1000),2))
        i=i+1
    return llimit

def getKey(mydict,ivalue):
    a1=list(mydict.values())
    #print("test1");
    try:
        b1=a1.index(ivalue)
    except ValueError:
        try:
            b1 = a1.index(round(ivalue-.05,2))
        except ValueError:
            try:
                b1 = a1.index(round(ivalue + .05,2))
            except ValueError:
                try:
                    b1 = a1.index(round(ivalue - .1,2))
                except ValueError:
                    try:
                        b1 = a1.index(round(ivalue + .1, 2))
                    except ValueError:
                        try:
                            b1 = a1.index(round(ivalue - .15, 2))
                        except ValueError:
                            try:
                                b1 = a1.index(round(ivalue + .15, 2))
                            except ValueError:
                                try:
                                    b1 = a1.index(round(ivalue - .2, 2))
                                except ValueError:
                                    try:
                                        b1 = a1.index(round(ivalue + .2, 2))
                                    except ValueError:
                                        try:
                                            b1 = a1.index(round(ivalue - .25, 2))
                                        except ValueError:
                                            try:
                                                b1 = a1.index(round(ivalue + .25, 2))
                                            except ValueError:
                                                try:
                                                    b1 = a1.index(round(ivalue - .3, 2))
                                                except ValueError:
                                                    try:
                                                        b1 = a1.index(round(ivalue + .3, 2))
                                                    except ValueError:
                                                        try:
                                                            b1 = a1.index(round(ivalue - .35, 2))
                                                        except ValueError:
                                                            try:
                                                                b1 = a1.index(round(ivalue + .35, 2))
                                                            except ValueError:
                                                                try:
                                                                    b1 = a1.index(round(ivalue - .4, 2))
                                                                except ValueError:
                                                                    try:
                                                                        b1 = a1.index(round(ivalue + .4, 2))
                                                                    except ValueError:
                                                                        try:
                                                                            b1 = a1.index(round(ivalue - .45, 2))
                                                                        except ValueError:
                                                                            b1 = a1.index(round(ivalue + .45, 2))
    except:
        print("Error")
    a = b1
    #print(a)
    return list(mydict.keys())[a]

def tgetKey(mydict,ivalue):
    a1=list(mydict.values()).index(round(ivalue,2))
    return a1

def mround(m):
    a=m*100
    b=a%10
    c=0
    if(b>=5 and b<=7):
        c=-1
        d=.05
    elif(b>=7):
        c=0
        d = 0
    else:
        c=0
        d=0
    return round((round(a/10)+c)/10+d,2)



# =============================================================================
# 
# SellPT['Date/Time']
# SellTT['Date/Time']
# SellSLT['Date/Time']
# 
# SpecificDate.to_csv('C:/ReadMoneycontrol/Crude/test1.csv',sep=',',encoding='utf-8')
# 
# SpecificDate.iloc[10][:5]
# SpecificDate1=(data.loc[SpecificDate]['Date/Time']<daily.iloc[101]['Date'])
# 
# SpecificDate.iloc[0][1:6]
# SpecificDate.dtypes
# SpecificDate.groupby['False']['False'].count()
# data.loc[mask]
# data.iloc[0]
# daily.iloc[100]
# odata=data
# 
# df=SpecificDate
# 
# df.Open
# 
# plt.plot(df['Date/Time'],df['Open'])
# # beautify the x-labels
# plt.gcf().autofmt_xdate()
# plt.show()
# 
# 
# #https://plot.ly/python/candlestick-charts/
# import plotly.plotly as py
# import plotly as py
# plotly.__version__
# import plotly.graph_objs as go
# trace = go.Candlestick(x=df['Date/Time'],
#                        open=df.Open,
#                        high=df.High,
#                        low=df.Low,
#                        close=df.Close)
# layout = go.Layout(
#     xaxis = dict(
#         rangeslider = dict(
#             visible = False
#         )
#     )
# )
# data1=data
# data = [trace]
# fig = dict( data=data, layout=layout )
# py.plot( fig, filename='d3-cloropleth-map' )
# fig = go.Figure(data=data,layout=layout)
# py.plot(data,filename='tutorial.html')
# py.iplot(fig, filename='simple_candlestick')
# 
# 
# Weekday = daily.groupby(['Weekday'])['Weekday'].count()
# Year=data.groupby(['starttime_year'])['starttime_year'].count()
# data.groupby(['starttime_month'])['starttime_month'].count()
# Year
# 
# Low_=list(data['Low'])
# Close_=list(data['Close'])
# High_=list(data['High'])
# Open_=list(data['Open'])
# 
# data1=data
# data['Close-Low']=np.round(data['Close']-data['Low'])
# data['High-Low']=np.round(data['High']-data['Low'])
# 
# groupby_birthyear_gender = data.groupby(['starttime_year', 'starttime_month','starttime_date'])['starttime_date'].count()
# groupby_birthyear_gender 
# groupby_birthyear_gender.plot.bar(title = 'Distribution of birth years', figsize = (15,4))
# 
# ohlc_dict = {                                                                                                             
# 'Open':'first',                                                                                                    
# 'High':'max',                                                                                                       
# 'Low':'min',                                                                                                        
# 'Close': 'last',                                                                                                    
# 'Volume': 'sum'
# }
# odata.resample('5T', how=ohlc_dict, closed='left', label='left')
# 
# data = data.sort_values(by='starttime')
# data.reset_index()
# print 'Date range of dataset: %s - %s'%(data.ix[1, 'starttime'], data.ix[len(data)-1, 'stoptime'])
# groupby_gender = data.groupby('gender').size()
# groupby_gender.plot.bar(title = 'Distribution of genders')
# 
# data = data.sort_values(by='birthyear')
# groupby_birthyear = data.groupby('birthyear').size()
# groupby_birthyear.plot.bar(title = 'Distribution of birth years', figsize = (15,4))
# 
# data_mil = data[(data['birthyear'] >= 1977) & (data['birthyear']<=1994)]
# groupby_mil = data_mil.groupby('usertype').size()
# groupby_mil.plot.bar(title = 'Distribution of user types')
# 
# groupby_birthyear_gender = data.groupby(['birthyear', 'gender'])['birthyear'].count().unstack('gender').fillna(0)
# groupby_birthyear_gender[['Male','Female','Other']].plot.bar(title = 'Distribution of birth years by Gender', stacked=True, figsize = (15,4))
# 
# groupby_birthyear_user = data.groupby(['birthyear', 'usertype'])['birthyear'].count().unstack('usertype').fillna(0)
# 
# groupby_birthyear_user['Member'].plot.bar(title = 'Distribution of birth years by Usertype', stacked=True, figsize = (15,4))
# 
# 
# data[data['usertype']=='Short-Term Pass Holder']['birthyear'].isnull().values.all()
# 
# data[data['usertype']=='Short-Term Pass Holder']['gender'].isnull().values.all()
# 
# 
# List_ = list(data['starttime'])
# 
# List_ = [datetime.datetime.strptime(x, "%m/%d/%Y %H:%M") for x in List_]
# data['starttime_mod'] = pd.Series(List_,index=data.index)
# data['starttime_date'] = pd.Series([x.date() for x in List_],index=data.index)
# data['starttime_year'] = pd.Series([x.year for x in List_],index=data.index)
# data['starttime_month'] = pd.Series([x.month for x in List_],index=data.index)
# data['starttime_day'] = pd.Series([x.day for x in List_],index=data.index)
# data['starttime_hour'] = pd.Series([x.hour for x in List_],index=data.index)
# data.groupby('starttime_date')['tripduration'].mean().plot.bar(title = 'Distribution of Trip duration by date', figsize = (15,4))
# 
# trip_duration = list(data['tripduration'])
# station_from = list(data['from_station_name'])
# print 'Mean of trip duration: %f'%statistics.mean(trip_duration)
# print 'Median of trip duration: %f'%statistics.median(trip_duration)
# print 'Mode of station originating from: %s'%statistics.mode(station_from)
# data['tripduration'].plot.hist(bins=100, title='Frequency distribution of Trip duration')
# plt.show()
# 
# q75, q25 = np.percentile(trip_duration, [75 ,25])
# iqr = q75 - q25
# print 'Proportion of values as outlier: %f percent'%(
# (len(data) - len([x for x in trip_duration if q75+(1.5*iqr) >=x>= q25-(1.5*iqr)]))*100/float(len(data)))
# 
# mean_trip_duration = np.mean([x for x in trip_duration if q75+(1.5*iqr) >=x>= q25-(1.5*iqr)])
# upper_whisker = q75+(1.5*iqr)
# print 'Mean of trip duration: %f'%mean_trip_duration
# 
# def transform_tripduration(x):
# 
#     if x > upper_whisker:
#         return mean_trip_duration
#     return x
# 
# data['tripduration_mean'] = data['tripduration'].apply(lambda x: transform_tripduration(x))
# 
# data['tripduration_mean'].plot.hist(bins=100, title='Frequency distribution of mean transformed Trip duration')
# plt.show()
# print 'Mean of trip duration: %f'%data['tripduration_mean'].mean()
# print 'Standard deviation of trip duration: %f'%data['tripduration_mean'].std()
# print 'Median of trip duration: %f'%data['tripduration_mean'].median()
# 
# data = data.dropna()
# seaborn.pairplot(data, vars=['age', 'tripduration'], kind='reg')
# plt.show()
# 
# pd.set_option('display.width', 100)
# pd.set_option('precision', 3)
# 
# data['age'] = data['starttime_year'] - data['birthyear']
# 
# correlations = data[['tripduration','age']].corr(method='pearson')
# print(correlations)
# for cat in ['gender','usertype']:
#     print 'Category: %s\n'%cat
#     groupby_category = data.groupby(['starttime_date', cat])['starttime_date'].count().unstack(cat)
#     groupby_category = groupby_category.dropna()
#     category_names = list(groupby_category.columns)
# 
#     for comb in [(category_names[i],category_names[j]) for i in range(len(category_names)) for j in range(i+1, len(category_names))]:
# 
#         print '%s %s'%(comb[0], comb[1])
#         t_statistics = stats.ttest_ind(list(groupby_category[comb[0]]), list(groupby_category[comb[1]]))
#         print 'Statistic: %f, P value: %f'%(t_statistics.statistic, t_statistics.pvalue)
#         print '\n'
#         
# daily_tickets = list(data.groupby('starttime_date').size())
# sample_tickets = []
# checkpoints = [1, 10, 100, 300, 500, 1000]
# plot_count = 1
# 
# random.shuffle(daily_tickets)
# 
# plt.figure(figsize=(15,7))
# binrange=np.array(np.linspace(0,700,101))
# 
# for i in xrange(1000):
#     if daily_tickets:
#         sample_tickets.append(daily_tickets.pop())
# 
#     if i+1 in checkpoints or not daily_tickets:
#         plt.subplot(2,3,plot_count)
#         plt.hist(sample_tickets, binrange)
#         plt.title('n=%d' % (i+1),fontsize=15)        
#         plot_count+=1
# 
#     if not daily_tickets:
#        break
# 
# plt.show()
# 
# =============================================================================
