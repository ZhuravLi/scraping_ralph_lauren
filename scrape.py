import requests
from bs4 import BeautifulSoup
import random
from PIL import Image
import os
from utils import get_response
from utils import save_img_urls, load_img_urls
from utils import save_item_urls, load_item_urls
from utils import headers, user_agents_list


def scrape_images(url):
    # List of urls for every item
    item_urls = []

    # There are only 32 items on the page (max), so we make 5 requests
    print('Collecting item_urls')
    for i in range(6):
        params = {'start': str(i*32), 'sz': '32'}
        response = get_response(url, i, params)
        page = BeautifulSoup(response.text, 'html.parser')
        
        thumb_links = page.find_all('a', class_='thumb-link')

        for link in thumb_links:
            item = 'https://www.ralphlauren.nl' + link.get('href')
            item_urls.append(item)
    print('Item urls are collected')
    save_item_urls(item_urls)
    
    # Lists of img links  
    person_imgs = {}
    cloth_imgs = {}
    
    print('Collecting img urls')
    for i, item_url in enumerate(item_urls):
        response = get_response(item_url, i+1)
        item_page = BeautifulSoup(response.text, 'html.parser')
        
        item_imgs = item_page.find_all('img', class_='popup-img pdp-popup-img')
        if len(item_imgs) >= 2: 
            person_imgs[i+1] = item_imgs[0].get('data-img')
            cloth_imgs[i+1] = item_imgs[1].get('data-img')
    print('Img urls are collected')
    save_img_urls(person_imgs, cloth_imgs)
    
    print('Saving imgs')
    os.makedirs('./person_imgs', exist_ok=True)
    os.makedirs('./cloth_imgs', exist_ok=True)

    for i, link in person_imgs.items():   
        response = get_response(link, i, stream=True)
        img = Image.open(response.raw)
        img.save(f'./person_imgs/person_{i:0=4d}.png')
        
    for i, link in cloth_imgs.items():
        response = get_response(link, i, stream=True)
        img = Image.open(response.raw)
        img.save(f'./cloth_imgs/cloth_{i:0=4d}.png')
    print('Imgs are saved')
    
    
def fix_scraped_images(imgs_to_remove, imgs_1, imgs_2):
    print('Fixing unpaired imgs')
    # Removing pics
    for i in imgs_to_remove:
        person_img = f'./person_imgs/person_{i:0=4d}.png'
        if os.path.exists(person_img):
            os.remove(person_img)
        cloth_img = f'./cloth_imgs/cloth_{i:0=4d}.png'
        if os.path.exists(cloth_img):
            os.remove(cloth_img)
        # Remove links
        person_imgs.pop(i, None)
        cloth_imgs.pop(i, None)
    
    for i in imgs_1 + imgs_2:
        response = get_response(item_urls[i-1], i, stream=True) 
        item_page = BeautifulSoup(response.text, 'html.parser')
        item_imgs = item_page.find_all('img', class_='popup-img pdp-popup-img')
        if i in imgs_1:
            person_imgs[i] = item_imgs[2].get('data-img')
            cloth_imgs[i] = item_imgs[0].get('data-img')
        elif i in imgs_2:
            person_imgs[i] = item_imgs[2].get('data-img')
        
    # Saving fixed imgs
    for i in imgs_1 + imgs_2:
        # Saving person_img
        response = get_response(person_imgs[i], i, stream=True)
        img = Image.open(response.raw)
        img.save(f'./person_imgs11/person_{i:0=4d}.png')
        
        # Saving cloth_img
        response = get_response(cloth_imgs[i], i, stream=True)
        img = Image.open(response.raw)
        img.save(f'./cloth_imgs11/cloth_{i:0=4d}.png')
    print('Fixed imgs are saved')
        
        
if __name__ == "__main__":
    url = 'https://www.ralphlauren.nl/en/men/clothing/hoodies-sweatshirts/10204?webcat=men%7Cclothing%7Cmen-clothing-hoodies-sweatshirts'
    scrape_images(url)
    
    # There are 2 types of mistake: 
    # - item does not have person in cloth (in original link), these we delete
    imgs_to_remove = [140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150]
    # - two people on the image
    imgs_two_persons = [66, 72, 73, 82, 87, 89, 93, 95, 97, 100, 101, 132]
    # they are divided in two groups
    # persons -- image
    imgs_1 = [93, 97, 101]
    # image -- persons
    imgs_2 = [66, 72, 73, 82, 87, 89, 95, 100, 132]
    
    person_imgs, cloth_imgs = load_img_urls()
    item_urls = load_item_urls()
    fix_scraped_images(imgs_to_remove, imgs_1, imgs_2)