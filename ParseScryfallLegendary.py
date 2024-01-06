"""
req_all_legends = 'https://api.scryfall.com/cards/search?q=type%3Alegendary'
"""

import urllib.request
import json
import time


cut_second_side_name = True
with (open('ScryfallData/LegendsScryFall.txt', 'w', encoding='utf-8') as fd,
      open('ScryfallData/Partners.txt', 'w', encoding='utf-8') as fdPartners,
      open('ScryfallData/Background.txt', 'w', encoding='utf-8') as fdBackground,
      open('ScryfallData/Companion.txt', 'w', encoding='utf-8') as fdCompanion):
    req = 'https://api.scryfall.com/cards/search?q=type%3Alegendary'
    json_L = {'has_more': True}
    i = 1
    while json_L['has_more']:
        contents = urllib.request.urlopen(req).read()
        time.sleep(0.2)  # no ddos scryfall, they don't want more than 10 requests per second
        json_L = json.loads(contents.decode('utf-8'))
        for item in json_L['data']:

            if cut_second_side_name:
                name = (item['name'].split(' // '))[0]
            else:
                name = item

            def color_identity_to_str(identity: list):
                color_identity = ''
                for elem in item['color_identity']:
                    color_identity += elem
                return color_identity

            # item['color_identity'] <=> ['B', 'G', 'R', 'U', 'W']
            if 'Partner' in item['keywords']:
                fdPartners.write(f"{item['name']} :: {color_identity_to_str(item['color_identity'])}\n")
            if -1 != item['type_line'].find('Background'):
                fdBackground.write(f"{item['name']} :: {color_identity_to_str(item['color_identity'])}\n")
            if 'Companion' in item['keywords']:
                fdCompanion.write(f"{item['name']} :: {color_identity_to_str(item['color_identity'])}\n")
            fd.write(f"{name}\n")

        print(f"page:{i:>4}")
        i += 1
        if json_L['has_more']:
            req = json_L['next_page']

    # erase last '\n' in files
    fd.truncate(fd.tell() - 1)
    fdPartners.truncate(fdPartners.tell() - 1)
    fdBackground.truncate(fdBackground.tell() - 1)
    fdCompanion.truncate(fdCompanion.tell() - 1)
