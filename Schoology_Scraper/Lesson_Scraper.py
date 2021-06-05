from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
from bs4 import BeautifulSoup
import time
from collections import defaultdict
import csv

# Class for each unit that bundles lessons, files, etc.
class Bundled():
    """Class for Units and more"""
    def __init__(self, unit):
        self.unit = unit
        self.lessons = defaultdict(dict)
        self.files = []

# Maps dictionary of units (Bundled instances)
Units = {}
for i in range(int(input('Enter how many units you would like to scrape'))):
    Units[input('Enter Unit Name')] = Bundled(input('Enter Unit Link'))
dom = input('Enter school\'s Schoology home page link')
Sun = input('Enter Schoology/School username')
Spw = input('Enter Schoology/School password')

# Selenium magyck
options = Options()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Note that this may not be applicable for all display resolutions
x0, y0 = str(pyautogui.size()).split()
x0 = x0[11:-1]
y0 = y0[7:-1]
coord = [int(x0) * 1/2, int(y0) * 16/39]

driver.get(input('Enter Course homepage materials url'))

# Schoology Authentification
def Ssignin():
    time.sleep(1)
    pyautogui.typewrite()
    pyautogui.click(coord[0], coord[1])
    time.sleep(1)
    pyautogui.typewrite(Spw)
    pyautogui.click(coord[0], coord[1])
    time.sleep(3)
    
Ssignin()

# Gets and Writes lesson page links to csv
Out = []
for Name, Unit in Units.items():
    driver.execute_script('window.open('');')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(Unit.unit)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    for i in soup.find_all('tr'):
        ele = i.find('a')
        if not ele == None:
            less = str(ele.get_text())
            link = dom + str(ele.get('href'))
            if '[LEARN]' in less:
                Unit.lessons[less] = link
    Out.append(Unit)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

with open('links.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    for Unit in Out:
        for less, link in Unit.lessons.items():
            writer.writerow([link])            