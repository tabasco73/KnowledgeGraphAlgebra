import os
import sqlite3

from graphviz import Digraph
from scripts.category_theory.composition_repair import find_implied_transitive_closure, reduce_morphisms
from scripts.utility.utility_db import get_concepts, update_column_for_row_at_id
from scripts.utility.utility_files import get_the_jsons, write_answer
from scripts.utility.utility_graph import abstract_definitions, edge_add, node_add

from dotenv import load_dotenv
load_dotenv()
DB_PATH = os.getenv('DB_PATH')

def display_info(data):
    def print_algebraic_info(info_list, depth=0):
        indent = "  " * depth
        if isinstance(info_list[0], int):
            depth, *content = info_list
            for item in content:
                if isinstance(item, list):
                    title, description = item
                    print(f"{indent}Title: {title}\n")
                    print(f"{indent}Description: {description}\n")
                else:
                    print(f"{indent}Question: {item}\n")
        elif isinstance(info_list[0], list) and info_list[0][0] == "Validity_Check":
            check_type, check_content = info_list[0]
            explanation = check_content.get("Explanation", "")
            verdict = check_content.get("Verdict", "")
            print(f"{indent}Validity Check Explanation:\n{explanation}\n")
            print(f"{indent}Verdict: {'True' if verdict else 'False'}\n")
        else:
            for item in info_list:
                if isinstance(item, list):
                    print_algebraic_info(item, depth + 1)

    for info in data:
        print_algebraic_info(info)




def get_gens():
    i = 1472
    init = 1
    content_all = []
    content_all = get_the_jsons(i, 'data/ValidateGensContext/check',init)
    edges = []
    verdicts = []

    for k in range(len(content_all)):
        print()
        verdict = content_all[k][1][0][1]['Verdict']
        id_ = content_all[k][0][0]
        explanation = content_all[k][1][0][1]['Explanation']
        verdict_integer = 1 if verdict else 0
        
        print(id_)
        
        update_column_for_row_at_id('Contexts' ,id_,('validation_reasoning',explanation))
        update_column_for_row_at_id('Contexts' ,id_,('validation',verdict_integer))
        #print(f"{k+init}!!!!!")
        #display_info(content_all[k])
        #print(f"{k+init}!!!!!")
        #if input("Okay? (y/n): ") == "n":
        #    write_answer(str(k+1)+'\n','check.txt')
    return edges


def get_edges():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT gen, spec, validation FROM Inheritances")
    rows = cursor.fetchall()
    conn.close()
    #rows = fix(rows, rows2)
    rows = [(a,b) for a,b,c in rows if c == 1]
    rows += [(145,26),(145,6),(6,11),(11,26),(146,14),(33,104),(11,134),(26,29),(11,72),(58,59),(13,129),(132,133),(63,48),(33,66)] + [(143, 95),(143, 70),(143, 102),(143, 62),(143, 80),(143, 10),(143,9)] + [(146,135),(11,40),(124,85),(11,124),(11,26)]
    print(len(rows))
    print(len(find_implied_transitive_closure(rows)))
    print(len(reduce_morphisms(find_implied_transitive_closure(rows) + rows)))
    before = find_implied_transitive_closure(rows) + rows

    #return before
    return reduce_morphisms(before)
    rows2 = ''
    all_ = [a for a in rows+rows2 if a not in []]
    reduced = reduce_morphisms(rows+rows2)
    return rows+rows2

def get_edges2():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT gen, spec, validation FROM Contexts")
    rows = cursor.fetchall()
    conn.close()
    #rows = fix(rows, rows2)
    rows = [(a,b) for a,b,c in rows if c == 1]
    #rows += [(145,26),(145,6),(6,11),(11,26),(146,14),(33,104),(11,134),(26,29),(11,72),(58,59),(13,129),(132,133),(63,48),(33,66)]
    print(len(rows))
    print(len(find_implied_transitive_closure(rows)))
    print(len(reduce_morphisms(find_implied_transitive_closure(rows) + rows)))

    before = find_implied_transitive_closure(rows) + rows
    #return before
    return reduce_morphisms(before)
    rows2 = ''
    all_ = [a for a in rows+rows2 if a not in []]
    rows3 = reduce_morphisms(rows+rows2)
    return rows+rows2

def display_it():
    abstr_def_nodes = abstract_definitions(get_concepts())
    all_nodes = abstr_def_nodes
    edges_heritage = get_edges()
    edges_belong = get_edges2()
    abstr_def_nodes = [a for a in abstr_def_nodes if int(a['Id']) in [item for sublist in edges_heritage+edges_belong for item in sublist]]
    #abstr_def_nodes = [a for a in abstr_def_nodes if int(a['Id']) in [item for sublist in edges_heritage for item in sublist]]
    edges_heritage_theorems = []
    #edges_belong = []
    edges_own = []
    synonyms = []
    composition_spread = []
    aggs_spread = []
    equiv = []
    dot = Digraph(comment = 'Graphviz Diagram')
    cluster_ids_ = {}
    dot = node_add(dot, abstr_def_nodes, 'lightblue', 'lightblue',cluster_ids_, style = 'filled')
    edge_add(dot, edges_heritage, all_nodes, 'red', arrowtail = 'normal', dir = 'back')
    edge_add(dot, edges_heritage_theorems, all_nodes, 'red', arrowtail = 'normal', dir = 'back')
    edge_add(dot, edges_belong, all_nodes,'blue', arrowtail = 'odiamond', dir = 'back')
    edge_add(dot, aggs_spread, all_nodes,'red', arrowtail = 'odiamond', dir = 'back')
    edge_add(dot, equiv, all_nodes, 'black', arrowhead = 'box',arrowtail = 'box', dir = 'both')
    edge_add(dot, synonyms, all_nodes, 'blue', arrowhead = 'box',arrowtail = 'box', dir = 'both')
    edge_add(dot, edges_own, all_nodes, 'black',  arrowtail = 'diamond', dir = 'back')
    edge_add(dot, composition_spread, all_nodes, 'red',  arrowtail = 'diamond', dir = 'back')
    dot.view()