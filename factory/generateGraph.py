from factory.graphClasses import Vertex, Edge
from parseTopLevel import readFileIntoString

'''
:param file_str_list List
:throws KeyError, IndexError
'''
def parseGraph(file_str_list):

    num_vertices = 0
    num_edges = 0
    try:
        num_vertices, num_edges = tuple(map(int, file_str_list[0].split()))
    except ValueError or IndexError:
        raise ValueError("First line must contain two integers: number of vertices and number of edges")
    except TypeError:
        raise ValueError("Do not split input values between two lines. Must be on a single line")

    vertices = dict()
    edges = set()

    i = 0
    for i in range(1, num_vertices + 1):
        label_type, name = file_str_list[i].split()
        v = Vertex(label_type, name)
        vertices[name] = v
        print(v)

    start_index = i + 1
    for i in range(start_index, len(file_str_list)):
        print("a" + file_str_list[i] + " b")
        first, second, cost = file_str_list[i].split()
        try:
            e = Edge(vertices[first], vertices[second], cost)
            edges.add(e)
            print(e)
        except KeyError:
            raise KeyError("No existing vertex for path between {} and {}".format(first, second))


if __name__ == '__main__':
    s = readFileIntoString('graph1.txt')
    parseGraph(s)
