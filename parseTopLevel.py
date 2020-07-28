def readFileIntoString(name):
    f = open(name)
    rows_raw = f.read().strip().split('\n')
    return rows_raw
