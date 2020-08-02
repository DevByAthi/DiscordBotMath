from factory.generateGraph import *
from factory.graphClasses import *
from heapq import *

def reachAllCustomers(a_graph: Graph, a_potential_factory: Vertex):

    # Check that a_potential_factory is in a_graph
    if a_potential_factory.name not in a_graph.vertices.keys():
        ret = "No existing vertex named {}".format(a_potential_factory.name)
        raise KeyError()

    verify_type(a_potential_factory)

    # Pre-processing to find number of customers in entire town
    # Note, not all customers can necessarily be reached from the potential factory
    num_customers = len([1 for val in a_graph.vertices.values() if val.type == "C"])

    # Create a temporary dictionary visited_nodes for the vertex names that have been added to the tree thus far
    visited_nodes = dict()

    # Create a temporary set tree_edges for the edges used in minimum spanning tree
    tree_edges = set()

    # Create copy of a_graph's edge set for purposes of finding MST as a min heap
    remaining_edges = list(a_graph.edges)
    heapify(remaining_edges)

    # Loop: terminate when all edges in a_graph have been encountered
    while len(remaining_edges) > 0:

        # Pop edge with the lowest travel cost from the min heap
        cur_edge = heappop(remaining_edges)
        v1, v2 = tuple(cur_edge.pair)

        # If this current edge connects to a factory
        # or potential factory that is not a_potential_factory, skip
        if a_graph.vertices[v1].type == 'F' or a_graph.vertices[v2].type == 'F':
            continue
        elif a_graph.vertices[v1].type == 'P' and a_graph.vertices[v1].name != a_potential_factory.name:
            continue
        elif a_graph.vertices[v2].type == 'P' and a_graph.vertices[v2].name != a_potential_factory.name:
            continue

        # If this current edge already connects two vertices in the visited_nodes dictionary, skip
        if v1 in visited_nodes.keys() and v2 in visited_nodes.keys():
            continue

        # Add names of vertices connected by current edge to visited_nodes
        visited_nodes[v1] = a_graph.vertices[v1]
        visited_nodes[v2] = a_graph.vertices[v2]

        # Add edge to tree_edges
        tree_edges.add(cur_edge)

    print(visited_nodes)
    print(tree_edges)
    # Return Graph object representing the minimum spanning subtree of a_graph
    # Create Graph object using visited_nodes and tree_edges
    return Graph(vertices=visited_nodes, edges=tree_edges)

    # This graph connects ONLY a_potential_factory to the customers via mail stations
    # Note that no other factories or potential factories are connected


def verify_type(a_potential_factory):
    # Verify a_potential_factory is in fact, a potential factory
    # Raise a special exception if a factory is given
    if a_potential_factory.type == 'F':
        raise TypeError("Can only provide a potential factory, not an existing one!")
    if a_potential_factory.type != 'P':
        raise TypeError("Must supply the name of a potential factory")


# Prim's Algorithm solution
def prims_algorithm(a_graph: Graph, name):
    # Check that a_potential_factory is in a_graph
    if name not in a_graph.vertices.keys():
        ret = "No existing vertex named {}".format(name)
        raise KeyError()

    a_potential_factory = a_graph.vertices[name]

    verify_type(a_potential_factory)

    a_graph.resetDistances()

    a_potential_factory.distanceValue = 0

    current_vertex_name = name

    # Create a temporary dict for the vertex names that have been added to the tree
    # The value represents the name of key's predecessor in MST, if any
    visited_vertices = {current_vertex_name: None}

    # Create min-heap for selecting next vertex on frontier by total travel cost
    name_queue = [(0, current_vertex_name)]

    # This loop terminates when the minimum spanning tree cannot be further expanded
    while not(len(name_queue) == 0):

        # Update current_vertex_name
        current_travel_cost, current_vertex_name = heappop(name_queue)

        # Retrieve Current Vertex
        current_vertex = a_graph.vertices[current_vertex_name]

        # Find neighbors of current node
        neighbors = a_graph.alt_lookup[current_vertex_name]

        # Iterate through each neighbor
        for neighbor_name in neighbors.keys():

            # TODO: If type of the neighbor is a factory or a potential factory, skip

            travel_cost = neighbors[neighbor_name]

            neighbor_vertex = a_graph.vertices[neighbor_name]

            # If type of the neighbor is a factory or a potential factory, skip
            if neighbor_vertex.type == 'F' or neighbor_vertex.type == 'P':
                continue

                    heappush(name_queue, (neighbor_vertex.distanceValue, neighbor_name))

            # If the neighbor has not yet been visited, add to visited_vertices
            else:
                # Update shortest distance to this neighbor
                neighbor_vertex.distanceValue = current_travel_cost + travel_cost
                # Mark current vertex as predecessor of neighbor in MST
                visited_vertices[neighbor_name] = current_vertex_name

                heappush(name_queue, (neighbor_vertex.distanceValue, neighbor_name))

    # Using a_graph lookup table, a_graph vertices dictionary, and visited_vertices,
    # create a Graph representing the MST of a_graph, excluding factories and other potential factories

    print("Visited: ", visited_vertices)
    return True


if __name__ == '__main__':
    s = readFileIntoString('graph2.txt')
    g = parse_into_graph(s)
    mst = prims_algorithm(g, 'Newtown_Factory_potential')

    '''# Check that non-existent vertex names will not be accepted
    try:
        reachAllCustomers(g, g.vertices['ASDF'])
    except KeyError as err:
        print(err)

    # Check that existing factories will not be accepted
    try:
        reachAllCustomers(g, g.vertices['Farmfresh_Chocolate'])
    except TypeError as err:
        print(err)

    print(mst.alt_lookup)
    '''
