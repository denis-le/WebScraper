import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# Make GET request
url = 'https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&os=win&supportedlang=english&snr=1_7_7_popularcomingsoon_7&filter=popularcomingsoon&infinite=1'

def total(url):
    url2 = requests.get(url)
    data = dict(url2.json())
    total = data['total_count']
    return int(total)

def get_data(url):
    url2 = requests.get(url)
    data = dict(url2.json())
    return data['results_html']

def parse(data):
    gameslist = []

    # parsing HTML
    soup = BeautifulSoup(data, 'html.parser')

    # find all the 'a' tags
    links = soup.find_all('a')
    
    for link in links:
        title = link.find('span', {'class': 'title'}).text
        date = link.find('div', {'class': 'search_released'}).text.strip()
        
        try:
            price = link.find('div', {'class': 'search_price'}).text.strip().split('$')[1]
        except:
            price = link.find('div', {'class': 'search_price'}).text.strip().split('$')[0]

        try:
            discount = link.find('div', {'class': 'search_price'}).text.strip().split('$')[2]
        except:
            discount = price

        game = {
            'title': title,
            'date': date,
            'price': price,
            'discounted_price': discount
        }

        gameslist.append(game)
    return gameslist

def output(gameslist):
    gamesdf = pd.concat([pd.DataFrame(g) for g in upcoming_games])
    gamesdf.to_csv('upcoming_games.csv', index = False)
    print('done')
    print(gamesdf.head())
    return

upcoming_games = []
for x in range(0, total(url), 50):
    url2 = (f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&os=win&supportedlang=english&snr=1_7_7_popularcomingsoon_7&filter=popularcomingsoon&infinite=1')
    data = get_data(url2)
    upcoming_games.append(parse(data))
    
output(upcoming_games)
