import json
import pickle
import time
import requests
from bs4 import BeautifulSoup
import tqdm

def scrape_minecraft_schematic_ids():
    num_pages = 70
    ids = []
    for page_idx in tqdm.tqdm(range(num_pages)):
        r = requests.get(f'https://www.minecraft-schematics.com/category/redstone/{page_idx}/')
        if r.status_code != 200:
            print(f'Bad request: {r.status.code}')

        soup = BeautifulSoup(r.content, 'html.parser')

        rows = soup.find_all("div", {"class": "row-fluid"})
        links = soup.find_all('a')
        for l in links:
            href = l.get('href')
            if href is not None and '/schematic/' in href:
                id = href.split('/')[-2]
                try:
                    id_int = int(id) #if the schematic isn't an integer (like an add schematic page), ignore it
                    ids.append(id)
                except ValueError:
                    pass
        time.sleep(0.1)
    with open('minecraft_schematic_redstone_ids', 'w') as f:
        json.dump(ids,  f)
    print(f"num ids scraped: {ids}")
    return ids
    
def scrape_minecraft_schematics(ids):
    for schematic_id in tqdm.tqdm(ids):
        r = requests.get(f'https://www.minecraft-schematics.com/schematic/{schematic_id}/')

if __name__ == '__main__':
    site = 'minecraft-schematics.com'
    pages_cached= True

    if site == 'minecraft-schematics.com':
        if not pages_cached:
            ids = scrape_minecraft_schematic_ids()
        else:
            with open('minecraft_schematic_redstone_ids', 'r') as f:
                ids = json.load(f)
        scrape_minecraft_schematics(ids)
        