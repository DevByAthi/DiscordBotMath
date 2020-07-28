class Vertex:

    LABELS = {'C', 'F', 'M', 'P'}

    def __init__(self, type, name):
        Vertex.checkType(type, name)
        self.type = type
        self.name = name

    @staticmethod
    def checkType(potential_type, potential_name):
        if potential_type.upper() not in Vertex.LABELS:
            raise TypeError("Not a valid type for vertex ", potential_name)


class Edge:
    pass


if __name__ == '__main__':
    vert = Vertex('C', 'Athreya')