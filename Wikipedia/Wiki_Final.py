import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

inp   = input("Enter Persons name: ")
time.sleep(15)
link  = 'https://www.google.com/search?q=' + str(inp) +" "+ "Wikipedia"
link  = link.replace(' ','+')
print(link)

res = requests.get(link)
soup = BeautifulSoup(res.text,'html.parser')

for sp in soup.find_all('div'):
    try:
        link = sp.find('a').get('href')
        
        if('en.wikipedia.org' in link):
            break
    except:
        pass
link = (link[7:]).split('&')[0]
print(link)

res = requests.get(link)
soup = BeautifulSoup(res.text,'html.parser')

heading = soup.find('h1').text
print(heading)


paragraphs = ''

for p in soup.find_all('p'):
    paragraphs += p.text
    paragraphs += '\n'
    
    
paragraphs = paragraphs.strip()
print(paragraphs)

for i in range(1000):
    paragraphs = paragraphs.replace('[' + str(i) + ']','')
    
    fd = open(heading + ".txt" , 'w',encoding='utf-8')
fd.write(paragraphs)
fd.close()