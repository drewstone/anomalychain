import scipy
import networkx as nx

from lib import analysis as alg
from math import sqrt

from web3 import Web3
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.blockparser
tx_collection = db["ethereum_transactions"]

def build_from_database(size=10):
	G = nx.DiGraph()
	web3 = Web3(None)

	txs = tx_collection.find().limit(int(size))
	tx_count = txs.count()

	# Build directed graph from transactions
	for tx in txs:
		weight = float(web3.fromWei(int(tx["value"]), 'ether'))
		G.add_edge(tx["from"], tx["to"], weight=weight)

	return G
