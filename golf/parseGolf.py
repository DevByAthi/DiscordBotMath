def readFileIntoArray(name):
    arr = []
    f = open(name)
    rows_raw = f.read().split('\n')
    for row in rows_raw:
        cols = list(map(int, row.split()))

        if min(cols) < 0:
            raise ValueError("Must provide nonnegative heights")

        arr.append(cols)
    return arr



if __name__ == "__main__":
    arr = readFileIntoArray('sampleGrid1.txt')
    print(arr)
