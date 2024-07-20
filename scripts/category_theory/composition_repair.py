import unittest
from collections import defaultdict
import networkx as nx

def find_implied_transitive_closure(morphisms):
    adjacency_list = defaultdict(set)
    for src, tgt in morphisms:
        adjacency_list[src].add(tgt)

    changes = True
    while changes:
        changes = False
        new_edges = defaultdict(set)
        for src in list(adjacency_list):
            for mid in list(adjacency_list[src]):
                for tgt in adjacency_list[mid]:
                    if tgt not in adjacency_list[src] and src != tgt:
                        new_edges[src].add(tgt)
                        changes = True
        for src in new_edges:
            adjacency_list[src].update(new_edges[src])
    
    original_set = set(morphisms)
    all_morphisms = set((src, tgt) for src, targets in adjacency_list.items() for tgt in targets)
    implied_morphisms = all_morphisms - original_set

    return list(implied_morphisms)


def reduce_morphisms(morphisms):
    G = nx.DiGraph()
    G.add_edges_from(morphisms)
    
    redundant_edges = []
    for (u, v) in morphisms:
        G.remove_edge(u, v)
        if nx.has_path(G, u, v):
            redundant_edges.append((u, v))
        G.add_edge(u, v)
    for edge in redundant_edges:
        G.remove_edge(*edge)
    
    return list(G.edges)


class TestTransitiveClosure(unittest.TestCase):
    def test_simple_chain(self):
        morphisms = [('A', 'B'), ('B', 'C')]
        expected = {('A', 'C')}
        result = find_implied_transitive_closure(morphisms)
        self.assertEqual(result, expected)

    def test_longer_chain(self):
        morphisms = [('A', 'B'), ('B', 'C'), ('C', 'D')]
        expected = {('A', 'C'), ('B', 'D'), ('A', 'D')}
        result = find_implied_transitive_closure(morphisms)
        self.assertEqual(result, expected)

    def test_branching(self):
        morphisms = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
        expected = {('A', 'D')}
        result = find_implied_transitive_closure(morphisms)
        self.assertEqual(result, expected)

    def test_cycle(self):
        morphisms = [('A', 'B'), ('B', 'C'), ('C', 'A')]
        expected = {('A', 'C'), ('B', 'A'), ('C', 'B')}
        result = find_implied_transitive_closure(morphisms)
        self.assertEqual(result, expected)

    def test_no_new_morphisms(self):
        morphisms = [('A', 'B'), ('C', 'D')]
        expected = set()
        result = find_implied_transitive_closure(morphisms)
        self.assertEqual(result, expected)

    def test_redundant_direct(self):
        morphisms = [('A', 'B'), ('B', 'C'), ('A', 'C')]
        expected = set()
        result = find_implied_transitive_closure(morphisms)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
    morphisms = [('A', 'B'), ('B', 'C'), ('A', 'C'), ('C', 'D'), ('A', 'D')]
    reduced_morphisms = reduce_morphisms(morphisms)
    print("Original Morphisms:", morphisms)
    print("Reduced Morphisms:", reduced_morphisms)