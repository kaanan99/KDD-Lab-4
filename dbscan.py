import numpy as np
import pandas as pd
import kmeans
import argparse
import math

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


def dbscan(D, epsilon, minPts):
    # Getting the Cores and Points
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
        points[tuple(x)] = point

    currentLabel = 0
    clusters = {}
   
    # Going through the cores and recursive call
    for x in cores:
        point = points[tuple(x)]
        point.visited = True
        if point.label == None:
            currentLabel += 1
            point.label = currentLabel
            DensityConnected(point, currentLabel, points)

    cluster_list = [[] for x in range(currentLabel)]
    noise = []
    border = []

    #Classifying points
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
        d = points[tuple(x)]
        d.label = clusterId
        if d.visited == False:
            d.visited = True
            if d.core == True:
                DensityConnected(d, clusterId, points)

def distance(x1, x2):
   return (((x1-x2) **2) ** .5).sum()

def find_max_min(cluster):
   max_dist = -math.inf
   min_dist = math.inf
   total_avg = 0
   for point in cluster:
      point_avg = 0
      for point2 in cluster:
         if point != point2:
            dist = distance(np.array(point), np.array(point2))
            if dist > max_dist:
               max_dist = dist
            if dist < min_dist:
               min_dist = dist
            point_avg += dist
      point_avg /=  len(cluster)
      total_avg += point_avg
   total_avg /= len(cluster)
   return max_dist, min_dist, total_avg

def print_output(cluster_list, noise, classes):
   total = 0
   for x in range(len(cluster_list)):
      print("\nCluster " + str(x) + ":")
      print("Points in cluster:", len(cluster_list[x]))
      max_dist, min_dist, total_avg = find_max_min(cluster_list[x])
      print("Maximum distance between two points:", max_dist)
      print("Minimum distance between two points:", min_dist)
      print("Average distance between points:", total_avg)
      print("Points in Cluster:")
      for point in cluster_list[x]:
         class_val = ""
         if len(classes) > 0:
            class_val = classes[point]
         print(point, class_val)
         total += 1
   if total > 0:
      print("\n Outliers:", len(noise), len(noise) / total)
   for outlier in noise:
      print(outlier)

def main():
   #Getting Arguments
   parser = argparse.ArgumentParser("Run K Means Clustering on the dataset")
   parser.add_argument("csv_path", help = "The filepath to the dataset")
   parser.add_argument("-ep", required=True, help = "The epsilon value")
   parser.add_argument("-minPts", required=True, help = "The minimum points for a point to be considered a core point")
   parser.add_argument("-c", required=False, help = "The index of the class column")
   parser.add_argument("-norm", required=False, help= "Set 1 to have to data normalized")
   args = parser.parse_args()
   # Get Data
   D, class_col = kmeans.get_data(args.csv_path, args.c, args.norm)
   D = D.to_numpy()
   classes = {}
   if class_col != None:
      for x in range(len(D)):
         classes[tuple(D[x])] = class_col[x]
   cluster_list, cores, border, noise = dbscan(D, float(args.ep), float(args.minPts))
   print_output(cluster_list, noise, classes)


if __name__ == '__main__':
    main()
