

def dbscan(argv):
    file = argv[1]
    epsilon = argv[2]
    numPts = argv[3]

    coreNum = 0
    D = []
    for line in file:
        for column in line:
            for row in column:
                D.append(row)

    neighborhoods = {}
    cores = {}
    d_len = len(D)
    for d in range (d_len):
        distances = []
        for i in range (D[d:d_len]):
            dist = distance(d, i)
            if dist <= epsilon:
                distances.append(dist)
        for i in range (D[d_len:d]):
            dist = distance(d, i)
            if dist <= epsilon:
                distances.append(dist)
        neighborhoods.append(d, distances)
        if len(distances) >= epsilon:
            cores.append(d, distances)


if __name__ == '__main__':
    dbscan()