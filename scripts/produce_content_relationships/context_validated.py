import json
import time

from scripts.utility.openai_request import query_openai_with_function_calling
from scripts.utility.utility_openai import function_call_fill, count_tokens
from scripts.utility.utility_db import get_edges_db2, get_concept

def validate_an_inh():
    functions = function_call_fill('Functioncalls/Check_Reasoning.json')
    rows = get_edges_db2()
    syst = 'You are a concept validator. I will provide you with a question and you will provide an explanation of whether it is true or false, together with a verdict.'
    inputtuplist = []
    for a,b,c  in rows:
        info_a = get_concept(b)
        info_b = get_concept(c)
        info_a = info_a[0]
        info_b = info_b[0]
        question = 'Does the concept of a/an ' + info_a[0] + ' need to be defined for a definition of a/an ' + info_b[0] + ' to make sense? (True if the first concept is needed and False if is not.)'
        prompt = question + '\n\nThese are the definitions of the concepts:\n"""\nConcept: ' + info_b[0] + '\nDefinition:\n' + info_b[1] + '\n\nConcept: ' + info_a[0] + '\nDefinition:\n' + info_a[1] + '\n"""'
        inputtuplist.append(([a,info_a,info_b, question], prompt))
    #30, i 1
    #inputtuplist = inputtuplist[565:]
    print(len(inputtuplist))
    #print(inputtuplist[0])
    #x = 60
    #inputtuplist = inputtuplist[x:]
    inputtuplist = [(i, prompt) for i, prompt in inputtuplist if i[0] in [1017]]
    #print(len(inputtuplist))
    #print(inputtuplist)
    if inputtuplist != []:
        start_time = time.time()

        for i, prompt in inputtuplist:
            
            #print(count_tokens(prompt))
            #return
            try:
                sample_response = query_openai_with_function_calling(syst, prompt, functions, {"name": "Validity_Check"}, 'gpt-4-turbo')
                resultjson = [i, sample_response]
            
                with open(r"data/ValidateGensContext/" + f'check{i[0]}.json', "w") as json_file:
                    json.dump(resultjson, json_file, indent=4)
                #print(i)
            except Exception as e:
                #print(e)
                print(i[0])
                print(prompt)
                print('________________________\n\n\n')
                #print(resultjson)
                continue
        end_time = time.time()

    execution_time = end_time - start_time
    print(f"The function took {execution_time} seconds to execute.")


