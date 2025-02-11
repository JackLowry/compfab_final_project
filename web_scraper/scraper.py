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
    # Use 'with' to ensure the session context is closed after use.
    # Fill in your details here to be posted to the login form.
    with open('web_scraper/minecraft_schematica_login_data.txt', 'r') as f:
        lines = f.readlines()
        payload = {
            'email_state': 'good',
            'password_state': 'good',
            'email': lines[0],
            'password': lines[1]
        }

    with requests.Session() as s:
        p = s.post('https://www.minecraft-schematics.com/login/action/', data=payload)
        for schematic_id in tqdm.tqdm(ids):
            # print the HTML returned or something more intelligent to see if it's a successful login page.
            print(p.text)

            # An authorised request.
            r = s.get(f'https://www.minecraft-schematics.com/schematic/24003/download/action/?type=schematic', allow_redirects=True)
            print(r.text)




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
        