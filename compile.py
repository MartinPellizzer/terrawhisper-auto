import os
import csv
import shutil
import markdown

start_folder = 'G:/tw-images/auto'


def is_row_not_empty(row):
    found = False
    for cell in row:
        if cell.strip() != '':
            found = True
            break
    return found


def csv_to_llst(filepath):
    llst = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            if is_row_not_empty(row):
                llst.append(row)
    return llst


shutil.copy2('style.css', 'website/style.css')

plants_rows = csv_to_llst('plants.csv')

plants_dict = {}
for i, item in enumerate(plants_rows[0]):
    plants_dict[item] = i

for plant_row in plants_rows[1:]:
    entity = plant_row[plants_dict['entity']].strip()
    common_name = plant_row[plants_dict['common_name']].strip().lower()
    latin_name = entity.capitalize().replace('-', ' ')

    article_md = ''

    with open(f'database/articles/{entity}/medicine.md') as f: content = f.read()
    article_md += f'## medicine\n\n'.title()
    try: shutil.copy2(f'{start_folder}/{entity}/0000.jpg', f'website/images/{entity}-medicine.jpg')
    except: pass
    article_md += f'\n\n![medicine](images/{entity}-medicine.jpg "medicine")\n\n'
    article_md += f'{content}\n\n'
    
    with open(f'database/articles/{entity}/cuisine.md') as f: content = f.read()
    article_md += f'## cuisine\n\n'.title()
    try: shutil.copy2(f'{start_folder}/{entity}/0001.jpg', f'website/images/{entity}-cuisine.jpg')
    except: pass
    article_md += f'\n\n![cuisine](images/{entity}-cuisine.jpg "cuisine")\n\n'
    article_md += f'{content}\n\n'
    
    with open(f'database/articles/{entity}/horticulture.md') as f: content = f.read()
    article_md += f'## horticulture\n\n'.title()
    try: shutil.copy2(f'{start_folder}/{entity}/0002.jpg', f'website/images/{entity}-horticulture.jpg')
    except: pass
    article_md += f'\n\n![horticulture](images/{entity}-horticulture.jpg "horticulture")\n\n'
    article_md += f'{content}\n\n'
    
    with open(f'database/articles/{entity}/botany.md') as f: content = f.read()
    article_md += f'## botany\n\n'.title()
    try: shutil.copy2(f'{start_folder}/{entity}/0003.jpg', f'website/images/{entity}-botany.jpg')
    except: pass
    article_md += f'\n\n![botany](images/{entity}-botany.jpg "botany")\n\n'
    article_md += f'{content}\n\n'
    
    with open(f'database/articles/{entity}/history.md') as f: content = f.read()
    article_md += f'## history\n\n'.title()
    try: shutil.copy2(f'{start_folder}/{entity}/0004.jpg', f'website/images/{entity}-history.jpg')
    except: pass
    article_md += f'\n\n![history](images/{entity}-history.jpg "history")\n\n'
    article_md += f'{content}\n\n'

    article_html = markdown.markdown(article_md, extensions=['markdown.extensions.tables'])

    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="Martin Pellizzer">
            <link rel="stylesheet" href="/style.css">
            <title>{latin_name}</title>
        </head>

        <body>
            <section class="container">
                {article_html}
            </section>
        </body>

        </html>
    '''

    with open(f'website/{entity}.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(plant_row)
