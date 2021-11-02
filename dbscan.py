import numpy as np
import pandas as pd
import from kmeans get_data

class Point:

    def __init__(self, value):
        self.visited = False
        self.label = None
        self.neighborhood = []
        self.core = None
        self.value = value

    def createNeighborhood (self, D, epsilon):
        for x in D:
            dist = distance(self.value, x)
            if dist < epsilon:
                self.neighborhood.append(x)


def dbscan(argv):
    file = argv[1]
    epsilon = argv[2]
    minPts = argv[3]

    coreNum = 0
    D = get_data(file)
    D = D.to_numpy()

    points = {}
    cores = []
    for x in D:
        point = Point(x)
        point.createNeighborhood(D, epsilon)
        if len(point.neighborhood) >= minPts:
            point.core = True
            cores.append(x)
        else:
            point.core = False
        points[x] = point

    currentLabel = 0
    clusters = {}

    for x in cores:
        point = points[x]
        point.visited = True
        if point.label == None:
            currentLabel += 1
            point.label = currentLabel
            DensityConnected(point, currentLabel, points)


    cluster_list = [[] * currentLabel]
    noise = []
    border = []

    for x in points.keys():
        point = points[x]
        if point.visited == True:
            if point.core == False:
                border.append(x)
            cluster_list[point.label-1].append(x)
        else:
            noise.append(x)
    return cluster_list, cores, border, noise

def DensityConnected(point, clusterId, points):

    for x in point.neighborhood:
        d = points[x]
        d.label = clusterId
        if d.visited == False:
            d.visited = True
            if d.core == True:
                DensityConnected(d, clusterId, points)

def distance(x1, x2):
   return (((x1-x2) **2) ** .5).sum()


if __name__ == '__main__':
    dbscan()