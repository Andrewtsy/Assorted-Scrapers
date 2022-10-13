import requests
from urllib.request import urlopen
import json
from time import sleep
import re

# Gets AoPS Course handouts page
handouts_url = input('Enter class handouts page url')
r = requests.get(handouts_url)
text = r.text

# Parses for individual handout names/links
p = re.compile('\"file\"\:\"([^"]+)')
urls = re.findall(p, text)
k = re.compile('\"name\"\:\"([^"]+)')
titles = re.findall(k, text) 

# Maps to dictionary
for title in titles:
    for url in urls:
        dic[title] = handouts_url + url
        urls.remove(url)
        break

direct = input('Enter wanted file directory')

# Downloads each handout as pdf
for title, url in dic.items():
    try:
        sleep(5)
        print(title, url)
        r = requests.get(url, stream = True)
        file = f'{direct}{str(title)}.pdf'
        with open(file, 'wb') as pdf:
            for chunk in r.iter_content(chunk_size = 1024):
                pdf.write(chunk)
    except:
        print('Unable to retrieve page')
        continue