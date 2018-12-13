# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 21:32:55 2018

@author: X119285
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# create a new Firefox session
driver = webdriver.Chrome("D:\X119285\Python\chromedriver.exe")
driver.implicitly_wait(30)
driver.maximize_window()

# Navigate to the application home page
driver.get("http://mcx.freetips.tips/")

# get the search textbox
search_field = driver.find_element_by_id("lst-ib")
search_field.clear()

# enter search keyword and submit
search_field.send_keys("Selenium WebDriver Interview questions")
search_field.submit()

# get the list of elements which are displayed after the search
# currently on result page using find_elements_by_class_name method
lists= driver.find_elements_by_class_name("post-news")
Title=lists[1].find_elements_by_class_name("post_title")[0].text
Description=lists[1].find_elements_by_class_name("post-desc")[0].text
Date=lists[1].find_elements_by_class_name("date")[0].text
MetaCategory=lists[1].find_elements_by_class_name("meta-cat")[0].text
User=lists[1].find_elements_by_class_name("meta-user")[0].text

# get the number of elements found
print ("Found " + str(len(lists)) + " searches:")

# iterate through each element and print the text that is
# name of the search

i=0
for listitem in lists:
   print (listitem.get_attribute("innerHTML"))
   i=i+1
   if(i>10):
      break

# close the browser window
driver.quit()
