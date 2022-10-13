import requests
import math
import pandas as pd
from bs4 import BeautifulSoup as bs

def first_roll():
    global count
    global mask
    
    r = requests.get(handle)
    page = r.text
    soup = bs(page, 'html.parser')
    numbers = soup.find('pre', class_='data').get_text().split('\n')[:-1]
    
    numbers = list(map(lambda i: i.split('\t'), numbers))
    numbers = list(map(lambda i: (int(i[0]), int(i[1])), numbers))
    print(numbers)
    die_1, die_2 = list(zip(*numbers))
    sum_ = list(map(sum, numbers))
    result = [True if i in (7, 11) else False if i in (2, 3, 12) else i for i in sum_]
    
    df['die_1_1'] = die_1
    df['die_2_1'] = die_2
    df['sum_1'] = sum_
    df['result_1'] = result
    
    mask = [1 if type(i) == int else 0 for i in result]
    count = sum(mask)
    
    print(result)
    print(mask)

def n_rolls():
    global count
    global mask
    index = 1
    
    while count != 0:
        print(count)
        index += 1
        die_1 = []
        die_2 = []
        sum_ = []
        result = []
        
        r = requests.get(handle)
        page = r.text
        soup = bs(page, 'html.parser')
        numbers = soup.find('pre', class_='data').get_text().split('\n')[:-1]
        
        numbers = list(map(lambda i: i.split('\t'), numbers))
        numbers = list(map(lambda i: (int(i[0]), int(i[1])), numbers))
        numbers = [i[0] if i[1] else (0, 0) for i in zip(numbers, mask)]
        print(numbers)
        die_1, die_2 = list(zip(*numbers))
        # die_1 = [math.prod(i) for i in zip(die_1, mask)]
        # die_2 = [math.prod(i) for i in zip(die_2, mask)]
        sum_ = list(map(sum, numbers))
        # sum_ = [math.prod(i) for i in zip(sum_, mask)]
        
        print(sum_)
        
        for i, j in enumerate(sum_):
            if j == 0:
                result.append(0)
            elif j == df['sum_1'][i]:
                result.append(True)
            elif j == 7:
                result.append(False)
            else:
                result.append('Roll Again')
                
        print(result)
        
        df[f'die_1_{index}'] = die_1
        df[f'die_2_{index}'] = die_2
        df[f'sum_{index}'] = sum_
        df[f'result_{index}'] = result
        
        mask = [1 if i=='Roll Again' else 0 for i in result]
        count = sum(mask)
        
        print(mask)

if __name__ == '__main__':

    df = pd.DataFrame()
    count = 200
    index = 0
    mask = 200*[1]
    
    handle = 'https://www.random.org/integers/?num=400&min=1&max=6&col=2&base=10&format=html&rnd=new'

    first_roll()
    n_rolls()   

    df.to_csv('ch6results.csv')