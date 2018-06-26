"""
Utilities for working with network-based distances and calculating which
network nodes are within various distance bands of other network nodes
"""




def pairwise(iterable):
    """
    Iterate through a list, pairwise.

    Parameters
    ----------
    iterable : list-like
        the list-like object to iterate through pairwise

    Returns
    -------
    zip
        a zipped iterable of pairwise tuples
    """

    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)



def get_subgraph_nodes(G, node, dists):
    
    subgraph_nodes = {}
    
    for dist1, dist2 in pairwise(dists):
        G_sub = nx.ego_graph(G, node, radius=dist2, distance='length', center=True, undirected=False)
        subgraph_nodes[(dist1, dist2)] = set(G_sub.nodes())
    
    return subgraph_nodes



def get_band_nodes(dists, subgraph_nodes):
    
    band_nodes = {}
    pairwise_dists = list(pairwise(dists))
    
    for idx1, dist_pair1 in reversed(list(enumerate(pairwise_dists))):

        if idx1 < 1:
            break

        dist_pair2 = pairwise_dists[idx1 - 1]
        band_nodes[dist_pair1] = subgraph_nodes[dist_pair1] - subgraph_nodes[dist_pair2]

    band_nodes[pairwise_dists[0]] = subgraph_nodes[pairwise_dists[0]]
    
    return band_nodes
    