LABELS = {'C': 'Customer', 'F': 'Factory', 'M': 'Mail Station', 'P': 'Potential Factory'}


class Vertex:

    def __init__(self, label_type, name):
        Vertex.check_type(label_type, name)
        self.type = label_type.upper()
        self.name = name

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return LABELS[self.type] + ": " + self.name

    @staticmethod
    def check_type(potential_type, potential_name):
        if potential_type.upper() not in LABELS.keys():
            raise TypeError("Not a valid type for vertex ", potential_name)


class Edge:
    def __init__(self, vertex1: Vertex, vertex2: Vertex, cost=0.0):
        if not Edge.is_valid_pairing(vertex1, vertex2):
            v1_full, v2_full = LABELS[vertex1.type], LABELS[vertex2.type]
            exception_str = "Locations of types {} and {} cannot be directly connected".format(v1_full, v2_full)
            raise TypeError(exception_str)

        # Store a set to allow edge's vertices to be referenced in either order
        self.pair = {vertex1.name, vertex2.name}
        self.cost = cost

    @staticmethod
    def is_valid_pairing(first: Vertex, second: Vertex):
        pairing = {first.type, second.type}
        # Mail stations can connect to any other location
        if 'M' in pairing:
            return True
        elif len(pairing) == 1:
            # No other pair of vertices can have the same type
            # That is, customers can't deliver to each other
            # Factories can't connect to each other, etc.
            return False
        elif 'C' in pairing:
            # Can connect to F or P
            return True
        elif 'F' in pairing and 'P' in pairing:
            # Factories cannot directly connect to potential factories
            return False


if __name__ == '__main__':
    vert1 = Vertex('C', 'Athreya')
    vert2 = Vertex('M', 'UPS_Store')
    vert3 = Vertex('F', 'Bakersfield_Factory')
    vert4 = Vertex('P', 'Newtown_Factory_potential')

    e1 = Edge(vert1, vert2)
    e2 = Edge(vert2, vert3)
    e3 = Edge(vert1, vert3)
    e4 = Edge(vert3, vert4)
