from argparse import ArgumentParser
import csv
import functools
import json
import copy
from pprint import pformat, pprint
import sys

parser = ArgumentParser()

parser.add_argument('infile', help="json file to be read")
args = parser.parse_args()

filename = args.infile
targetfile = filename.strip('.json') + '.csv'

def flatten_field(inputitem, field):
    item = copy.deepcopy(inputitem)
    flattened = {key: item[field][key] for key in item[field]}
    item.update(flattened)
    item.pop(field)
    return item

def flattenauthors(inputitem):
    item = copy.deepcopy(inputitem)
    try:
        item['authors'] = ', '.join(item['authors']['author'])
    except KeyError:
        item_string = pformat(item)
        print('No author:' + item_string, file=sys.stderr)
        item['authors'] = None
    return item

with open(filename) as f:
    results = json.load(f)
    hits = results['result']['hits']['hit']
    flattened = list(map(lambda x: flatten_field(x, 'info'), hits))
    toprint = list(map(flattenauthors,flattened))
    keys = [item.keys() for item in toprint]
    allkeys = sorted(functools.reduce(lambda x,y: x | y, keys))

with open(targetfile, 'w') as tf:
    writer = csv.DictWriter(tf, allkeys)
    writer.writeheader()
    for item in toprint:
        writer.writerow(item)
