import sys
from lib import eth

args = sys.argv
start = int(args[1])
amount = int(args[2])

eth.migrate_blockchain(start, amount)
