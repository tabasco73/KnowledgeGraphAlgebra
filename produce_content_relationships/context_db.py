from graphviz import Digraph

from utility.utility_files import get_the_jsons, get_actual_id, write_answer
from composition_repair import find_implied_transitive_closure, reduce_morphisms
from utility.utility_db import insert_into_table, get_concepts
from utility.utility_graph import abstract_definitions, node_add, edge_add


def tuple_in_test(list_tup1, list_tup2):
    new_ = []
    for tup1 in list_tup1:
        verd = True
        for tup2 in list_tup2:
            if tup1 == tup2:
                verd = False
                break
        if verd:
            new_.append(tup1)
    return new_

def get_edges():
    i = 180
    content_all = []
    content_all = get_the_jsons(i, 'Contexts/gen',0)
    edges = []
    for k in range(len(content_all)):
        #print(k)
        content_all2 = content_all[k][1][0][1]['Implied_Association_Relationships']
        list_of_ts = content_all[k][0]
        for obj in content_all2:
            spec = get_actual_id(list_of_ts, obj['The_Definition_of_This_Concept'])
            gen =  get_actual_id(list_of_ts, obj['Depends_On_This_Concept'])
            
            if gen != spec and (gen, spec) not in edges:
                edges.append((gen,spec))
                if None in [gen, spec]:
                    print(obj['Explanation'])
                    print((gen, spec))
                #insert_into_table(('gen',gen), ('spec',spec), 'Contexts')
            if gen == spec or (gen, spec) not in edges:
                print(obj['Explanation'])
                print((gen, spec))

    old_edges = edges
    print(len(edges))
    #edges = list(set(find_implied_transitive_closure(edges)))
    print(len(edges))
    #write_answer(str(edges), 'edges.txt')
    #print(len(reduce_morphisms(edges)))
    return edges
    return reduce_morphisms(edges)


def display_it():
    abstr_def_nodes = abstract_definitions(get_concepts())
    all_nodes = abstr_def_nodes
    edges_heritage = get_edges()
    abstr_def_nodes = [a for a in abstr_def_nodes if int(a['Id']) in [item for sublist in edges_heritage for item in sublist]]
    edges_heritage_theorems = []
    edges_belong = []
    edges_own = []
    synonyms = []
    composition_spread = []
    aggs_spread = []
    equiv = []
    dot = Digraph(comment = 'Graphviz Diagram')
    cluster_ids_ = {}
    dot = node_add(dot, abstr_def_nodes, 'lightblue', 'lightblue',cluster_ids_, style = 'filled')
    edge_add(dot, edges_heritage, all_nodes, 'black', arrowtail = 'normal', dir = 'back')
    edge_add(dot, edges_heritage_theorems, all_nodes, 'red', arrowtail = 'normal', dir = 'back')
    edge_add(dot, edges_belong, all_nodes,'black', arrowtail = 'odiamond', dir = 'back')
    edge_add(dot, aggs_spread, all_nodes,'red', arrowtail = 'odiamond', dir = 'back')
    edge_add(dot, equiv, all_nodes, 'black', arrowhead = 'box',arrowtail = 'box', dir = 'both')
    edge_add(dot, synonyms, all_nodes, 'blue', arrowhead = 'box',arrowtail = 'box', dir = 'both')
    edge_add(dot, edges_own, all_nodes, 'black',  arrowtail = 'diamond', dir = 'back')
    edge_add(dot, composition_spread, all_nodes, 'red',  arrowtail = 'diamond', dir = 'back')
    dot.view()