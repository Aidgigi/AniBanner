import requests
from concurrent.futures import ThreadPoolExecutor

def get_and_write(url):
    res = requests.get(url)

    with open(url.split('/')[-1], 'wb') as f:
        f.write(res.content)
    
with open("negatives_parsed", 'r') as f:
    urls = f.readlines()

urls = [u.split('\n')[0] for u in urls]

with ThreadPoolExecutor(max_workers = 50) as pool:
    pool.map(get_and_write, urls)