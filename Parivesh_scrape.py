#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# In[3]:


url = 'http://forestsclearance.nic.in/Online_Status.aspx'


# In[4]:


# response = requests.get(url)
# data = response.text
# soup = BeautifulSoup(data, 'html.parser')


# In[4]:


# To check if Allocation of fresh forest land (Form-A) is selected
# Opening url has this checked already
# soup.find('input', {'id':'ctl00_ContentPlaceHolder1_RadioButtonList1_0'}).get('checked')


# In[44]:


# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

PATH = "geckodriver.exe"
driver = webdriver.Firefox(executable_path = PATH)

try:
    driver.get(url)
    # driver.find_element_by_id('ctl00_ContentPlaceHolder1_Button1').click()

#     driver.find_element(by = By.ID, value= 'ctl00_ContentPlaceHolder1_Button1' ).click()
    element = WebDriverWait(driver,30).until(
        EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Button1' )))
    # WebDriverWait(driver, 15)
#     element = WebDriverWait(driver, 25).until(
#     EC.presence_of_element_located((By.LINK_TEXT, 'click on for Viewing Report of PartI ')) )
    element.click()
    time.sleep(15)
    for i in range(2,100):
        element = WebDriverWait(driver,30).until(
            EC.presence_of_element_located((By.LINK_TEXT, '{}'.format(i))))
        element.click()
        time.sleep(30)
        
        if i // 10 == 0:
            element = WebDriverWait(driver,30).until(
                EC.presence_of_element_located((By.LINK_TEXT, '...')))
            element.click()
            time.sleep(15)
#         driver.find_element(by=By.LINK_TEXT, value ='{}'.format(i)).click()
finally:
    page_no = driver.find_elements(by=By.LINK_TEXT, value='2')
    driver.quit()

page_no


# In[22]:


for i in page_no:
    print(i.get_attribute('outerHTML'))


# In[11]:


PATH = "geckodriver.exe"
driver = webdriver.Firefox(executable_path = PATH)

part_I = []

try:
    driver.get(url)
    # driver.find_element_by_id('ctl00_ContentPlaceHolder1_Button1').click()

#     driver.find_element(by = By.ID, value= 'ctl00_ContentPlaceHolder1_Button1' ).click()
    element = WebDriverWait(driver,30).until(
        EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Button1' )))
    # WebDriverWait(driver, 15)
#     element = WebDriverWait(driver, 25).until(
#     EC.presence_of_element_located((By.LINK_TEXT, 'click on for Viewing Report of PartI ')) )
    element.click()
    time.sleep(15)
finally:    
    a_tags = driver.find_elements(by= By.TAG_NAME, value ='a')
    # for a in a_tags:
    #     print(a)
    for a in a_tags:
        if a.get_attribute('target') and 'Part I ' in a.get_attribute('title'):
#             print(a.get_attribute('outerHTML'))
            print(a.get_attribute('title'))

#         if a.get_attribute('href'):
            part_I.append(a.get_attribute('href'))
        #         print(a.get_attribute('outerHTML'))
        #         if a.get('target') == '_blank':
        #             print(a.get_attribute('outerHTML'))
    driver.quit()


# In[17]:


rows = []

for i in part_I:
    rows.append(scrape_form_a_pi(i))

rows


# In[50]:


import csv

csv_columns = list(rows[1].keys())
dict_data = rows

csv_file = 'parivesh_formA_parti.csv'
try:
    with open(csv_file,'w', encoding = 'utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
except IOError:
    print("I/O error")


# In[35]:


# Pressing the Search Button to open table

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


soup.find('input', {'id': 'ctl00_ContentPlaceHolder1_Button1'})


# In[59]:


## Scrape Form-A Part - I

part_i_url = 'http://forestsclearance.nic.in/viewreport.aspx?pid=FP/AN/Others/147080/2021'
def scrape_form_a_pi(url):
    # a function that returns a dictionary
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    
    bullet_points = soup.find_all('span', {'class': ['lifont','li1','li2', 'lisub2']})
    
    pi_dict = {} # will be inner function, make dict nonlocal or global in future
    
    section = 'A'
    lifont_active = True
    li1_active = True
    li2_active = True
    lisub2_active = False
    
    for i in bullet_points:
        if i.get('class')[0] == 'lifont' and lifont_active:
            font = i.contents[0]
            if font == 'Details of land required for the Project  ':
                li2_active = False
                lisub2_active = True
            elif font == 'Maps of forest land proposed to be diverted  ':
                li1_active = False
                li2_active = True
                lisub2_active = True
                print(font)
            else:
                li1_active = False
                li2_active = True
                lisub2_active = True
#             print(font)
        elif i.get('class')[0] == 'li1' and li1_active:
            head = font + ':' + i.contents[0]
    #         print(head)
        else:
            if i.get('class')[0] == 'li2' and li2_active:
                if li1_active:
                    subhead = head +':'+ i.b.text
                else:
                    subhead = font + ':' + i.b.text
                 #Note: add function for hrefs               
                pi_dict[subhead] = i.contents[1]
    #             print(subhead)
            elif i.get('class')[0] == 'lisub2' and lisub2_active:
    #             print(i.b.text)
                if not li2_active:
                    sub2head = font + ':' + i.b.text
                else:
                    sub2head = subhead + ':' + i.b.text
                pi_dict[sub2head] = i.contents[1]
    #             print(subsubhead)
    
    return pi_dict, bullet_points


# In[60]:


pi_dict, bulletpoints = scrape_form_a_pi(part_i_url)
print('------')
for bp in bulletpoints:
    print(bp.text)


# In[61]:


pi_dict


# In[75]:


## Scrape Form-A Part - II

part_ii_url = 'http://forestsclearance.nic.in/PartIIReport_A.aspx?pid=FP/AP/IRRIG/150316/2021'

def scrape_form_a_pii(url):
    # a function that returns a dictionary
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    
    bullet_points = soup.find_all('span', {'class': ['li3','f','li2']})
    
    for i in bullet_points:
        print(i.text)
    
    pi_dict = {} # will be inner function, make dict nonlocal or global in future
    
    for i in bullet_points:
        if i.get('class')[0] == 'li3':
            li3 = i.contents[0]
#             if i.contents[1]:
#                 pi_dict[li3] = i.contents[1]
#             print(li3)
        else:
            if i.get('class')[0] == 'li2':
                li2 = li3 +':'+ i.b.text               
                pi_dict[li2] = i.contents[1]
                print(li2)
    
    return pi_dict

scrape_form_a_pii(part_ii_url)


# In[73]:


## Scrape Form-A TimeLine Details

timeline_details_url = 'http://forestsclearance.nic.in/timeline.aspx?pid=FP/AP/ROAD/34554/2018'

def scrape_form_a_tl_details(url):
    # a function that returns a dictionary
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    
    bullet_points = soup.find_all('span', {'class': ['lifont','li2']})
    
    tl_d_dict = {}
    
    for i in bullet_points:
        if i.get('class')[0] == 'lifont':
            font = i.contents[0]
            if font == 'Time Line ':
                print('stop')
                break
#         elif i.get('class')[0] == 'li1':
#             head = font + ':' + i.contents[0]
#     #         print(head)
        else:
            if i.get('class')[0] == 'li2':
                subhead = font +':'+ i.b.text
                #Note: add function for hrefs               
                tl_d_dict[subhead] = i.contents[1]
                print(subhead)
                print(i.contents[1])
            else:
                subsubhead = subhead + ':' + i.b.text
                tl_d_dict[subhead] = i.contents[1]
    #             print(subsubhead)

    return tl_d_dict

scrape_form_a_tl_details(timeline_details_url)


# In[158]:


bp.contents[1]


# In[ ]:




