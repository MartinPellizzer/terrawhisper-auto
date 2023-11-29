import csv
import os
import re
from ctransformers import AutoModelForCausalLM


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


llm = AutoModelForCausalLM.from_pretrained("mistral-7b-instruct-v0.1.Q8_0.gguf", model_type="mistral", max_new_tokens=1024, context_length=1024)
# llm = AutoModelForCausalLM.from_pretrained("zephyr-7b-beta.Q8_0.gguf", model_type="mistral")

num_articles = 10

def write_section(section):
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:num_articles+1]):
        print(f'{i+1}')
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        try: os.makedirs(f'database')
        except: pass
        try: os.makedirs(f'database/articles')
        except: pass
        try: os.makedirs(f'database/articles/{entity}')
        except: pass

        try:
            with open(f'database/articles/{entity}/{section}.md', 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            content = ''
        if content.strip() != '': continue
        
        if section == 'medicine':
            prompt = f'''
                Write 5 paragraphs about the medicinal aspect {common_name} ({latin_name}).
                In paragraph 1, write about the health benefits and health conditions this plant helps (don't mention constituents in this paragraph).
                In paragraph 2, write about the medicinal constituents.
                In paragraph 3, write about the most used parts and medicinal preparations.
                In paragraph 4, write about the possible side effects.
                In paragraph 5, write about the precautions.
                Include as much data as possible in as few words as possible.
                Include only proven data.
                Don't write lists.
            '''
        elif section == 'cuisine':
            prompt = f'''
                Write 5 paragraphs about the culinary aspect of {common_name} ({latin_name}).
                In paragraph 1, write about the culinary uses.
                In paragraph 2, write about the flavor profile.
                In paragraph 3, write about the edible parts.
                In paragraph 4, write about the culinary tips.
                In paragraph 5, write about the possible side effects and toxicity.
                Include as much data as possible in as few words as possible.
                Don't include medicinal aspects.
                Don't write lists.
            '''
        elif section == 'horticulture':
            prompt = f'''
                Write 3 paragraphs about the horticultural aspect of {common_name} ({latin_name}).
                In paragraph 1, write about how to grow this plant.
                In paragraph 2, write about the ideal growing conditions.
                In paragraph 3, write about the maintenance.
                Include as much data as possible in as few words as possible.
                Use the metric system.
                Don't write lists.
            '''
        elif section == 'botany':
            prompt = f'''
                Write 5 paragraphs about the botanical aspect of {common_name} ({latin_name}).
                In paragraph 1, tell me the taxonomy, including domain, kingdom, phylum, class, order, family, genus, species. Then, tell me the common names.
                In paragraph 3, tell me the morphology.
                In paragraph 2, tell me the variants names and their differences.
                In paragraph 4, tell me the geographic distribution and natural habitats.
                In paragraph 5, tell me the life-cycle.
                Include as much data as possible in as few words as possible.
                Don't write lists.
            '''
        elif section == 'history':
            prompt = f'''
                Write 3 paragraphs about the historical aspect of {common_name} ({latin_name}).
                In paragraph 1, write about the traditional medicine.
                In paragraph 2, write about the uses in divination.
                In paragraph 3, write about the legends.
                Include as much data as possible in as few words as possible.
                Don't write lists.
            '''
        
        print()
        print("Q:")
        print()
        print(prompt)
        print()
        print("A:")
        print()
        prompt = prompt.strip()
        prompt = re.sub("\s\s+", " ", prompt)
        reply = ''
        for text in llm(prompt, stream=True):
            reply += text
            print(text, end="", flush=True)
        print()

        reply = reply.strip()

        lines = reply.split('\n')

        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line.strip().endswith(':'): continue
            if ':' in line: line = line.split(':')[1]
            if line[0].isdigit(): line = ' '.join(line.split(' ')[1:])
            lines_formatted.append(line)
        
        reply = '\n\n'.join(lines_formatted)

        with open(f'database/articles/{entity}/{section}.md', 'w', newline='', encoding='utf-8') as f:
            f.write(reply)

write_section('medicine')
write_section('cuisine')
write_section('horticulture')
write_section('botany')
write_section('history')

quit()

prompt = '''
Write 5 paragraphs about the medicinal aspect of yarrow (Achillea millefolium).
In paragraph 1, write about the health benefits, medicinal properties, and health conditions this plant helps.
In paragraph 2, write about the medicinal constituents.
In paragraph 3, write about the most used parts and medicinal preparations.
In paragraph 4, write about the possible side effects.
In paragraph 5, write about the precautions.
Write as much info as possible in as few words as possible.
Include data, numbers, and percentages.
Don't use modal verbs.
Separate the paragraphs with a new line.
'''

# print(llm(prompt))

tot_text = ''
for text in llm(prompt, stream=True):
    tot_text += text
    print(text, end="", flush=True)

print()
print()
print(tot_text)
quit()


try: os.makedirs(f'database')
except: pass
try: os.makedirs(f'database/articles')
except: pass
try: os.makedirs(f'database/articles/{entity}')
except: pass

with open(f'database/articles/{entity}/medicine.md', 'a', newline='', encoding='utf-8') as f:
    f.write(reply)


num_articles = 10
# num_articles = 999

def write_list(section):
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:]):
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        tmp_rows = csv_get_rows(f'database/medicine-{section}.csv')
        tmp_entities = [tmp_row[0] for tmp_row in tmp_rows]
        if entity in tmp_entities: continue 
        # print(tmp_rows)

        # quit()
        
        print(f'{i}/{num_articles}')

        if section == 'benefits':
            prompt = f"""
                Write a numbered list of the 10 most important health benefits of {common_name} ({latin_name}).
                Start each health benefit with a third-person singular verb.
                Write only the health benefits, don't add descriptions.
                Write each health benefit in less than 5 words.
                Write each health benefit in a new line.
            """
        elif section == 'constituents':
            prompt = f"""
                Write a numbered list of the 10 most important medicinal constituents of {common_name} ({latin_name}).
                Don't add descriptions.
                Write each medicinal constituents in less than 5 words.
                Write each medicinal constituent in a new line.
            """
        elif section == 'preparations':
            prompt = f"""
                Write a numbered list of the 10 most important medicinal preparations of {common_name} ({latin_name}).
                Start each medicinal preparations with "{common_name}".
                Write only the medicinal preparations, don't add descriptions.
                Write each medicinal preparation in less than 5 words.
                Write each medicinal preparation in a new line.
            """
        elif section == 'side-effects':
            prompt = f"""
                Write a numbered list of the 10 most common side effects of using {common_name} ({latin_name}) for medicinal purposes.
                Start each side effects with a third-person singular verb.
                Write only the side effects, don't add descriptions.
                Write each side effect in less than 5 words.
                Write each side effect in a new line.
            """
        elif section == 'precautions':
            prompt = f"""
                Write a numbered list of the 10 most important precautions to take when using {common_name} ({latin_name}) for medicinal purposes.
                Write only the precautions, don't add descriptions.
                Write each precaution in less than 5 words.
                Write each precaution in a new line.
            """
        
        print()
        print("Q:")
        print()
        print(prompt)
        print()
        print("A:")
        print()
        reply = llm(prompt)
        print(reply)
        print()
        print('------------------------------------------------')

        lines = reply.split('\n')

        lines_formatted = []
        for line in lines:
            tmp_line = line.strip()
            if tmp_line == '': continue
            if not tmp_line[0].isdigit(): continue
            tmp_line = ' '.join(tmp_line.split(' ')[1:])
            tmp_line = tmp_line.replace('.', '')
            tmp_line = tmp_line.strip()
            tmp_line = tmp_line.split(':')[0]
            tmp_line = tmp_line.split(' - ')[0]
            lines_formatted.append([entity, tmp_line])

        with open(f'database/medicine-{section}.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='|')
            for line in lines_formatted:
                writer.writerow(line)

write_list('benefits')
write_list('constituents')
write_list('preparations')
write_list('side-effects')
write_list('precautions')


def write_text(section):
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:num_articles]):
        print(f'{i}')
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)
        
        # try:
        #     with open(f'database/articles/{entity}/{section}.md', 'r', encoding='utf-8') as f:
        #         content = f.read()
        # except: 
        #     content = ''
        # if content.strip() != '': continue

        benefits = csv_get_rows(f'database/medicine-benefits.csv')
        benefits = [f'{row[1].lower()}' for row in benefits if row[0] == entity] 
        benefits = ', '.join(benefits)
        
        constituents = csv_get_rows(f'database/medicine-constituents.csv')
        constituents = [f'{row[1].lower()}' for row in constituents if row[0] == entity] 
        constituents = ', '.join(constituents)

        if section == 'benefits':
            prompt = f"""
                Write a 100 words paragraph for an article about the benefits of {common_name} ({latin_name}), such as {benefits}.
                Don't write lists. 
                Include numbers, values, and percentages.
                Pack as much info as possible in as few words as possible.
            """
        elif section == 'constituents':
            prompt = f"""
                Write a paragraph about the key constituents of {common_name} ({latin_name}) in less than 100 words.
                Include {constituents}.
                Include as much numbers, values, and percentages as possible in as few words as possible.
                Don't write lists.
                Don't write benefits and properties.
                
            """
        # Write only about what the constituents are, not what they do.
        #         Don't mention studies.
        
        print()
        print("Q:")
        print()
        print(prompt)
        print()
        print("A:")
        print()
        prompt = prompt.strip()
        prompt = re.sub("\s\s+", " ", prompt)
        reply = llm(prompt)
        print(reply)
        print()
        print('------------------------------------------------')

        reply = reply.strip()

        try: os.makedirs(f'database')
        except: pass
        try: os.makedirs(f'database/articles')
        except: pass
        try: os.makedirs(f'database/articles/{entity}')
        except: pass
        try: os.makedirs(f'database/articles/{entity}/medicine')
        except: pass

        # with open(f'database/articles/{entity}/{section}.md', 'a', newline='', encoding='utf-8') as f:
        #     f.write(reply)

# write_text('benefits')
write_text('constituents')