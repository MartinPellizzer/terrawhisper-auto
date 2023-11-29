import csv
import os
from ctransformers import AutoModelForCausalLM

num_articles = 10

def csv_get_rows(filepath):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter="|")
        for i, line in enumerate(reader):
            rows.append(line)
    return rows


def get_latin_name(entity):
    entity_words = entity.capitalize().split('-')
    first_word = entity_words[0]
    rest_words = '-'.join(entity_words[1:])
    latin_name = ' '.join([first_word, rest_words])
    return latin_name


# create articles forlders
rows = csv_get_rows('plants.csv') 
for row in rows[1:num_articles]:
    entity = row[0].strip()
    try: os.makedirs(f'articles/{entity}')
    except: pass
    try: os.makedirs(f'articles/{entity}/medicine')
    except: pass





llm = AutoModelForCausalLM.from_pretrained("llama-2-7b-chat.Q8_0.gguf", model_type="llama")
# llm = AutoModelForCausalLM.from_pretrained("llama-2-13b-chat.Q5_K_M.gguf", model_type="llama", max_new_tokens=512)
# llm = AutoModelForCausalLM.from_pretrained("llama-2-13b-chat.Q8_0.gguf", model_type="llama", max_new_tokens=512)
# llm = AutoModelForCausalLM.from_pretrained("llama-2-7b.Q8_0.gguf", model_type="llama", max_new_tokens=1024)





# rows = csv_get_rows('articles-medicine.csv')

# write content
# def write_sections(section, section_index):
#     rows = csv_get_rows('log-articles-medicine.csv') 
#     for i, row in enumerate(rows[1:num_articles]):
#         print(f'{i}/{num_articles}')
#         entity = row[0].strip()
#         benefits = row[1].strip()
#         constituents = row[2].strip()
#         latin_name = get_latin_name(entity)

#         if row[section_index] != '': continue

#         if section == 'benefits':
#             prompt = f'''
#                 Write a 100 words paragraph on the most important health benefits of {latin_name}.
#                 Pack as much data as possible in as few words as possible.
#                 Don't use lists. 
#                 Don't mention studies.
#                 Don't mention constituents.
#                 Don't write introductory text.
#                 Don't write conclusionary text.
#                 Start the paragraph with the following text: {latin_name} has many health benefits, such as
#             '''
#         elif section == 'constituents':
#             prompt = f'''
#                 Write a 100 words paragraph about the most important constituents of {latin_name} and explain their benefits on health.
#                 Pack as much data as possible in as few words as possible.
#                 Don't use lists. 
#                 Start the paragraph with the following text: The health benefits of {latin_name} are due to its constituents, such as
#             '''
#         elif section == 'preparations':
#             prompt = f'''
#                 Write a 100 words long paragraph about the most important medicinal preparations of {latin_name} and their usage.
#                 Pack as much data as possible in as few words as possible.
#                 Don't use lists. 
#                 Start the paragraph with the following text: The most important medicinal preparations of {latin_name} are 
#             '''

#         print()
#         print(f'{latin_name} - {section}')
#         reply = llm(prompt)
#         print(reply)
#         print()

#         with open(f'articles/{entity}/medicine/{section}.md', 'w', encoding='utf-8') as f:
#             f.write(reply)

def get_lists(section):
    with open(f'medicine-{section}.csv', 'a') as f: pass

    rows = csv_get_rows(f'medicine-{section}.csv') 
    entities_done = [row[0] for row in rows]

    rows = csv_get_rows('plants.csv') 
    for i, row in enumerate(rows[1:num_articles]):
        print(f'{i}/{num_articles}')
        entity = row[0].strip()
        latin_name = get_latin_name(entity)

        if row[0] in entities_done: continue
        
        if section == 'constituents':
            prompt = f'''
                Write a numbered list of the 10 most important medicinal constituents of {latin_name}.
                Don't add descriptions to the medicinal constituents.
                Each medicinal constituents must be less than 5 words.
                Order the medicinal constituents from the most important to the least.
            '''
        if section == 'preparations':
            prompt = f'''
                Write 1 numbered list of the 10 most important medicinal preparations of {latin_name}.
                Write only the list, no supplementary content.
                Don't add descriptions to the medicinal preparations.
                Each medicinal preparations must be 1 to 2 words max.
                Order the list from the most important preparation to the least.
            '''
        if section == 'side-effects':
            prompt = f'''
                List the 10 most common health side effects of {latin_name}.
                Give me only the side effects, don't add descriptions.
            '''

        print(latin_name)
        print()
        reply = llm(prompt)
        print(reply)

        lines = reply.split('\n')

        lines_formatted = []
        for line in lines:
            tmp_line = line.strip()
            if tmp_line == '': continue
            if not tmp_line[0].isdigit(): continue
            tmp_line = ' '.join(tmp_line.split(' ')[1:])
            tmp_line = tmp_line.replace('.', '')
            tmp_line = tmp_line.strip()
            lines_formatted.append([entity, tmp_line])

        with open(f'medicine-{section}.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='|')
            for row in lines_formatted:
                writer.writerow(row)

get_lists('constituents')
get_lists('preparations')
get_lists('side-effects')
quit()

def write_sections(section):
    rows = csv_get_rows('log-articles-medicine.csv') 
    for i, row in enumerate(rows[1:num_articles]):
        print(f'{i}/{num_articles}')
        entity = row[0].strip()
        latin_name = get_latin_name(entity)

        with open(f'articles/{entity}/medicine/{section}.md', 'r', encoding='utf-8') as f:
            content = f.read()
        if content.strip() != '': continue

        if section == 'benefits':
            prompt = f'''
                Write a 100 words paragraph on the most important health benefits of {latin_name}.
                Pack as much data as possible in as few words as possible.
                Don't use lists. 
                Don't mention studies.
                Don't mention constituents.
                Don't write introductory text.
                Don't write conclusionary text.
                Start the paragraph with the following text: {latin_name} has many health benefits, such as
            '''
        elif section == 'constituents':
            prompt = f'''
                Write a 100 words paragraph about the most important constituents of {latin_name} and explain their benefits on health.
                Pack as much data as possible in as few words as possible.
                Don't use lists. 
                Start the paragraph with the following text: The health benefits of {latin_name} are due to its constituents, such as
            '''
        elif section == 'preparations':
            prompt = f'''
                Write a 100 words long paragraph about the most important medicinal preparations of {latin_name}.
                Pack as much data as possible in as few words as possible.
                Don't use lists. 
                Don't use introductory text.
                Start the paragraph with the following text: The most important medicinal preparations of {latin_name} are 
            '''

        print()
        print(f'{latin_name} - {section}')
        reply = llm(prompt)
        print(reply)
        print()

        with open(f'articles/{entity}/medicine/{section}.md', 'w', encoding='utf-8') as f:
            f.write(reply)



write_sections('benefits')
write_sections('constituents')
write_sections('preparations')

quit()

for i, row in enumerate(rows[1:num_articles]):
    entity = row[0].strip()
    # medicine = row[1].strip()
    # cuisine = row[2].strip()
    # horticulture = row[3].strip()

    # if medicine != '': continue

    # print(entity)

    entity_words = entity.capitalize().split('-')
    first_word = entity_words[0]
    rest_words = '-'.join(entity_words[1:])
    latin_name = ' '.join([first_word, rest_words])

    print(latin_name)
    # continue

    prompt = f'''
        Write a numbered list 20 health benefits of {latin_name}.
        Add a verb at the beginning of each benefit.
        Don't use modal verbs (ex. may, can, etc...).
        Don't add descriptions to the benefits.
        Each benefits must be less than 5 words.
        Order the benefits by the most important to the least.
    '''

    
    # prompt = f'''
    #     Write a numbered list the 10 most common culinary uses of {latin_name}.
    #     Don't add descriptions to the culinary uses.
    #     Order the culinary uses by the most common to the least.

    # '''
    
    # prompt = f'''
    #     Write a numbered list the 10 most useful cultivation tips for {latin_name}.
    #     Write every cultivation tip in less than 5 words.
    #     Don't add descriptions to the cultivation tips.
    #     Order the cultivation tips by the most useful to the least.

    # '''

    print()
    print()
    print()
    print(f'Q: {i}/{len(rows[1:])}')
    print()
    print(prompt)
    print()
    print('A:')
    print()
    reply = llm(prompt)
    print(reply)

    lines = reply.split('\n')

    lines_formatted = []
    for line in lines:
        tmp_line = line.strip()
        if tmp_line == '': continue
        if not tmp_line[0].isdigit(): continue
        tmp_line = ' '.join(tmp_line.split(' ')[1:])
        tmp_line = tmp_line.replace('.', '')
        tmp_line = tmp_line.strip()
        lines_formatted.append([entity, tmp_line])

    with open('medicine-benefits.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|')
        for row in lines_formatted:
            writer.writerow(row)

    # entity_num -= 1