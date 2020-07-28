from parseTopLevel import readFileIntoString
def readIntoGrid(rows_raw):
    arr = []
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
    arr = readIntoGrid(readFileIntoString('sampleGrid6.txt'))
    print(arr)
