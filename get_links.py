import time
from selenium import webdriver
from login import login
import numpy as np

def get_num_pages(url):
    driver.get(url)
    result_cnt = driver.find_element_by_id('result_count')
    result_cnt = int(result_cnt.text.split(' ')[0].replace(',',''))
    pagenum = np.array(range(round(result_cnt/50)))*50
    return pagenum

def indeedlogin():
    driver.get('https://secure.indeed.com/account')
    credentials = login()
    userfield = driver.find_element_by_id('signin_email')
    userfield.send_keys(credentials[0])
    passwordfield = driver.find_element_by_id('signin_password')
    passwordfield.send_keys(credentials[1])
    passwordfield.submit()

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
indeedlogin()
title =[]
job_titles = {'data+analyst':['jtid%3A25613','jtid%3A2','jtid%3A116367'],
    'data+scientist':['jtid%3A540143','jtid%3A777866','jtid%3A4042737']}
for jt in tqdm(job_titles):
    rbs = job_titles[jt]
    for rb in tqdm(rbs):
        url = f"https://www.indeed.com/resumes?q={jt}&l=CA&co=US&rb={rb}&lmd=all&start=50"
        pagenum = get_num_pages(url)
        for num in tqdm(pagenum):
            url = f"https://www.indeed.com/resumes?q={jt}&l=CA&co=US&rb={rb}&lmd=all&start={num}"
            driver.get(url)
            print(url)
            results = driver.find_elements_by_xpath('//div[@class="app_name"]')
            for result in results:
                tag = result.find_element_by_xpath('./a')
                title.append(tag.get_attribute('href'))