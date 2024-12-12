import networkx as nx
import random
import time
import matplotlib.pyplot as plt

def find_dominating_set(graph):
    dominating_set = set()
    uncovered_nodes = set(graph.keys())
    
    while uncovered_nodes:
        # Find the node with the maximum number of uncovered neighbors
        max_cover_node = max(uncovered_nodes, key=lambda node: len(graph[node] & uncovered_nodes))
        # Add this node to the dominating set
        dominating_set.add(max_cover_node)
        # Remove this node and its neighbors from the uncovered nodes
        uncovered_nodes -= graph[max_cover_node] | {max_cover_node}
    
    return dominating_set

def find_dominating_set_local(graph):
    dominating_set = set(graph.nodes())

    while True:
        improved = False
        for node in dominating_set:
            # Try removing the node and check if it's still a dominating set
            new_dominating_set = dominating_set - {node}
            if is_dominating_set(graph, new_dominating_set):
                dominating_set = new_dominating_set
                improved = True
                break  # Move to the next iteration

        if not improved:
            break  # No more improvements possible

    return dominating_set

def is_dominating_set(graph, nodes):
    """Checks if the given set of nodes is a dominating set."""
    covered_nodes = set(nodes)
    for node in nodes:
        covered_nodes.update(graph.neighbors(node))
    return covered_nodes == set(graph.nodes())

# Create a random graph
def create_random_graph(num_nodes, edge_prob):
    graph = {i: set() for i in range(num_nodes)}
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_prob:
                graph[i].add(j)
                graph[j].add(i)
    return graph

# Parameters for the random graph
num_nodes = 10
edge_prob = 0.3

# Generate the random graph
graph = create_random_graph(num_nodes, edge_prob)

# Create a NetworkX graph from the dictionary
G = nx.Graph(graph)
G_local = nx.Graph(graph)

# Measure time for the greedy algorithm
start_time = time.time()
dominating_set = find_dominating_set(graph)
greedy_time = time.time() - start_time

# Measure time for the local search algorithm
start_time = time.time()
dominating_set_local = find_dominating_set_local(G_local)
local_time = time.time() - start_time


print("Time to complete greedy algorithm: {:.6f} seconds".format(greedy_time))
print("Time to complete local search algorithm: {:.6f} seconds".format(local_time))
print("Dominating Set:", dominating_set)
print("Dominating Set Local:", dominating_set_local)

# Draw the first graph
plt.figure(figsize=(12, 6))
plt.subplot(121)
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
# Highlight the dominating set
nx.draw_networkx_nodes(G, pos, nodelist=dominating_set, node_color='red')
plt.title("Dominating Set Greedy")

# Draw the second graph
plt.subplot(122)
pos_local = nx.spring_layout(G_local)
nx.draw(G_local, pos_local, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
# Highlight the dominating set
nx.draw_networkx_nodes(G_local, pos_local, nodelist=dominating_set_local, node_color='blue')
plt.title("Dominating Set Local")

# Show the plots
plt.show()