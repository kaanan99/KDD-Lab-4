import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_cluster_2D(clusters):
   x = []
   y = []
   cluster = []
   for c in range(len(clusters)):
      for point in clusters[c]:
         x.append(point[0])
         y.append(point[1])
         cluster.append(c + 1)
   df = pd.DataFrame({"x":x, "y":y, "cluster":cluster})
   fig, ax = plt.subplots()
   ax.scatter(df.x, df.y, c = pd.Categorical(df.cluster).codes)
   plt.legend()
   plt.show()
   return

def plot_cluster_3D(clusters):
   x = []
   y = []
   z = []
   cluster = []
   for c in range(len(clusters)):
      for point in clusters[c]:
         x.append(point[0])
         y.append(point[1])
         z.append(point[2])
         cluster.append(c + 1)
   df = pd.DataFrame({"x":x, "y":y, "z":z, "cluster":cluster})
   fig = plt.figure()
   ax = plt.axes(projection ="3d")
   ax.scatter3D(df.x, df.y, df.z, c = pd.Categorical(df.cluster).codes)
   plt.show()

def main():
   x = [[[1, 2, 3]], [[2, 4, 6]], [[5, 6, 7]]] 
   plot_cluster_3D(x)


if __name__ == '__main__':
   main()
