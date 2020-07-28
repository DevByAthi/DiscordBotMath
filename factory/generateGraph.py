from factory.graphClasses import Vertex, Edge
from parseTopLevel import readFileIntoString


def parseGraph(file_str_list):

    num_vertices = 0
    num_edges = 0
    try:
        num_vertices, num_edges = tuple(map(int, file_str_list[0].split()))
    except ValueError or IndexError:
        raise ValueError("First line must contain two integers: number of vertices and number of edges")
    except TypeError:
        raise ValueError("Do not split input values between two lines. Must be on a single line")

    vertices = set()
    edges = set()

    i = 0
    for i in range(1, num_vertices + 1):
        label_type, name = file_str_list[i].split()
        v = Vertex(label_type, name)
        vertices.add(v)
        print(v)

    start_index = i
    for i in range(start_index, len(file_str_list)):
        pass


if __name__ == '__main__':
    s = readFileIntoString('graph1.txt')
    parseGraph(s)
