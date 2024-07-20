import os
import sqlite3
import json

from scripts.combinatorial_algorithm.combine import swap_all_integers_n
from scripts.utility.openai_request import query_openai_with_function_calling
from scripts.utility.utility_db import get_the_concept_ids
from scripts.utility.utility_openai import function_call_fill, count_tokens

from dotenv import load_dotenv
load_dotenv()
DB_PATH = os.getenv('DB_PATH')

def get_contexts(m, uppsättning):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, content FROM Definitioner")
    rows = cursor.fetchall()
    conn.close()
    rows = [(a,b,c) for a,b,c in rows if a in uppsättning]
    functions = function_call_fill('Functioncalls/Implied_Association.json')
    syst = 'You are an expert in analysing the nature of concepts, specifically within abstract algebra. Your goal is to provide an exhaustive mapping of the relationships between the given concepts.\n You will focus on identifying relationships where one concepts definition is dependent on the other. I.e. one concept has to be defined for the definition of the other to defined.'
    prompt = ' Here are the concepts:\n\n'
    
    keys = []
    for j, (a,b,c) in enumerate(rows):
        prompt += 'ID: '+str(j)+'\nName: '+ b + '\n\nDefinition: '+ c + '\n\n__\n\n'
        keys += [(j, a, b, c)]
    print(f'{syst=}')
    print(f'{prompt=}')
    inputtuplist = [(keys, prompt)]
    if inputtuplist != []:
        for i, prompt in inputtuplist:
            print(prompt)
            print(count_tokens(prompt))
            #return
            sample_response = query_openai_with_function_calling(syst, prompt, functions, {"name": "Definition_Association_Analysis"}, 'gpt-4-turbo')
            resultjson = [i, sample_response]
            print(resultjson)
            with open(r"Contexts/" + f'gen{m}.json', "w") as json_file:
                json.dump(resultjson, json_file, indent=4)
            print(i)

def prompt_through_all_insikter():
    primtal = [2,3,5,7,11,13,17,19,23,29,31,37,41]

    numbers = get_the_concept_ids()
    for prime in primtal:
        if len(numbers) > prime**2:
            ''
        else:
            n = prime
            break
    #print(n)
    zeros = [0 for i in range(n*n -len(numbers))]
    numbers += zeros
    uppsättningar = swap_all_integers_n(numbers, n)
    uppsättningar2 = []
    for a in uppsättningar:
        if not(a.count(0) == len(a)):
            uppsättningar2.append(a)
    return uppsättningar2
    
def run_contexts():
    uppsättningar = prompt_through_all_insikter()
    print(len(uppsättningar))
    for i, a in enumerate(uppsättningar):
        
        if i in [135,139,136]:
            get_contexts(i, a)

if __name__ =='__main__':
    run_contexts()