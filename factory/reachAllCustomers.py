from factory.graphClasses import *
from heapq import *

def reachAllCustomers(a_graph: Graph, a_potential_factory: Vertex):

    # Check that a_potential_factory is in a_graph
    if a_potential_factory.name not in a_graph.vertices.keys():
        raise KeyError("No existing vertex named {}".format(a_potential_factory.name))

    # Verify a_potential_factory is in fact, a potential factory

    # Raise a special exception if a factory is given
    if a_potential_factory.type == 'F':
        raise TypeError("Can only provide a potential factory, not an existing one!")

    if a_potential_factory.type != 'P':
        raise TypeError("Must supply the name of a potential factory")

    # Pre-processing to find number of customers in entire town
    # Note, not all customers can necessarily be reached from the potential factory
    num_customers = len([1 for val in a_graph.vertices.values() if val.type == "C"])

    # Create a temporary dictionary visited_nodes for the vertex names that have been added to the tree thus far

    # Create a temporary set tree_edges for the edges used in minimum spanning tree

    # Create copy of a_graph's edge set for purposes of finding MST as a min heap

    # Loop: terminate when all edges in a_graph have been encountered

        # Pop edge with the lowest travel cost from the min heap

        # If this current edge connects to a factory
        # or potential factory that is not a_potential_factory, skip

        # If this current edge already connects two vertices in the visited_nodes dictionary, skip

        # Add names of vertices connected by current edge to visited_nodes

        # Add edge to tree_edges

    # Return Graph object representing the minimum spanning subtree of a_graph
    # Create Graph object using visited_nodes and tree_edges

    # This graph connects ONLY a_potential_factory to the customers via mail stations
    # Note that no other factories or potential factories are connected

    pass
