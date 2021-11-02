import pandas as pd
import numpy as np
import argparse
import math

def get_data(csv_path):
   '''
   Parameters:
      csv_path - The path to the csv file
   Returns:
      A pandas dataframe 
   '''
   D = pd.read_csv(csv_path) 
   restrictions = list(D.iloc[0:])
   cols = [x for x in range(D.shape[1])]
   new_cols = []
   for x in range(len(restrictions)):
      if int(float(restrictions[x])) == 1:
         new_cols.append(x)
   D = D.iloc[1:, new_cols]
   return D

def distance(x1, x2):
   return (((x1-x2) **2) ** .5).sum()

def find_farthest(D, centroids):
   max_distance = -math.inf 
   centroid = None
   for point in D:
      if np.any(point == centroids):
         pass
      else:
         current_distance = 0
         for c in centroids:
            current_distance += distance(point, c)
         if current_distance > max_distance:
            max_distance = current_distance
            centroid = point
   return centroid


def select_initial(D, k):
   average = np.array([0.0] * D.shape[1])
   for x in D:
      average += x
   average = average / len(D)
   centroids = []
   centroids.append(find_farthest(D, [average]))
   for x in range(k-1):
      new_centroid = find_farthest(D, [centroids])
      centroids.append(new_centroid)
   return centroids

def calculate_SSE(centroids, assignments):
   sse = 0
   for x in range(len(centroids)):
      for y in assignments[x]:
         sse += distance(x, y)
   return sse

def check_stopping(centroids, assignments, prev_sse):
   return abs(prev_sse - calculate_SSE(centroids, assignments))

def assign_points(centroids, D):
   assignments = [[] for x in range(len(centroids))]
   for point in D:
      min_distance = math.inf
      index = None
      for x in range(len(centroids)):
         dis = distance(centroids[x], point)
         if dis < min_distance:
            min_distance = dis
            index = x
      assignments[index].append(point)
   return assignments

def find_new_centroids(assignments):
   centroids = []
   for cluster in assignments:
      new_center = np.array([0.0] * len(cluster[0]))
      for point in cluster:
         new_center += point
      new_center /= len(cluster)
      centroids.append(new_center)
   return centroids

def print_output(centroids, assignments):
   for x in range(len(centroids)):
      print("Cluster " +  str(x) + ":")
      print("Center:", centroids[x])
      distances = [sum(y) for y in abs(assignments[x] - centroids[x])]
      print("Max Dist. to Center:", max(distances))
      print("Min Dist. to Center:", min(distances))
      print("Avg Dist. to Center:", sum(distances) / len(distances))

def main():
   parser = argparse.ArgumentParser("Run K Means Clustering on the dataset")
   parser.add_argument("csv_path", help = "The filepath to the dataset")
   parser.add_argument("-k", required=True, help = "The number of clusters")
   args = parser.parse_args()
   D = get_data(args.csv_path)
   D = D.to_numpy()
   k = int(args.k)
   thr = .1
   init_centroids = select_initial(D, k)
   assignments = assign_points(init_centroids, D)
   prev_sse = calculate_SSE(init_centroids, assignments)
   centroids = find_new_centroids(assignments)
   assignments = assign_points(centroids, D)
   while check_stopping(centroids, assignments, prev_sse) > thr:
      centroids = find_new_centroids(assignments)
      assignments = assign_points(centroids, D)
      prev_sse = calculate_SSE(centroids, assignments)
   print_output(centroids, assignments)


if __name__ == '__main__':
   main()
