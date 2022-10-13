import time
import csv

from selenium import webdriver
from bs4 import BeautifulSoup as bs

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.random.org/integers/?num=5&min=1&max=6&col=1&base=10&format=html&rnd=new')

numbers = []

for i in range(25):
    page = driver.page_source
    soup = bs(page, 'html.parser')

    number = soup.find('pre', class_='data').get_text()

    print(number.split('\n')[:-1])
    numbers.append(number.split('\n'))
    
    driver.refresh()
    
with open('numbers.csv', 'w', newline='') as file:
    csvwriter = csv.writer(file)
    csvwriter.writerows(numbers)