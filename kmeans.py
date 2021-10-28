import pandas as pd
import numpy as np
import argparse

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


def main():
   parser = argparse.ArgumentParser("Run K Means Clustering on the dataset")
   parser.add_argument("csv_path", help = "The filepath to the dataset")
   parser.add_argument("-k", required=True, help = "The number of clusters")
   args = parser.parse_args()
   D = get_data(args.csv_path)
   print(D)

if __name__ == '__main__':
   main()
