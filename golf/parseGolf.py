def readFileIntoArray(name):
    arr = []
    f = open(name)
    rows_raw = f.read().strip().split('\n')
    for row in rows_raw:
        cols = list(map(int, row.split()))

        if min(cols) < 0:
            raise ValueError("Must provide nonnegative heights")

        arr.append(cols)

    length_validity = set([len(row) for row in arr])
    if len(length_validity) != 1:
        raise ValueError("Row lengths do not match")
    return arr



if __name__ == "__main__":
    arr = readFileIntoArray('sampleGrid1.txt')
    print(arr)
