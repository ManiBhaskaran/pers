# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:11:41 2019

@author: lalitha
"""

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
    return (round(a/10)+c)/10+d

'''
def fibupper(vdelta,Low):
    ulimit={}
    i=1
    while(i<=2000):
        ulimit[i]=mround(round(Low+(vdelta*i/1000),2))
        i=i+1
    return ulimit
'''
def fibupper(vdelta,Low):
    ulimit={}
    i=1
    while(i<=14000):
        ulimit[i]=mround(round(Low+(vdelta*i/1000),2))
        i=i+1
    i = -14000
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


    except :
        print("Error")
    a = b1
    #print(a)
    return list(mydict.keys())[a]






def getTolerance(Data,DataIndex,decimal,percent):
    fPH=Data.iloc[DataIndex]['High']
    fPL=Data.iloc[DataIndex]['Low']
    Range=fPH-fPL
    return round(Range*percent,decimal)

DataIndex=2
GL1=list(GoldHistoryV1.iloc[DataIndex])[6:]
GL2=list(GoldHistoryV2.iloc[DataIndex])[6:]
SL1=list(SilverHistory.iloc[DataIndex])[6:]
SL2=list(SilverHistoryV2.iloc[DataIndex])[6:]


LL1=list(LeadHistoryV1.iloc[DataIndex])[6:]
LL2=list(LeadHistoryV2.iloc[DataIndex])[6:]

GT=getTolerance(GoldHistoryV1,DataIndex,0,.01)
ST=getTolerance(SilverHistory,DataIndex,0,.03)
LT=getTolerance(LeadHistoryV1,DataIndex,2,.01)

print(GoldHistoryV1.iloc[DataIndex]['Date'])
PC=GoldHistoryV1.iloc[DataIndex]['Close']
for G1 in GL1:
    for G2 in GL2:
        if(G2-GT <= G1 <= G2+GT):
            if(abs(PC-G2)<400):
                print(str(G1) + " - " + str(G2))
print(GoldHistoryV1.iloc[DataIndex-1]['Open'])


PC=SilverHistory.iloc[DataIndex]['Close']
for G1 in SL1:
    for G2 in SL2:
        if(G1-ST <= G2 <= G1+ST):
            if(abs(PC-G2)<500):
                print(str(G1) + " - " + str(G2))
print(SilverHistory.iloc[DataIndex-1]['Open'])

PC=LeadHistoryV1.iloc[DataIndex]['Close']
for G1 in LL1:
    for G2 in LL2:
        if(G1-LT <= G2 <= G1+LT):
            if(abs(PC-G2)<5):
                print(str(G1) + " - " + str(G2))
print(LeadHistoryV1.iloc[DataIndex-1]['Open'])                

    
