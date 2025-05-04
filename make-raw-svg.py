# coding: utf-8
import json
with open('scrap-2025-05-04.json', 'r', encoding='utf-8') as f: J = json.load(f)
from itertools import count
from collections import defaultdict
counters = defaultdict(count)
out = []

from urllib.parse import quote as urlquote
from html import escape as attrquote
import colorhash

for i, video in enumerate(J):
    v = video
    nvideo = next(counters[v['category_slug']])
    x = 50 * nvideo
    y = 50 * ['mathematiques', 'physique', 'chimie', 'biologie'].index(v['category_slug'])
    
    color_hexstring = colorhash.ColorHash(v['link'], lightness=[0.5], saturation=[0.8]).hex
    link, name = v['link'], v['name']
    out.append(
        f'<g data-link="{urlquote(link)}" data-name="{attrquote(name)}">'
        f'<circle fill="{color_hexstring}" cx="{x}" cy="{y}" r="20"></circle>'
        f'<text font-size="0.5em" x="{x+25}" y="{y+25}" text-anchor="middle">{attrquote(name)}</text>'
        f'</g>')
    
with open('raw.svg', 'w', encoding='utf-8') as f: f.write('''
<svg version="1.1"
     width="1920" height="1080"
     xmlns="http://www.w3.org/2000/svg"><g transform="translate(50,50)">{}</g></svg>
'''.format(''.join(out)))
