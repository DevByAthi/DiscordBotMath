from parseTopLevel import readFileIntoString


def parseGraph(file_str_list):
    for line in file_str_list:
        print(line)

    num_vertices = 0
    num_edges = 0
    try:
        num_vertices = int(file_str_list[0])
        num_edges = int(file_str_list[2])
    except ValueError or IndexError:
        raise ValueError("First line must contain two integers: number of vertices and number of edges")

    for i in range(2, num_vertices + 2):
        pass


if __name__ == '__main__':
    pass