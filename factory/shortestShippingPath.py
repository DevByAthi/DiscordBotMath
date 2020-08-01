from graphClasses import *
from heapq import heapify, heappop

def findCheapestShippingPath(a_graph, a_node_name):
    # Abstract: Decide which factory a customer should order chocolate from to minimize shipping costs.
    # Pre (graph): a_graph is a graph with non-negative edge weights representing the shipping network connecting
    #   customers, mail centers, factories, and potential factory construction sites. See graphClasses.py for
    #   implementation details.
    # Pre (node): a_node_name is a string corresponding to the name of one of the nodes in a_graph.
    # Post: factoryToReturn is a tuple wherein the first entry is the name of the factory node, cheapest_factory,
    #   which the customer should order chocolate from such that the path weight between cheapest_factory and
    #   a_node_name is minimal as compared to the path weight between a_node_name and any other factory node, the
    #   second entry is the total cost of shipping from cheapest_factory to a_node_name.

    # Sa: pathQueue is a binary heap which contains every node in a_graph, ranked by the total weight needed to reach
    #   that node from a_node_name. To begin with, all nodes  have a weight of infinity, except the node with
    #   name=a_node_name, which has weight 0 as the starting node.

    # Get the dict of nodes from a_graph
    # Store them as a list pathQueue
    # Find the node n0 with n0.name = a_node_name and set n0.distanceValue = 0
    # Put n0 in index 0 of pathQueue
    pathQueue = a_graph.vertices
    pathQueue[a_node_name].distanceValue = 0
    pathQueue = list(pathQueue.values())
    heapify(pathQueue)

    # [Sb]: Every change to pathQueue has been additive in the sense that we have gained information about a shortest
    #   path approaching a factory node.

    removedNodes = set()
    factoryToReturn = None
    while len(pathQueue) > 0:
        # Since each iteration either removes an element from pathQueue or breaks the loop, this loop is guaranteed
        # not to run indefinitely.

        # Get the node, cheapestNode, from the bottom of pathQueue
        cheapestNode = pathQueue[0]
        # Check if cheapestNode is a factory. If so, we are done.
        if cheapestNode.type == 'F':
            factoryToReturn = (cheapestNode.name, cheapestNode.distanceValue)
            break
        else:
            # Get all neighbor nodes connected to cheapestNode as a list
            neighbouringNodes = a_graph.getNeighboringNodes(cheapestNode)
            for neighborNode in neighbouringNodes:
                if (neighborNode not in removedNodes) and (neighborNode.type == 'F' or neighborNode.type == 'M'):
                    # Calculate whether the path to reach neighborNode is shorter than the existing path.
                    edgeLookupString = neighborNode.name + '_' + cheapestNode.name
                    if edgeLookupString in a_graph.lookup:
                        neighborEdge = a_graph.lookup[edgeLookupString]
                    else:
                        edgeLookupString = cheapestNode.name + '_' + neighborNode.name
                        neighborEdge = a_graph.lookup[edgeLookupString]

                    newDistance = neighborEdge.cost + cheapestNode.distanceValue
                    if newDistance < neighborNode.distanceValue:
                        #   If a new shortest path to neighborNode has been found, update neighborNode's distanceValue
                        #   and position in pathQueue.
                        neighborNode.distanceValue = newDistance
                        heapify(pathQueue)

                elif (neighborNode not in removedNodes) and not (neighborNode.type == 'F' or neighborNode.type == 'M'):
                    # If neighborNode does not have the appropriate node type, remove it from pathQueue, and add it to removedNodes.
                    # No need to re-heapify pathQueue in this case, since neighborNode will always have distanceValue = inf here
                    # and thus will not disturb the order when it is removed.
                    removedNodes.add(neighborNode)
                    pathQueue.remove(neighborNode)

            # Once done with all neighboring nodes of cheapestNode, remove cheapestNode from pathQueue.
            removedNodes.add(cheapestNode)
            heappop(pathQueue)

    # Sc: factoryToReturn has been returned.
    if factoryToReturn is not None:
        return factoryToReturn
    else:
        print("Uh oh. No factory found.")
        return None

# Testing
if __name__ == '__main__':
    vert1 = Vertex('C', 'Athreya')
    vert2 = Vertex('M', 'UPS_Store')
    vert3 = Vertex('F', 'Bakersfield_Factory')
    vert4 = Vertex('P', 'Newtown_Factory_potential')
    vert5 = Vertex('M', 'UPS_Store2')
    vert6 = Vertex('M', 'UPS_Store3')
    vert7 = Vertex('F', 'Farmfresh_Chocolate')
    vertex_set = {vert1, vert2, vert3, vert4, vert5, vert6, vert7}
    vertices_dict = dict()
    for v in vertex_set:
        vertices_dict[v.name] = v

    e1 = Edge(vert1, vert2, 1)
    e2 = Edge(vert2, vert3, 6)
    e3 = Edge(vert1, vert3, 10)
    e4 = Edge(vert2, vert5, 2)
    e5 = Edge(vert5, vert6, 2)
    e6 = Edge(vert6, vert3, 1)
    e7 = Edge(vert2, vert4, 1)
    e8 = Edge(vert5, vert7, 2)
    edges = {e1, e2, e3, e4, e5, e6, e7, e8}

    g = Graph(vertices_dict, edges)
    factory = findCheapestShippingPath(g, 'Athreya')
    print(factory)
