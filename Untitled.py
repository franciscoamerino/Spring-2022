#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests


# In[2]:


# To read over pdf files
# !pip install PyPDF2


# In[3]:


url = 'http://forestsclearance.nic.in/Online_Status.aspx'


# In[4]:


response = requests.get(url)
data = response.text
soup = BeautifulSoup(data, 'html.parser')


# In[5]:


# To check if Allocation of fresh forest land (Form-A) is selected
# Opening url has this checked already
soup.find('input', {'id':'ctl00_ContentPlaceHolder1_RadioButtonList1_0'}).get('checked')


# In[6]:


get_ipython().system('pip install selenium')


# In[7]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = 
driver = webdriver.Firefox(PATH)


# In[35]:


# Pressing the Search Button to open table

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


soup.find('input', {'id': 'ctl00_ContentPlaceHolder1_Button1'})


# In[164]:


## Scrape Form-A Part - I

part_i_url = 'http://forestsclearance.nic.in/viewreport.aspx?pid=FP/AN/Others/147080/2021'
def scrape_form_a_pi(url):
    # a function that returns a dictionary
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    
    bullet_points = soup.find_all('span', {'class': ['lifont','li1','li2', 'lisub2']})
    
    pi_dict = {} # will be inner function, make dict nonlocal or global in future
    
    for i in bullet_points:
        if i.get('class')[0] == 'lifont':
            font = i.contents[0]
            if font == 'Details of land required for the Project  ':
                print('stop')
                break
        elif i.get('class')[0] == 'li1':
            head = font + ':' + i.contents[0]
    #         print(head)
        else:
            if i.get('class')[0] == 'li2':
                subhead = head +':'+ i.b.text
                #Note: add function for hrefs               
                pi_dict[subhead] = i.contents[1]
    #             print(subhead)
            else:
                subsubhead = subhead + ':' + i.b.text
                pi_dict[subhead] = i.contents[1]
    #             print(subsubhead)
    
    
    return pi_dict


# In[166]:


## Scrape Form-A Part - II


# In[179]:


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




