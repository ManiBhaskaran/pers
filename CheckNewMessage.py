import selenium.webdriver
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time 
import pandas as pd
import numpy as np
import winsound
import pyglet
import datetime
  
# Replace below path with the absolute path 
# to chromedriver in your computer 
driver = webdriver.Chrome('C:\\Users\\lalitha\\chromedriver') 
Timer=0
FirstTime=True

while(Timer<20000):    
    driver.get("http://mcx.freetips.tips/") 
    wait = WebDriverWait(driver, 800) 
    
    
    
    classname='"post-news"'
    x_arg1 = '//div[contains(@class,' + classname + ')]'
    #postdesc='"post-desc"'
    #postdescarg = '//p[contains(@class,' + postdesc + ')]'
    #datestr='"date"'
    #datearg = '//span[contains(@class,' + datestr + ')]'
    #category='"meta-cat"'
    #categoryarg = '//span[contains(@class,' + category + ')]'
    #user='"meta-user"'
    #userarg = '//span[contains(@class,' + user + ')]'
    
    
    message1 = wait.until(EC.presence_of_element_located(( 
        By.XPATH, x_arg1))) 
    messages1=driver.find_elements_by_xpath(x_arg1)
    #messages_postdesc=driver.find_elements_by_xpath(postdescarg)
    #messages_date=driver.find_elements_by_xpath(datearg)
    #messages_category=driver.find_elements_by_xpath(categoryarg)
    #messages_user=driver.find_elements_by_xpath(userarg)
    
    lDescription=[]
    lDate=[]
    lCategory=[]
    lUser=[]
    lTipsID=[]
    
    
    i=0
    index=9999
    for message in messages1:
        msgAr=message.text.split('\n')
        #print("\n"+messages_postdesc[i].text + "\n" +messages_date[i].text + "\n"+messages_category[i].text+ "\n"+messages_user[i].text)
        lDescription.insert(index,msgAr[0])
        lDate.insert(index,msgAr[3].split(' : ')[1].replace(' at','').strip())
        lTipsID.insert(index,msgAr[4].split(' : ')[1].strip())
        lCategory.insert(index,msgAr[5].split(' : ')[1].strip())
        lUser.insert(index,msgAr[6].split(' : ')[1].strip())
        i=i+1
        
    Data={'Message':lDescription,'Date':lDate,'Category':lCategory,'User':lUser,'TipsID':lTipsID}
    df1 = pd.DataFrame(Data)
    #df1.iloc[1:5]
    df1.index=df1['TipsID']
    
    
    #df1.iloc[1]
    
    if(FirstTime):
        GlobalData=df1
        NewData=GlobalData
        FirstTime=False
        #print('True');
    else:
        #print('False.......')
        MergeResult=pd.merge(GlobalData, df1, how='outer', indicator='Exist')
        NewData=MergeResult.loc[np.where(MergeResult['Exist']=='right_only')]
        GlobalData=pd.concat([GlobalData,df1]).drop_duplicates(keep='first')
    
    l=0
    print('\n\n**********   ' + str(datetime.datetime.now()) + "  ---  " + str(Timer)  + '    *******\n\n')
    firstSound=True
    while(l<len(NewData)):        
        print('\n\n**********       *******\n\n')
        print(NewData.iloc[l]['User']+'\n'+NewData.iloc[l]['Date']+'\n'+NewData.iloc[l]['Message'])
        l=l+1
        if(firstSound):
            winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
            firstSound=False
    time.sleep(30)
    Timer=Timer+1