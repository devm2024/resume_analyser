import time
from selenium import webdriver
from ratelimiter import RateLimiter
from login import login
import numpy as np
import pandas as pd
from tqdm import tqdm
from tqdm._tqdm_notebook import tqdm_notebook


def get_num_pages(jt,rb,start=0):
    # Gets the counts of links in a page.
    url = f"https://www.indeed.com/resumes?q={jt}&l=CA&co=US&lmd=all&rb={rb}&start=50"
    driver.get(url)
    result_cnt = driver.find_element_by_id('result_count')
    if result_cnt.text != '':
        result_cnt = int(result_cnt.text.split(' ')[0].replace(',',''))
        pagenum = np.array(range(round(result_cnt/50)))*50
        return pagenum[(pagenum >=start) & (pagenum <5000)]
    else:
        print(jt)
        return None

def indeedlogin():
    # To sign in to indeed using your email id and password
    driver.get('https://secure.indeed.com/account')
    credentials = login()
    userfield = driver.find_element_by_id('signin_email')
    userfield.send_keys(credentials[0])
    passwordfield = driver.find_element_by_id('signin_password')
    passwordfield.send_keys(credentials[1])
    passwordfield.submit()

def scrapper(jt,num,rb):
    # Given a job title,page num and year of exp id, collect all the links
    url = f"https://www.indeed.com/resumes?q={jt}&l=CA&co=US&lmd=all&rb={rb}&start={num}"
    temp =[]
    driver.get(url)
    results = driver.find_elements_by_xpath('//div[@class="app_name"]')
    if results!= []:
        for result in results:
            tag = result.find_element_by_xpath('./a')
            temp.append(tag.get_attribute('href'))
        return temp
    else:
        return ''
        
def limited(until):
    duration = int(round(until - time.time()))
    print('Rate limited, sleeping for {:d} seconds'.format(duration))

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
indeedlogin()
title =[]
job_titles =['"data+scientist"','"data+analyst"']
exp_rbdict  ={'<1year':'yoe%3A1-11',
             '1-2 years':'yoe%3A12-24',
             '3-5 years':'yoe%3A25-60',
             '6-10 years':'yoe%3A61-120',
             'More than 10 years':'yoe%3A121'}
rate_limiter = RateLimiter(max_calls=17, period=180, callback=limited)
for jt in tqdm(job_titles):  
    for rb in exp_rbdict:
        pagenum = get_num_pages(jt,exp_rbdict[rb])
        if pagenum is not None:
            for num in tqdm(pagenum):
                with rate_limiter:
                    temp =scrapper(jt,num,exp_rbdict[rb])
                    title+=temp
                    if num%500 ==0 or len(temp)==0: 
                        data = pd.DataFrame(np.array(title),columns=['links'])
                        data.to_csv('links3.csv')
                        print('No of links:',len(title))
        else:
            print('No pages available')
driver.quit() # close browser
data = pd.DataFrame(np.array(title),columns=['links'])
data.to_csv('links4.csv')
