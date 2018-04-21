from datetime import datetime
import os

import dill
import overpy


def get_prefs():
    prefs = ''
    with open('pref.txt', mode='r') as f:
        for row in f.readlines():
            prefs += '{}|'.format(row.rstrip()) 
    return prefs[:-1]


def input_node_info():
    key = input('Input node key:')
    tag = input('Input tag of key:')
    return key, tag


def save_result(result, key, tag):
    now = datetime.now()
    date = '{}{}{}'.format(now.year, now.month, now.day)
    filename = 'data/{}-{}_{}.pkl'.format(date, key, tag)
    
    print('Save as {}'.format(filename))
    
    if not os.path.exists(filename):
        with open(filename, 'wb') as f:
            dill.dump(result, f)
        print('Save complete.')

        
def fetch_result(key, tag):
    api = overpy.Overpass()
    prefs = get_prefs()
    query = (
        'area["name"~"{prefs}"];\n'
        'node(area)["{key}"="{tag}"];\n'
        'out;'
    ).format(prefs=prefs, key=key, tag=tag)
    print('Fetch query...')
    result = api.query(query)
    print('Fetch complete')
    save_result(result, key, tag)


def main():
    key, tag = input_node_info()
    fetch_result(key, tag)


if __name__ == "__main__":
    main()
