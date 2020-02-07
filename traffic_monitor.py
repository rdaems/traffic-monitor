import os
import requests
from lxml import html


output_path = '/home/rdaems/traffic_monitor/data.csv'

urls = [
    'http://www.filebeeld.be/mobiel/reistijden/R0?from=GRB&to=SSW',
    'http://www.filebeeld.be/mobiel/reistijden/R0?from=SSW&to=GRB',
]
pages = [requests.get(url) for url in urls]
trees = [html.fromstring(page.content) for page in pages]
headers = ['date', 'binnenring_nu', 'buitenring_nu', 'binnenring_vertraging', 'buitenring_vertraging']

if not os.path.exists(output_path):
    with open(output_path, 'w') as f:
        f.write(','.join(headers) + '\n')

data = {
    'date': pages[0].headers['Date'].split(', ')[1],
    'binnenring_nu': trees[0].xpath('/html/body/table/tr[2]/td[2]/span/text()')[0],
    'buitenring_nu': trees[1].xpath('/html/body/table/tr[2]/td[2]/span/text()')[0],
    'binnenring_vertraging': trees[0].xpath('/html/body/table/tr[2]/td[3]/text()')[0],
    'buitenring_vertraging': trees[1].xpath('/html/body/table/tr[2]/td[3]/text()')[0],
}
for key in data:
    if data[key] == '-':
        data[key] = '0'

with open(output_path,'a') as f:
    f.write(','.join([data[h] for h in headers]) + '\n')
