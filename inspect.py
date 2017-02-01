from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import time
import re

url = "https://www.epa.gov/"

link = urlopen(url)
soup = BeautifulSoup(link)
count = 0
list1 = []
list2 = []
for x in soup.findAll('a'):
    list1.append(x['href'])
    url = x['href']
    if url.startswith("https://www.epa.gov") or url.startswith('/'):
        if not url.startswith('/languages'):
            list2.append(url)

for x in list1:
    if x not in list2:
        count+=1
        print(x)

print(len(list1), count)
