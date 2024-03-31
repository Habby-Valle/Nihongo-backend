import json
import uuid

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def create_japanese_dict():
    japanese_dict_list = []

    for i in range(1, 33):
        term_data = load_json(f'core/utils/jmdict_english/term_bank_{i}.json')
        for term in term_data:
            japanese_dict = {}
            japanese_dict['id'] = str(uuid.uuid4())
            japanese_dict['id_term'] = term[6]
            japanese_dict['term'] = term[0]
            japanese_dict['reading'] = term[1]
            japanese_dict['translates'] = term[5]
            japanese_dict['classification'] = term[2]
            japanese_dict['frequency'] = term[4]
            japanese_dict['extra'] = [7]
            japanese_dict['extra_II'] = [3]

            japanese_dict_list.append(japanese_dict)
    japanese_dict_list.sort(key=lambda x: x['term'])
    
    return japanese_dict_list