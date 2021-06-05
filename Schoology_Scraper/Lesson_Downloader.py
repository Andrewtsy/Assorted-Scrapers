from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
from bs4 import BeautifulSoup
import csv
import time

# Selenium Magyck
options = Options()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Note this may not be applicable to all display resolutions...
x0, y0 = str(pyautogui.size()).split()
x0 = x0[11:-1]
y0 = y0[7:-1]
coord = [int(x0) * 1/2, int(y0) * 16/39]

Sun = input('Enter Schoology username')
Spw = input('Enter Schoology Password')
GDun = input('Enter Google email (preferably school\'s))

# Gets page and Schoology authentication
driver.get(input('Enter Schoology course homepage materials url'))

# Schoology Authentification
def Ssignin():
    time.sleep(3)
    pyautogui.typewrite(un)
    pyautogui.click(coord[0], coord[1])
    time.sleep(3)
    pyautogui.typewrite(pw)
    pyautogui.click(coord[0], coord[1])
    time.sleep(5)

# Google Drive Authentification
def GDsignin():
    pyautogui.typewrite(GDun)
    pyautogui.click(int(x0) * 37/63, int(y0) * 26/39)
    time.sleep(5)
    pyautogui.click(int(x0) * 36/63, int(y0) * 21.5/39)
    time.sleep(5)

links = []

with open('links.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        links.append(str(row[0]))

Ssignin()
run_once = 0

# Downloads Google Drive pdfs
for link in links:
    driver.execute_script('window.open('');')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(link)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    for i in soup.find_all('iframe'):
        url = str(i.get('src'))
        print(url)
        if 'drive.google.com' in url:
            url = url[:-20] + 'view'
            print(url)
            driver.execute_script('window.open('');')
            driver.switch_to.window(driver.window_handles[2])
            try:
                driver.get(url)
            except:
                print('bad link')
                continue
            time.sleep(3)
            while run_once == 0:
                GDsignin()
                run_once += 1
            pyautogui.click(int(x0) * 58/63, int(y0) * 5/39)
            time.sleep(2)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])