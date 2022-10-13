import os
import re
import time

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

# sets options to automatically download files into folder names 'downloads'
options = Options()
options.add_experimental_option('prefs', {'download.default_directory': os.path.abspath('downloads')})

# makes driver and opens jair homepage
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://www.jair.org/index.php/jair')

# using beautifulsoup and regex, parses html for names and links of each paper
page = driver.page_source
soup = bs(page, 'html.parser')
p1 = re.compile('^https://www\.jair\.org/index\.php/jair/article/view/[0-9]{5}$')
p2 = re.compile('^https://www\.jair\.org/index\.php/jair/article/view/[0-9]{5}/[0-9]{5}$')

names = [''.join([i for i in i.get_text() if i.isalnum()]) for i in soup.find_all('a', href=p1)]
links = [i['href'].replace('view', 'download') for i in soup.find_all('a', href=p2)]

# creates dictionary of each paper's title and url
papers = dict(zip(names, links))

# iterates through papers in the issue by accessing the download url and renaming the pdfs
for name, link in papers.items():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(link)
    
    time.sleep(2.5)
    fname = max(os.listdir('downloads'), key=lambda x: os.path.getatime(os.path.join('downloads', x)))
    try:
        os.rename(os.path.join('downloads', fname), os.path.join('downloads', f'{name}.pdf')) 
    except OSError:
        print(f'unable to rename {name} file')
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

driver.close()