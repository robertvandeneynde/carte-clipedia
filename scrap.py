import bs4 
import requests
from itertools import count

def onlyone(it):
    if len(L := list(it)) != 1:
        raise ValueError('No values' if len(L) == 0 else 'Too much values')
    return L[0]

videos = []
for category_slug in ('mathematiques', 'physique', 'chimie', 'biologie'):
  for page in count(1):
    page1 = requests.get(f'https://clipedia.be/{category_slug}?page={page}').text
    print("Catégorie", category_slug, "Page", page)
    soup = bs4.BeautifulSoup(page1, features='lxml')
    videos_list = soup.select('.videos-list')
    if not videos_list:
        break
        
    video_list = onlyone(videos_list)
    videos_item = video_list.select('.videos-item')
    link_cls, label_cls, name_cls = '.videos-item-anchor', '.label', '.videos-item-title'
    
    out = []
    for video in videos_item:
        link = onlyone(video.select(link_cls)).get('href')
        label = onlyone(video.select(label_cls)).text
        name = onlyone(video.select(name_cls)).text
        out.append((link, label, name))
    
    for link, label, name in out:
        videos.append({
            'page': page,
            'link': link,
            'name': name,
            'category_slug': category_slug,
            'category_name': label,
        })
        
import json
with open('scrap.json', 'w', encoding='utf-8') as f:
    json.dump(videos, f, indent=4, ensure_ascii=False)
print('scrap.json')
