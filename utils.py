import requests
import random
from time import sleep
from PIL import Image


# Headers for requests
user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0'
]
headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'referer': 'https://www.google.com/',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': random.choice(user_agents_list),
    }


def get_response(url, num_url, params=None, stream=False):
    """Sending request by url until response is not ok
        num_url (int): sequence number of url
    """
    headers['user-agent'] = random.choice(user_agents_list)
    response = requests.get(url, headers=headers, params=params, stream=stream) 
    while not response.ok:
        sleep(1)
        print('Error in url №', num_url, '\t', response.status_code)
        headers['user-agent'] = random.choice(user_agents_list)
        response = requests.get(url, headers=headers, params=params, stream=stream) 
    print(f'Url № {num_url} is ready')
    return response


def save_item_urls(item_urls):
    with open('item_urls.txt', 'w') as f:
        for i, link in enumerate(item_urls):
            f.write(str(i+1)+' '+link+'\n')
   
            
def load_item_urls():
    item_urls = []
    with open('item_urls.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        item_urls.append(line.split()[1])
    return item_urls


def save_img_urls(person_imgs, cloth_imgs):
    with open('person_imgs.txt', 'w') as f:
        for i, link in person_imgs.items():
            f.write(str(i)+' '+link+'\n')
    with open('cloth_imgs.txt', 'w') as f:
        for i, link in cloth_imgs.items():
            f.write(str(i)+' '+link+'\n')
            

def load_img_urls():
    person_imgs = {}
    cloth_imgs = {}
    with open('person_imgs.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            person_imgs[int(line.split()[0])] = line.split()[1]
    with open('cloth_imgs.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            cloth_imgs[int(line.split()[0])] = line.split()[1]
    return person_imgs, cloth_imgs
