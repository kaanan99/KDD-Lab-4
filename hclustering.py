import numpy as np
import pandas as pd
import argparse
import kmeans
import math
import os
import json
import queue
import dbscan
import visualize

class Tree:
   
   def __init__(self, height, leaf, name):
      self.height = height
      self.leaf = leaf
      self.name = name
      self.left = None
      self.right = None

   def __str__(self):
      return self.name

   def to_dict(self, root=False):
     d = {}
     if self.height == 0:
      return {"type": "leaf", "height": 0, "data": self.name}
     the_type = "node"
     if root:
        the_type = "root"
     nodes = []
     nodes.append(self.left.to_dict())
     nodes.append(self.right.to_dict())
     return {"type": the_type, "height": round(self.height, 2), "data": self.name, "nodes": nodes}

def populate_matrix(df, points):
   for x in range(df.shape[0]):
      for y in range(x+1, df.shape[0]):
         dist = kmeans.distance(points[x], points[y])
         df.iloc[x, y] = dist
         df.iloc[y, x] = dist

def complete_link(df, col1, col2):
   values = []
   for x in df.columns:
      if not np.isnan(df.loc[col1, x]) and not np.isnan(df.loc[col2, x]):
         values.append(max(df.loc[col1][x], df.loc[col2][x]))
   return values

def update_matrix(df, col1, col2):
   values = complete_link(df, col1, col2)
   df = df.drop([col1], axis = 1)
   df = df.drop([col2], axis = 1)
   df = df.drop([col1], axis = 0)
   df = df.drop([col2], axis = 0)
   new_name = str(col1) + ", " + str(col2)
   new_row = pd.Series(data = values, name = new_name)
   new_row = new_row.set_axis(df.columns)
   df[new_name] = values
   df = df.append(new_row, ignore_index = False)
   return df

def find_next(df):
   min_val = math.inf
   best_col = None
   best_row = None
   for col in df.columns:
      for row in df.index:
         if df.loc[col, row] < min_val:
            min_val = df.loc[col, row]
            best_col = col
            best_row = row
   return best_col, best_row, min_val

def adjust_tree(col1, col2, nodes, distance):
   node1 = None
   node2 = None
   for x in range(len(nodes)):
      if nodes[x].name == str(col1):
         node1 = nodes[x]
      elif nodes[x].name == str(col2):
         node2 = nodes[x]
   nodes.remove(node1)
   nodes.remove(node2)
   new_node = Tree(distance, False,node1.name + ", " + node2.name)
   new_node.left = node1
   new_node.right = node2
   nodes.append(new_node)


def to_json(the_file, csv):
   outpath = os.path.splitext(csv)[0] + '.json'
   with open(outpath, 'w') as f:
      json.dump(the_file, f)

def get_clusters(dendogram, thr, points):
   clusters = []
   q = queue.Queue()
   q.put(dendogram)
   while not q.empty():
      current = q.get()
      if current.height <= thr:
         clusters.append([points[int(x)] for x in current.name.split(", ")])
      else:
         q.put(current.left)
         q.put(current.right)
   return clusters

def print_output(cluster_list, classes):
   for x in range(len(cluster_list)):
       print("\nCluster " + str(x + 1) + ":")
       print("Points in cluster:", len(cluster_list[x]))
       max_dist, min_dist, total_avg = dbscan.find_max_min(cluster_list[x])
       print("Maximum distance between two points:", max_dist)
       print("Minimum distance between two points:", min_dist)
       print("Average distance between points:", total_avg)
       print("Points in Cluster:")
       for point in cluster_list[x]:
          class_val = ""
          if len(classes) > 0:
             class_val = classes[tuple(point)]
          print(point, class_val)


def main():
   # Get Arguments
   parser = argparse.ArgumentParser("Run K Means Clustering on the dataset")
   parser.add_argument("csv_path", help = "The filepath to the dataset")
   parser.add_argument("-t", required=False, help = "The value for the threshold")
   parser.add_argument("-c", required=False, help = "The index of the class column")
   parser.add_argument("-norm", required=False, help= "Set 1 to have to data normalized")
   parser.add_argument("-v", required=False, help= "Set 1 to have a visualization of the data, only works on 2D datasets, use 2 for 3D dataset")
   args = parser.parse_args()
   
   # Setting Up
   D, class_col = kmeans.get_data(args.csv_path, args.c, args.norm)
   D = D.to_numpy()
   classes = {}
   if class_col != None:
      for x in range(len(D)):
         classes[tuple(D[x])] = class_col[x]
   points = {}
   for x in range(len(D)):
      points[x] = D[x]

   # Initializing Data Frame
   df = pd.DataFrame([[np.nan] *len(D)] * len(D))
   populate_matrix(df, points)
   
   # Initializing Tree
   nodes = []
   for i in range(D.shape[0]):
      nodes.append(Tree(0, True, str(i)))
   
   # Main Loop
   while df.shape[0] > 2:
      col1, col2, distance = find_next(df)
      df = update_matrix(df, col1, col2) 
      adjust_tree(col1, col2, nodes, distance)
   
   # Creating the Tree
   node1 = nodes[0]
   node2 = nodes[1]
   distance = df.iloc[0,1]
   root_node = Tree(distance, False, node1.name + ", " + node2.name)
   root_node.left = node1
   root_node.right = node2
   dendogram = root_node.to_dict(True)
   csv = os.path.basename(args.csv_path)
   to_json(dendogram, csv)

   # Getting Clusters
   if args.t != None:
      clusters = get_clusters(root_node, float(args.t), points)
      print_output(clusters, classes)
  
   if args.v != None:
      if args.v == "1":
         visualize.plot_cluster_2D(clusters)

if __name__ == '__main__':
   main()
