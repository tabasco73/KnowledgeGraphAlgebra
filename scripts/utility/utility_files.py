import json
import re
import tiktoken

def pretty_json(data, indent=4, level=0, is_last=True):
    lines = []
    ind = ' ' * indent * level

    if isinstance(data, dict):
        lines.append("{")
        items = list(data.items())
        for index, (key, value) in enumerate(items):
            lines.append(ind + ' ' * indent + json.dumps(key) + ":")
            if isinstance(value, (dict, list)):
                lines.extend(pretty_json(value, indent, level + 1, is_last=(index == len(items)-1)))
            else:
                if index == len(items) - 1:
                    lines.append(ind + ' ' * (indent * 2) + json.dumps(value))
                else:
                    lines.append(ind + ' ' * (indent * 2) + json.dumps(value) + ",")
        if not is_last:
            lines.append(ind + "},")
        else:
            lines.append(ind + "}")
    elif isinstance(data, list):
        lines.append("[")
        for index, item in enumerate(data):
            if isinstance(item, (dict, list)):
                lines.extend(pretty_json(item, indent, level + 1, is_last=(index == len(data)-1)))
            else:
                if index == len(data) - 1:
                    lines.append(ind + ' ' * indent + json.dumps(item))
                else:
                    lines.append(ind + ' ' * indent + json.dumps(item) + ",")
        if not is_last:
            lines.append(ind + "],")
        else:
            lines.append(ind + "]")
    else:
        raise ValueError("Data should be a dict or list")

    return lines


def write_answer(string, filename):
    with open(filename, 'w') as f:
        f.write(string)

        
def read_prompt(file_input):
    with open(file_input, 'r') as file:
        data = file.read()
        #print(data)
    return data

def read_json(json_name):
    with open(json_name, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def write_json(content, filename):
    #formatted_data = '\n'.join(pretty_json(content))
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    
def get_the_jsons(max_int, name, start = 0):
    content = []
    for i in range(start, max_int+1):
        content.append(read_json(name + str(i)+'.json'))
    return content

def count_tokens(string_inp):
    encc = tiktoken.encoding_for_model("gpt-4")
    encoded_str = encc.encode(string_inp)
    return len(encoded_str)


def get_actual_id(list_of_ts, nid):
    for a,b,c,d, in list_of_ts:
        if a == nid:
            return b
