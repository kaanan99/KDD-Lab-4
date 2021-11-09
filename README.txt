CSC 466
Lab 4

Jacob Gold - jgold04@calpoly.edu
Kaanan Kharwa - kkharwa@calpoly.edu 

Kmeans Clustering - kmeans.py
Compile instructions:
python3 kmeans.py
Required flags:
1. [-k] num -> number of clusters
2. dataset.csv -> input dataset
Optional flags:
1. [-c] class -> class label column index
2. [-norm] (0,1) -> if 1, normalizes data before computing clusters
3. [-h] -> help

DBSCAN - dbscan.py
Compile instructions:
python3 dbscan.py
Required flags:
1. [-ep] num -> epsilon value for clusters
2. [-minPts] num -> minimum points per cluster
3. dataset.csv -> input dataset
Optional flags:
1. [-c] class -> class label column index
2. [-norm] (0,1) -> if 1, normalizes data before computing clusters
3. [-h] -> help

Hierarchical Clustering - hclustering.py
Compile instructions:
python3 hclustering.py [-h] dataset.csv 
Required flags:
1. [-t] num -> threshold value for clusters
2. dataset.csv -> input dataset
Optional flags:
1. [-c] class -> class label column index
2. [-norm] (0,1) -> if 1, normalizes data before computing clusters
3. [-h] -> help