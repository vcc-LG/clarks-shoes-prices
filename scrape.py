import requests
from bs4 import BeautifulSoup
import numpy as np 
from matplotlib import pyplot as plt 

def get_soup(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        print('could not parse html')
    return soup

def get_list_of_elements_by_class(soup, class_name):
    try:
        list_of_elements = soup.find_all(class_=class_name)
    except:
        print('could not find elements of class {}'.format(class_name))
    return list_of_elements

def get_item_price(item):
    try:
        price = float(item.find_all("span",{"itemprop":"price"})[0].text.strip('£'))
    except:
        try:
            price = float(item.find_all("span",{"itemprop":"lowPrice"})[0].text.strip('£'))
        except:
            print('could not parse price')
            import ipdb; ipdb.set_trace()
    return price

def get_girl_shoe_response():
    headers = {
        'cookie': '',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': '',
        'accept': '*/*',
        'referer': 'https://www.clarks.co.uk/Girls/All-styles/c/g4',
        'authority': 'www.clarks.co.uk',
        'x-requested-with': 'XMLHttpRequest',
    }
    params = (
        ('q', ':relevance'),
        ('show', 'All'),
        ('_', '1524947394149'),
    )
    try:
        response = requests.get('https://www.clarks.co.uk/Girls/All-styles/c/g4', headers=headers, params=params)
    except:
        print('could not girls shoes response')
    return response

def get_boy_shoe_response():
    headers = {
        'cookie': '',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': '',
        'accept': '*/*',
        'referer': 'https://www.clarks.co.uk/Boys/All-Styles/c/b4',
        'authority': 'www.clarks.co.uk',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = (
        ('q', ':relevance'),
        ('show', 'All'),
        ('_', '1524948406792'),
    )

    try:
        response = requests.get('https://www.clarks.co.uk/Boys/All-Styles/c/b4', headers=headers, params=params)
    except:
        print('could not boys shoes response')
    return response

if __name__ == "__main__":

    girl_shoe_prices = []
    girl_soup = get_soup(get_girl_shoe_response())
    girl_list_of_items = get_list_of_elements_by_class(girl_soup, 'product-thumbnail-container')
    for item in girl_list_of_items:
        girl_shoe_prices.append(get_item_price(item))


    boy_shoe_prices = []
    boy_soup = get_soup(get_boy_shoe_response())
    boy_list_of_items = get_list_of_elements_by_class(boy_soup, 'product-thumbnail-container')
    for item in boy_list_of_items:
        boy_shoe_prices.append(get_item_price(item))

    min_val = min(girl_shoe_prices + boy_shoe_prices)
    max_val = max(girl_shoe_prices + boy_shoe_prices)
    bins = np.linspace(min_val, max_val, 50)

    print('found {} items for girls'.format(len(girl_shoe_prices)))
    print('found {} items for boys'.format(len(boy_shoe_prices)))

    print('mean price for girls = £{:.2f}'.format(np.mean(girl_shoe_prices)))
    print('mean price for boys = £{:.2f}'.format(np.mean(boy_shoe_prices)))

    print('median price for girls = £{:.2f}'.format(np.median(girl_shoe_prices)))
    print('median price for boys = £{:.2f}'.format(np.median(boy_shoe_prices)))

    print('max price for girls = £{}'.format(max(girl_shoe_prices)))
    print('max price for boys = £{}'.format(max(boy_shoe_prices)))

    print('min price for girls = £{}'.format(min(girl_shoe_prices)))
    print('min price for boys = £{}'.format(min(boy_shoe_prices)))

    plt.hist(girl_shoe_prices, bins, alpha = 0.5, label='girls',color="crimson")
    plt.hist(boy_shoe_prices, bins, alpha = 0.5,label='boys',color="blue")
    plt.title('Kid\'s shoe prices in Clarks for boys and girls shoes')
    plt.xlabel('Price (£)')
    plt.ylabel('Count')
    plt.legend(loc='upper right')
    plt.show()
