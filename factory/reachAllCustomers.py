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

            travel_cost = neighbors[neighbor_name]

            neighbor_vertex = a_graph.vertices[neighbor_name]

            # If type of the neighbor is a factory or a potential factory, skip
            if neighbor_vertex.type == 'F' or neighbor_vertex.type == 'P':
                continue

            # Lambda function to determine if current distance to vertex can be further minimized
            isMinimized = lambda a_vertex: a_vertex.distanceValue > current_travel_cost + travel_cost

            # If the neighbor has not yet been visited,
            # or its distance can be minimized
            # update the vertex's distanceValue, add vertex to MST, and add vertex to queue accordingly
            if neighbor_name not in visited_vertices.keys() or isMinimized(neighbor_vertex):
                # Update shortest distance to this neighbor
                neighbor_vertex.distanceValue = current_travel_cost + travel_cost
                # Mark current vertex as predecessor of neighbor in MST, updating the tree
                visited_vertices[neighbor_name] = current_vertex_name
                # Add updated neighbor to queue
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
