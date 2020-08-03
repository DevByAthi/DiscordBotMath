from factory.generateGraph import *
from factory.graphClasses import *
from heapq import *


def verify_type(a_potential_factory):
    # Verify a_potential_factory is in fact, a potential factory
    # Raise a special exception if a factory is given
    if a_potential_factory.type == 'F':
        raise TypeError("Can only provide a potential factory, not an existing one!")
    if a_potential_factory.type != 'P':
        raise TypeError("Must supply the name of a potential factory")


def parse_mst_dict(customer_paths: dict):
    return [" \u27F6 ".join(customer_paths[key]) for key in customer_paths.keys()]


def get_paths_to_customers(a_graph: Graph, visited: dict):
    visited_customers = [node for node in visited.keys()
                         if node in a_graph.vertices.keys()
                         and a_graph.vertices[node].type == 'C']

    all_customer_paths = dict()

    for customer in visited_customers:
        path = []
        current = customer
        while current is not None:
            path.append(current)
            current = visited[current]
        path.reverse()
        all_customer_paths[customer] = path[:]
    return all_customer_paths


# Prim's Algorithm solution
'''
    :param a_graph: A Graph object representing a town
    :param name: the name of a potential factory site listed in a_graph
    :return: a dictionary relating to each customer reachable from `name` the sequences of locations to visit
'''
def prims_algorithm(a_graph: Graph, name):
    # PRECONDITION: a_graph has a non-empty vertex set
    # PRECONDITION: name is the name of exactly one of the vertices of a_graph
    # PRECONDITION: all edges in a_graph are nonnegative
    # INVARIANT: the vertex set and edge set of a_graph are both constant and unchanged
    # POSTCONDITION: the vertex represented by name is the root of a minimum spanning tree of a_graph
    # POSTCONDITION: the returned dict has the names of customers reachable from the vertex represented by name as keys
    #                (these customers are henceforth, "reachable customers")
    # POSTCONDITION: the returned dictionary stores a path from the vertex represented by name
    #                to each reachable customer as values


    # Check that a_potential_factory is in a_graph
    if name not in a_graph.vertices.keys():
        ret = "No existing vertex named `{}`".format(name)
        raise TypeError(ret)

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

    # Sa: name_queue is a min-heap with all vertices on the frontier in a_graph

    # [Sb] Greed used: Every iteration improves the upper bound on the distance
    # from the the vertex represented by name to another vertex in a_graph

    # This loop terminates when the frontier cannot be further expanded,
    # and thus when the minimum spanning tree has been acquired
    while not (len(name_queue) == 0):

        # Update current_vertex_name
        current_travel_cost, current_vertex_name = heappop(name_queue)

        # Retrieve Current Vertex
        current_vertex = a_graph.vertices[current_vertex_name]

        # Find neighbors of current vertex
        neighbors = a_graph.alt_lookup[current_vertex_name]

        # Iterate through each neighbor
        for neighbor_name in neighbors.keys():

            travel_cost = neighbors[neighbor_name]
            neighbor_vertex = a_graph.vertices[neighbor_name]

            # If type of the neighbor is a factory or a potential factory, skip
            if neighbor_vertex.type == 'F' or neighbor_vertex.type == 'P':
                continue

            # Lambda function to determine if current distance to vertex can be further minimized
            can_be_minimized = lambda a_vertex: a_vertex.distanceValue > current_travel_cost + travel_cost

            # If the neighbor has not yet been visited,
            # or its distance can be minimized
            # update the vertex's distanceValue, add vertex to MST, and add vertex to queue accordingly
            if neighbor_name not in visited_vertices.keys() or can_be_minimized(neighbor_vertex):
                # Update shortest distance to this neighbor
                neighbor_vertex.distanceValue = current_travel_cost + travel_cost
                # Mark current vertex as predecessor of neighbor in MST, updating the tree
                visited_vertices[neighbor_name] = current_vertex_name
                # Add updated neighbor to queue
                heappush(name_queue, (neighbor_vertex.distanceValue, neighbor_name))

    # Using a_graph lookup table, a_graph vertices dictionary, and visited_vertices,
    # create a dictionary representing the MST of the subgraph of a_graph containing `name`,
    # when excluding factories and other potential factories

    # Sc: name_queue is empty, as no vertices remain on the frontier
    # AND the minimum spanning tree has been found,
    # AND root of this tree is the vertex represented by `name`

    return get_paths_to_customers(a_graph, visited_vertices)


if __name__ == '__main__':
    s = readFileIntoString('graph2.txt')
    g = parse_into_graph(s)
    mst = prims_algorithm(g, 'Newtown_Factory_potential')
    print(mst)
    print(parse_mst_dict(mst))

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
