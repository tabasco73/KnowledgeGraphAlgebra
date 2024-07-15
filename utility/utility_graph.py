from graphviz import Digraph


def help_fill(id_, name):
    return {"Id":f"{str(id_)}", "Info": f'ID:{id_} - {name}'}

def abstract_definitions(list_id_names):
    nodes = []
    for id_, name in list_id_names:
        nodes.append(help_fill(id_, name))
    return nodes

def node_add(dot, node_list, color_choice, fill_color,cluster_ids, **kwargs):
    clusters = {}
    for node in node_list:
        node_id = str(node["Id"])

        if node_id in cluster_ids:
            cluster_info = cluster_ids[node_id]
            cluster_name = 'cluster_' + cluster_info['name']
            cluster_color = cluster_info['color']

            if cluster_name not in clusters:
                clusters[cluster_name] = Digraph(name=cluster_name)
                clusters[cluster_name].attr(style='filled', color=cluster_color)
                
            clusters[cluster_name].node(node_id, label=node["Info"], color=color_choice, fillcolor=fill_color, **kwargs)
        else:
            dot.node(node_id, label=node["Info"], color=color_choice, fillcolor=fill_color, **kwargs)

    for cluster in clusters.values():
        dot.subgraph(cluster)

    return dot

def edge_add(dot, edges_heritage, nodes, color_choice, **kwargs):
    nodes = [int(node["Id"]) for node in nodes]
    for start, end in edges_heritage:
        #print(nodes)
        if start in nodes and end in nodes:
            #print(start in nodes)
            dot.edge(str(start), str(end), color=color_choice, **kwargs)
    return dot