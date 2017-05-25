import numpy as np
from annoy import AnnoyIndex
import networkx as nx
from scipy.cluster.vq import vq, kmeans, whiten

# Creates feature vectors for in/out edges of digraph
def get_egonet_features(G):
	featin = []
	featout = []
	for inx, node in enumerate(G.nodes()):
		# Lambda functions
		ine = lambda n: G.in_edges(n)
		oute = lambda n: G.out_edges(n)

		in_ego = list(map(lambda e: e[0], ine(node))) + [node]
		out_ego = list(map(lambda e: e[1], oute(node))) + [node]

		in_edges = list(filter(lambda e: (e[0] and e[1]) in in_ego, ine(in_ego)))
		out_edges = list(filter(lambda e: (e[0] and e[1]) in out_ego, oute(out_ego)))

		in_weights = [-1.0]
		out_weights = [-1.0]
		if len(in_edges) > 0:
			in_weights = list(map(lambda e: G[e[0]][e[1]]["weight"], in_edges))
			if sum(in_weights) == 0:
				in_weights = [-1.0]
		if len(out_edges) > 0:
			out_weights = list(map(lambda e: G[e[0]][e[1]]["weight"], out_edges))
			if sum(out_weights) == 0:
				out_weights = [-1.0]

		featin.append([len(in_ego), len(in_edges), 1 / sum(in_weights)])
		featout.append([len(out_ego), len(out_edges), 1 / sum(out_weights)])

	return (featin, featout)

# Picks top k features with highest summed distance to their k nearest neighbors
def get_knn_outliers(k, features, num_trees=10):
	t = AnnoyIndex(len(features[0]))
	for inx, elt in enumerate(features):
		t.add_item(inx, elt)
	t.build(num_trees)

	outlier_scores = []
	for i in range(len(features)):
		# Get summed distances to all num_neighbors
		knn = t.get_nns_by_item(i, k, include_distances=True)
		outlier_scores.append(sum(knn[1]))

	outlier_scores = np.array(outlier_scores)
	k_outliers = outlier_scores.argsort()[::-1]
	return k_outliers, outlier_scores

def get_global_centroid(features):
	whitened = whiten(fin)
	book = array((whitened[0],whitened[2]))
	(centroid, weights) = kmeans(whitened, book)
	return (centroid[0], weights)
