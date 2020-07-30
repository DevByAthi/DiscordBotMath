import factory.graphClasses
from heapq import heapify, heappop

def getNeighboringNodes(a_graph, a_node):
    # Return a list of all nodes in a_graph which are adjacent to a_node
    return [1, 2, 3]

def findCheapestShippingPath(a_graph, a_node_name):
    # Abstract: Decide which factory a customer should order chocolate from to minimize shipping costs.
    # Pre (graph): a_graph is a graph with non-negative edge weights representing the shipping network connecting
    #   customers, mail centers, factories, and potential factory construction sites. See graphClasses.py for
    #   implementation details.
    # Pre (node): a_node_name is a string corresponding to the name of one of the nodes in a_graph.
    # Post: factoryToReturn is a tuple wherein the first entry is the name of the factory node, cheapest_factory,
    #   which the customer should order chocolate from such that the path weight between cheapest_factory and
    #   a_node_name is minimal as compared to the path weight between a_node_name and any other factory node, and the
    #   second entry is the cost of shipping from that factory node to a_node_name.

    # Sa: pathQueue is a binary heap which contains every node in a_graph, ranked by the total weight needed to reach
    #   that node from a_node_name. To begin with, all nodes  have a weight of infinity, except the node with
    #   name=a_node_name, which has weight 0 as the starting node.

    # Get the dict of nodes from a_graph
    # Store them as a list pathQueue
    # Find the node n0 with n0.name = a_node_name and set n0.distanceValue = 0
    # Put n0 in index 0 of pathQueue
    pathQueue = a_graph.nodes
    pathQueue[a_node_name].distanceValue = 0
    pathQueue = pathQueue.values
    heapify(pathQueue)

    # [Sb]: Every change to pathQueue has been additive in the sense that we have gained information about a shortest
    #   path approaching a factory node.

    removedNodes = set()
    while len(pathQueue) > 0:
        # Since each iteration either removes an element from pathQueue or breaks the loop, this loop is guaranteed
        # not to run indefinitely.

        # Get the node, cheapestNode, from the bottom of pathQueue
        cheapestNode = pathQueue[0]
        # Check if cheapestNode is a factory. If so, we are done.
        if cheapestNode.type == 'F':
            factoryToReturn = tuple(cheapestNode.name, cheapestNode.distanceValue)
            break
        else:
            # Get all neighbor nodes connected to cheapestNode as a list
            neighbouringNodes = getNeighboringNodes(a_graph, cheapestNode)
            for neighborNode in neighbouringNodes:
                if (neighborNode not in removedNodes) and (neighborNode.type == 'F' or neighborNode.type == 'M'):
                    # Calculate whether the path to reach neighborNode is shorter than the existing path.
                    neighborEdge = a_graph.getEdgeBetween(cheapestNode, neighborNode)
                    newDistance = neighborEdge + cheapestNode.distanceValue
                    if newDistance < neighborNode.distanceValue:
                        #   If a new shortest path to neighborNode has been found, update neighborNode's distanceValue
                        #   and position in pathQueue.
                        neighborNode.distanceValue = newDistance
                        heapify(pathQueue)

                elif not (neighborNode.type == 'F' or neighborNode.type == 'M'):
                    # If neighborNode does not have the appropriate node type, remove it from pathQueue, and add it to removedNodes.
                    # No need to re-heapify pathQueue in this case, since neighborNode will always have distanceValue = inf here
                    # and thus will not disturb the order when it is removed.
                    removedNodes.add(neighborNode)
                    pathQueue.remove(neighborNode)

            # Once done with all neighboring nodes of cheapestNode, remove cheapestNode from pathQueue.
            removedNodes.add(cheapestNode)
            pathQueue.remove(cheapestNode)

    # Sc: factoryToReturn has been returned.

    return factoryToReturn
