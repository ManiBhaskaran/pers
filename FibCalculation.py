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