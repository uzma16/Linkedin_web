#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd 
import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import numpy as np
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[23]:


gc = gspread.service_account(filename =r'leads-key.json')
import_data = gc.open("linkedin_leads").worksheet('Sheet1') 
export_data = gc.open("linkedin_leads").worksheet('Sheet2')


# In[24]:


driver=webdriver.Chrome()
wait = WebDriverWait(driver, 20)
driver.get("https://linkedin.com/")
wait.until(EC.presence_of_element_located((By.ID, "session_key"))).send_keys('Your email ID')
driver.find_element(By.ID, "session_password").send_keys('Your Password')
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
print("Login Successfully")


# In[25]:


#To find the selected jobs

def find_jobs (soup):   
        jobs = soup.find_all('div',{'class':'job-card-container'})
        job_role = []
        company = []
        location = []
        date = []
        for i in jobs:
            try:
                job_role.append(i.find('a',{'class': 'disabled ember-view job-card-container__link job-card-list__title'}).text.strip())
            except:
                job_role.append(np.nan)
            try:
                company.append(i.find('span',{'class':'job-card-container__primary-description'}).text.strip())
            except:
                company.append(np.nan)
            try:
                location.append(i.find('li',{'class':'job-card-container__metadata-item'}).text.strip())
            except:
                location.append(np.nan)
            try:
                date.append(i.find('time')['datetime'])
            except:
                date.append(np.nan)       
        d = {'job_role':job_role, 'company':company, 'location':location, 'date':date}
        df = pd.DataFrame(d)
        return df


# In[26]:


def slow_scroll():
    scroll_iterations = 10  # Adjust the number of scroll iterations as needed
    scroll_increment = 500  # Adjust the scroll height increment as needed
    for _ in range(scroll_iterations):
        driver.execute_script(f"window.document.getElementsByClassName('jobs-search-results-list')[0].scrollBy(0, {scroll_increment});")
        time.sleep(1)  


# In[27]:


def update_data():
    global combined_df
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    soup.prettify()
    df = find_jobs(soup)
    dff = df.fillna('N/A')
    data = dff.values.tolist()
    export_data.append_rows(data) # Insert the data into the Google Sheet


# In[28]:


def search_and_extract_data(client, combined_df):
    if client == 0: 
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "search-global-typeahead"))).click() # searching
        driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(clients[0],Keys.ENTER) #value type
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-pressed='false'][normalize-space()='Jobs']"))).click() # Filter for job
        wait.until(EC.element_to_be_clickable((By.ID, "searchFilter_timePostedRange"))).click() # Datetime Filter
        wait.until(EC.element_to_be_clickable((By.XPATH, "//section[1]//div[1]//section[1]//div[1]//div[1]//div[1]//ul[1]//li[3]//div[1]//div[1]//div[1]//div[1]//div[1]//form[1]//fieldset[1]//div[1]//ul[1]//li[3]//label[1]//p[1]//span[1]"))).click()  #Week
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[5]/div[3]/div[4]/section[1]/div[1]/section[1]/div[1]/div[1]/div[1]/ul[1]/li[3]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/fieldset[1]/div[2]/button[2]"))).click() #Submit
        slow_scroll()
        update_data()
        try:
            for i in range(2, 7): 
                page_button_xpath = f"//button[@aria-label='Page {i}']"
                wait.until(EC.element_to_be_clickable((By.XPATH, page_button_xpath))).click()
                slow_scroll()
                update_data()
        except Exception as e:
            print("Pagination error:", str(e))

    else:
        driver.find_element(By.CLASS_NAME, "jobs-search-box__keyboard-text-input").send_keys(clients[client],Keys.ENTER)
        slow_scroll()
        update_data()
        try:
            for i in range(2, 7):
                page_button_xpath = f"//button[@aria-label='Page {i}']"
                wait.until(EC.element_to_be_clickable((By.XPATH, page_button_xpath))).click()
                slow_scroll()
                update_data()
        except Exception as e:
            print("Pagination error:", str(e))
   
# Extraction of clients' names from sheet 1
clients = import_data.col_values(1)
combined_df = pd.DataFrame()

for client in range(0,len(clients)):
    combined_df = search_and_extract_data(client, combined_df)

    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "jobs-search-box__keyboard-text-input").clear() #To clear


# In[ ]:


# To close the window
driver.quit()

