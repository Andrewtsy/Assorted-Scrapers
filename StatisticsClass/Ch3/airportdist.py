import requests
from bs4 import BeautifulSoup as bs
import csv

arr = list()
out = list()

home = input('What is your home airport?')

with open('airports.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for line in csvreader:
        airport = line[0][-4:-1]
        arr.append(airport)

for airport in arr:
    link = f'https://www.airportdistancecalculator.com/flight-{home}-to-{airport}.html'
    response = requests.get(link)
    soup = bs(response.content, 'html.parser')
    try:
        out.append([airport, soup.find('p').find('span').string])
    except:
        out.append([airport, 'None'])
    
 
with open('airportdists.csv', mode='w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerows(out)