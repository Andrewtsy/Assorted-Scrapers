from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys

link = 'https://www.hackerrank.com/domains/python'

# Miscallaneous extra problems
probs = ['alphabet-rangoli', 'capitalize', 'py-check-subset', 'py-check-strict-superset', 'validating-uid', 'detect-html-tags-attributes-and-attribute-values', 'html-parser-part-2', 'np-mean-var-and-std', 'np-dot-and-cross', 'np-inner-and-outer', 'np-polynomials', 'np-linear-algebra']

# Create own text file with hackerrank username and password
file = open(r'cred.txt', 'r')
USERNAME, PASSWORD = map(lambda i: i.strip(), file.readlines())
file.close()

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(link)
    
    # iterates through each difficulty and subdomain combination and extracts ten problem names from each
    elements = driver.find_elements_by_class_name('checkbox-input')
    diffs, subs = elements[6:9], elements[9:]
    for diff in diffs:
        diff.click()
        for sub in subs:
            sub.click()
            time.sleep(2)
            page = driver.page_source
            soup = bs(page, 'html.parser')
            probs.extend([i.get('data-attr1') for i in soup.find_all('a', class_='js-track-click challenge-list-item')])
            sub.click()
        diff.click()
    time.sleep(5)
    
    # Authentication
    driver.find_element_by_css_selector('button.login.pull-right.btn.btn-dark.btn-default.mmT').click()
    
    driver.find_element_by_id('input-1').send_keys(USERNAME)
    driver.find_element_by_id('input-2').send_keys(PASSWORD)
    driver.find_element_by_id('input-2').send_keys(Keys.RETURN)
    
    time.sleep(5)
    
    # Scrapes each problem into a .py file
    for PROBLEM in probs:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(f'https://www.hackerrank.com/rest/contests/master/challenges/{PROBLEM}/hackers/{USERNAME}/download_solution')
                  
        page = driver.page_source
        soup = bs(page, 'html.parser')
        text = soup.get_text()
        assert 'Access Denied' not in text
        
        file = open(f'{PROBLEM}.py', 'w')
        file.write(text)
        
        time.sleep(2)
        file.close()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

if __name__ == '__main__':
    main()