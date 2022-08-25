#Importing Libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
from tqdm import tqdm
from selenium import webdriver
import chromedriver_binary
import streamlit as st

path = chromedriver_binary.chromedriver_filename

inp = st.text_input("Enter the title of Job: ") 
time.sleep(15)

#Temporary web driver to extract number of pages

link = "https://www.naukri.com/"+inp.replace(" ","-") +"-jobs-"
temp = webdriver.Chrome(path)
temp.get(link)
soup = BeautifulSoup(temp.page_source,'html.parser')


#Number of web pages for a particular job

x= soup.find('span',class_='fleft grey-text mr-5 fs12').text[10:15]
x = x.strip(' ')
x = round(int(x)/20)
st.write(f"Number of pages to be scraped: {x}")

#Defining a function to generate a list of URL's of all pages
base_url  = "https://www.naukri.com/"

all_urls = list()

def generate_urls():
    for i in range(0,x+1):
        all_urls.append(base_url + inp.replace(" ","-") +"-jobs-"+ str(i))

generate_urls()
st.write(f"List of first 5 URL's : {all_urls[1:5]}")


# A function used to open multiple windows to scrap data from each window
def multiple_browser():
    lis  = []
    lis2 = []
    Data = []
    for i in tqdm(range(x+1)):

        browser = (('browser'+str(i)))
        lis.append([browser])
        lis[i]  = webdriver.Chrome(path)
        lis[i].get(str(all_urls[i]))
        soup = (('soup'+str(i)))
        lis2.append([soup])
        lis2[i]  = BeautifulSoup(lis[i].page_source,'html.parser')
        time.sleep(2)
        for sp in lis2[i].find_all('article',class_='jobTuple bgWhite br4 mb-8'):
            try:
                title               = sp.find('a',class_='title fw500 ellipsis').text
            except:
                title               = np.nan
            try:
                company_name        = (sp.find('a',class_='subTitle ellipsis fleft').get('title'))
            except:
                company_name        = np.nan    
            try:    
                link                = sp.find('a',class_='title fw500 ellipsis').get('href')
            except:
                link                = np.nan
            try:    
                rating              = soup.find('span',class_='starRating fleft dot').text
            except:
                rating              = np.nan
            try:
                Review_page_company = sp.find('a',class_='reviewsCount ml-5 fleft blue-text').get('href')
            except:
                Review_page_company = np.nan
            try:    
                Rating_Company      = sp.find('a',class_='reviewsCount ml-5 fleft blue-text').text
            except:
                Rating_Company      = np.nan
            try:
                experience          = sp.find('span',class_='ellipsis fleft fs12 lh16').get('title')
            except:
                experience          = np.nan
            try:    
                salary              = sp.find('li',class_='fleft grey-text br2 placeHolderLi salary').text
            except:
                salary              = np.nan
            try:
                Location            = sp.find('li',class_ = 'fleft grey-text br2 placeHolderLi location').text
            except:
                Location            = np.nan
            try:
                Skill_Set           = sp.find('ul',class_ = 'tags has-description').text
            except:
                Skill_Set           = np.nan

            Data.append([title,company_name,rating,experience,salary,Rating_Company,Location,Skill_Set,link,Review_page_company])
    df = pd.DataFrame(Data,columns=['Title','Company','Rating','Experience','Salary','Rating of Company','Location','Skill_Set','Link','Review_page_company'])
    df.to_csv("Multi_Windows_Scrap_streamlit.csv",index=False)
    return st.dataframe(data=df)

multiple_browser()

df_1 = pd.read_csv('Multi_Windows_Scrap_streamlit.csv')

### Scraping from individual posts
browser = webdriver.Chrome(path)
data = []
for i in tqdm(df_1['Link']):
    browser.get(i)
    soup = BeautifulSoup(browser.page_source,'html.parser')
    time.sleep(0.5)
    try:
        Average_Salary = soup.find('span',class_='avg-salary-inner').text
    except:
        Average_Salary = np.nan
    try:    
        Role           = soup.find('div',class_='other-details').text.split(',')
    except:
        Role           = np.nan
    try:    
        Education      = soup.find('div',class_='education').text[9:]
    except:
        Education      = np.nan
    data.append([Average_Salary,Role,Education])    
df = pd.DataFrame(data,columns=['Expected Average Salary','Role','Education'])
st.write("Dataframe for Multi Job Scrape")
st.dataframe(data=df)
df.to_csv("Multi_Jobs_Depth_Scrap_streamlit.csv",index=False)

df_common = pd.DataFrame()

df_common['Company']                  = df_1['Company']
df_common['Title']                    = df_1['Title']
df_common['Role']                     = df['Role']
df_common['Experience']               = df_1['Experience']
df_common['Real Salary']              = df_1['Salary']
df_common['Expected Salary']          = df['Expected Average Salary']
df_common['Education']                = df['Education']
df_common['Company Rating']           = df_1['Rating']
df_common['Reviews of Company']       = df_1['Rating of Company']
df_common['Location']                 = df_1['Location']
df_common['Skills']                   = df_1['Skill_Set']
df_common['Link']                     = df_1['Link']
df_common['Review Page of Company']   = df_1['Review_page_company']

st.write("Combined Dataframe")
st.dataframe(data=df_common)
st.markdown("Your data has been scraped and saved in your current working directory!!!")
df_1.to_csv("Data_Scientist_Jobs_main_final_streamlit.csv",index=False)
    
        
        
