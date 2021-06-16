import requests
from concurrent.futures import ThreadPoolExecutor
import os
from tqdm import tqdm 

def get_and_write(url):
    res = requests.get(url[0])

    if url[0].lower().endswith(".jpeg"):
        url_ending = "jpg"
    
    else:
        url_ending = url[0].split('.')[-1].lower()

    with open(f"images/{url[1]}.{url_ending}", 'wb') as f:
        f.write(res.content)

    with open("negatives_downloaded", 'a') as f:
        f.write(f"{url[0]}\n")
    
with open("negatives_parsed", 'r') as f:
    urls = f.readlines()

urls = [u.split('\n')[0] for u in urls]

url_pack = []

for url in urls:
    url_pack.append([url, len(url_pack) + 1])

with ThreadPoolExecutor(max_workers = 50) as pool:
    tqdm(pool.map(get_and_write, url_pack), total = len(url_pack))