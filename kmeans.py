import pandas as pd
import numpy as np
import argparse
import math

def normalize(x, max_val, min_val):
    '''
    Parameters:
       x - the value which is being normalized
       max_val - the maximum value in the column
       min_val - the minimum value in the column
    Returns:
       A numerical value which represents the normalized x
    '''
    return (x - min_val) / (max_val - min_val)

def get_data(csv_path, col=None, norm = None):
   '''
   Parameters:
      csv_path - The path to the csv file
      class_col - The name of the class column
   Returns:
      A pandas dataframe 
   '''
   D = pd.read_csv(csv_path) 
   restrictions = list(D.iloc[0:])
   class_col = None
   if col != None:
      class_col = D.iloc[:, int(col)].to_list()
   cols = [x for x in range(D.shape[1])]
   new_cols = []
   for x in range(len(restrictions)):
      if int(float(restrictions[x])) == 1:
         new_cols.append(x)
   D = D.iloc[1:, new_cols]
   #Normalize Data
   if norm != None and int(norm) == 1:
      for x in range(D.shape[1]):
         max_val = max(D.iloc[:, x])
         min_val = min(D.iloc[:, x])
         D.iloc[:, x] = D.iloc[:, x].apply(normalize, args=[max_val, min_val])
   return D, class_col

def distance(x1, x2):
   return (((x1-x2) **2) ** .5).sum()


def check_if_centroid(point, centroids):
   for c in centroids:
      if np.all(point == c):
         return True
   return False

def find_farthest(D, centroids):
   max_distance = -math.inf 
   centroid = None
   for point in D:
      if not check_if_centroid(point, centroids):
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
      new_centroid = find_farthest(D, centroids)
      centroids.append(new_centroid)
   return centroids
  

def calc_SSE_one(center, assignments):
   sse = 0
   for x in assignments:
      sse += distance(center, x)
   return sse

def calculate_SSE(centroids, assignments):
   sse = 0
   for x in range(len(centroids)):
      sse += calc_SSE_one(centroids[x], assignments[x])
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

def print_output(centroids, assignments, classes, is_class):
   for x in range(len(centroids)):
      print("\nCluster " +  str(x) + ":")
      print("Cluster Size: " + str(len(assignments[x])))
      print("Center:", centroids[x])
      distances = [sum(y) for y in abs(assignments[x] - centroids[x])]
      print("Max Dist. to Center:", max(distances))
      print("Min Dist. to Center:", min(distances))
      print("Avg Dist. to Center:", sum(distances) / len(distances))
      print("Sum of Squared Errors:", calc_SSE_one(centroids[x], assignments[x]))
      print("Points in Cluster:")
      for point in assignments[x]:
         class_val = ""
         if is_class != None:
            class_val = classes[tuple(point)]
         print(point, class_val)

def main():
   # Get Arguments
   parser = argparse.ArgumentParser("Run K Means Clustering on the dataset")
   parser.add_argument("csv_path", help = "The filepath to the dataset")
   parser.add_argument("-k", required=True, help = "The number of clusters")
   parser.add_argument("-c", required=False, help = "The index of the class column")
   parser.add_argument("-norm", required=False, help= "Set 1 to have to data normalized")
   args = parser.parse_args()
   # Setting Everything Up 
   D, class_col = get_data(args.csv_path, args.c, args.norm)
   D = D.to_numpy()
   classes = {}
   if class_col != None:
      for x in range(len(D)):
         classes[tuple(D[x])] = class_col[x]
   k = int(args.k)
   thr = .1
   #Find Initial Centriods
   init_centroids = select_initial(D, k)
   #Assign Points
   assignments = assign_points(init_centroids, D)
   #Calculate SSE
   prev_sse = calculate_SSE(init_centroids, assignments)
   #New Centroids and assignments
   centroids = find_new_centroids(assignments)
   assignments = assign_points(centroids, D)
   #Calculate Centroids and Assign Points until Stopping condition
   while check_stopping(centroids, assignments, prev_sse) > thr:
      centroids = find_new_centroids(assignments)
      assignments = assign_points(centroids, D)
      prev_sse = calculate_SSE(centroids, assignments)
   #Print output
   print_output(centroids, assignments, classes, args.c)


if __name__ == '__main__':
   main()
