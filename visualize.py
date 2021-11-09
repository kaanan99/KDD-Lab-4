import matplotlib.pyplot as plt
import seaborn as sns
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
   sns.scatterplot(x = "x", y = "y", hue = "cluster", data = df)
   plt.show()
   return

def main():
   x = [[[1, 2]], [[2, 4]], [[5, 6]]] 
   plot_cluster_2D(x)


if __name__ == '__main__':
   main()
