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
        'cookie': 'JSESSIONID=1A315AADDAF2CE0277811BE690BFCC9E.c1; JSESSIONID=1A315AADDAF2CE0277811BE690BFCC9E.c1; ROUTEID=.1; b1pi=!PHCbmHq94b10ydSuhX4P2qdnHtwURZ6fMQdDf3cPl+YFgvGfjRSIRpXgPo81JjRX4tdBDOPJFHq+kJY=; akacd_holding_page_uk=3702400036~rv=79~id=e42a32c4c99acb483e6887942d18747d; cmTPSet=Y; CoreID6=39642202223515249472389&ci=52540000|www.clarks.co.uk; clarkscookiepolicy=accept; 52540000|www.clarks.co.uk_clogin=v=7&l=61758021524947238963&e=1524949193820; rr_rcs=eF4FwbkNgDAQBMDEEb2s5PU9vuuANiyDJQIyoH5mSnnnLl6ZHgs8bUCXVbRMR6TFlD6kc23391xHZdMArWlql1QlIQLwB3VTEOQ',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
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
        'cookie': 'JSESSIONID=1A315AADDAF2CE0277811BE690BFCC9E.c1; ROUTEID=.1; b1pi=!PHCbmHq94b10ydSuhX4P2qdnHtwURZ6fMQdDf3cPl+YFgvGfjRSIRpXgPo81JjRX4tdBDOPJFHq+kJY=; akacd_holding_page_uk=3702400036~rv=79~id=e42a32c4c99acb483e6887942d18747d; cmTPSet=Y; CoreID6=39642202223515249472389&ci=52540000|www.clarks.co.uk; clarkscookiepolicy=accept; BVImplmain_site=19244; 52540000|www.clarks.co.uk_clogin=v=7&l=61758021524947238963&e=1524950206512; rr_rcs=eF4FwbsNgDAMBcAmFbs8yf_YG7BGFIhEQQfMz13b7u-5DmKxBLtYWRp1LYEqwO2duwZxRS7w6QO2nCBVgSzPqX1o5_UDZFYQ6A',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
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
