import requests
from concurrent.futures import ThreadPoolExecutor
import os, io
from tqdm import tqdm
from PIL import Image

def get_and_write(url):
    print(f"Now Processing: {url[1]}")
    res = requests.get(url[0])

    if url[0].lower().endswith(".jpeg"):
        url_ending = "jpg"
    
    else:
        url_ending = url[0].split('.')[-1].lower()
    
    fname = f"images/{url[1]}.{url_ending}"

    fob = io.BytesIO(res.content)

    try:
        img = Image.open(fob)

        if img.mode.lower() != 'rgb':
            print(f"Converted: {url[1]}")
            img = img.convert('RGB')

        img = img.resize((224, 224), Image.ANTIALIAS)
    
        img.save(f"images/{url[1]}.jpg", 'JPEG', quality = 100)

    except Exception as e:
        print(e)

    with open("negatives_downloaded", 'a') as f:
        f.write(f"{url[0]}\n")
    
with open("negatives_parsed", 'r') as f:
    urls = f.readlines()

urls = [u.split('\n')[0] for u in urls]

url_pack = []

for url in urls:
    url_pack.append([url, len(url_pack) + 1])

with ThreadPoolExecutor(max_workers = 50) as pool:
    tqdm(pool.map(get_and_write, url_pack))