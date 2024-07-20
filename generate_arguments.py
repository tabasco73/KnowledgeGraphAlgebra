import os
import sqlite3

from scripts.category_theory.composition_repair import find_implied_transitive_closure, reduce_morphisms
from scripts.utility.utility_db import get_concept
from dotenv import load_dotenv
load_dotenv()
DB_PATH = os.getenv('DB_PATH')


def find_configurations(set_1, set_2):
    configurations = []

    # Convert lists of tuples to dictionaries for faster lookup
    set_1_dict = {edge: 1 for edge in set_1}
    set_2_dict = {edge: 1 for edge in set_2}

    # Iterate through all possible node combinations
    for (A, B) in set_1_dict:
        for (C, D) in set_1_dict:
            if A != C and B != D:  # Ensuring nodes are different
                if (A, C) in set_2_dict and (B, D) in set_2_dict:
                    configurations.append({
                        'SET_1': [(A, B), (C, D)],
                        'SET_2': [(A, C), (B, D)]
                    })
    return configurations


def get_edges2():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT gen, spec, validation FROM Inheritances")
    rows = cursor.fetchall()
    conn.close()
    rows = [(a,b) for a,b,c in rows if c == 1]
    rows += [(145,26),(145,6),(6,11),(11,26),(146,14),(33,104),(11,134),(26,29),(11,72),(58,59),(13,129),(132,133),(63,48),(33,66)]
    rows += find_implied_transitive_closure(rows)
    inheritances = reduce_morphisms(rows)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT gen, spec, validation FROM Contexts")
    rows = cursor.fetchall()
    conn.close()
    #rows = fix(rows, rows2)
    rows = [(a,b) for a,b,c in rows if c == 1]
    print(len(rows))
    print(len(find_implied_transitive_closure(rows)))
    print(len(reduce_morphisms(find_implied_transitive_closure(rows) + rows)))
    edges = reduce_morphisms(find_implied_transitive_closure(rows) + rows)

    analogies = find_configurations(inheritances, edges)
    for analogy in analogies:
        name_sources = []
        name_targets = []
        for edge in analogy['SET_1']:
            print(f'{edge=}')
            source = edge[0]
            target = edge[1]
            source = get_concept(source)[0]
            name_s_1 = source[0]
            name_sources.append(name_s_1)
            content_s = source[1]
            
            target = get_concept(target)[0]
            name_t_1 = target[0]
            name_targets.append(name_t_1)
            content_t = target[1]

        for edge in analogy['SET_2']:
            #print(f'{nodes=}')
            source = edge[0]
            target = edge[1]
            source = get_concept(source)[0]
            name_s_2 = source[0]
            content_s= source[1]

            target = get_concept(target)[0]
            name_t_2 = target[0]
            content_t = target[1]
        print(f'A/an {name_targets[0]} is to a/an {name_targets[1]} what a/an {name_sources[0]} is to a/an {name_sources[1]}')
        print(analogy)
    print(len(analogies))
    




get_edges2()