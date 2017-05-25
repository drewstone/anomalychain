import json
from web3 import Web3, KeepAliveRPCProvider
from pymongo import MongoClient

def migrate_blockchain(start, blockcount):
	web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
	client = MongoClient('localhost', 27017)
	db = client.blockparser
	tx_collection = db["ethereum_transactions"]

	for i in range(blockcount):
		if i % 100000 == 0:
			print(i)

		block = web3.eth.getBlock(start+i, full_transactions=True)
		if len(block["transactions"]) > 0:
			txs = extract_txs(block["transactions"])
			tx_collection.insert_many(txs)

def extract_txs(txs):
	def extract_tx(tx):
		return {
			"to": tx["to"],
			"from": tx["from"],
			"value": str(tx["value"]),
			"blockNumber": str(tx["blockNumber"]),
			"hash": tx["hash"],
			"gas": str(tx["gas"]),
			"gasPrice": str(tx["gasPrice"]),
		}

	transactions = []
	for tx in txs:
		transactions.append(extract_tx(tx))

	return transactions
