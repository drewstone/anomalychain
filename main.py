from sys import argv
from lib import graph, analysis

G = None

if len(argv) > 1:
	G = graph.build_from_database(argv[1])
else:
	G = graph.build_from_database()


(fin, fout) = analysis.get_egonet_features(G)
outliers = analysis.get_knn_outliers(10, fin)
