import hashlib

# Class to construct a Merkle Tree and compute the Merkle Root
class MerkleTree:
    
    def __init__(self, transactions):
        self.transactions = [tx for tx in transactions if tx is not None]
        if len(transactions) < 1 or len(transactions) > 3:
            raise ValueError("Merkle Tree must be constructed with 1 to 3 transactions.")
        
        self.root = self.build_tree()
    
    def hash_data(self, data):
        return hashlib.sha3_256(data.encode()).hexdigest()

    def build_tree(self):
        # Hash individual transactions
        hashes = [self.hash_data(tx) for tx in self.transactions]
        
        # Handle case with 1 transaction (root is just the hash of that transaction)
        if len(hashes) == 1:
            return hashes[0]
        
        # Handle case with 2 transactions
        if len(hashes) == 2:
            return self.hash_data(hashes[0] + hashes[1])
            
        # Original case with 3 transactions
        h1, h2, h3 = hashes
        h12 = self.hash_data(h1 + h2)
        return self.hash_data(h12 + h3)

    def get_root(self):
        return self.root
    
def hash_data(data):
        return hashlib.sha3_256(data.encode()).hexdigest()


num_acc = int(input("Enter the number of accounts: "))
accounts = {}

for i in range(num_acc):
    acc, bal = input(f"Enter details of account {i+1}: ").split()
    accounts[acc] = int(bal)

print("Accounts with their balances: ", accounts)

num_txns = int(input("Enter the number of transactions: "))
txns = []

for _ in range(num_txns):
    acc1, acc2, amount, extra_data = input().split()  
    txns.append({
        "from": acc1,
        "to": acc2,
        "amt": int(amount),
        "extra_data": int(extra_data),
    })

count, block_count, prev_block_hash = 0, 0, 0
merkle_data = [None] * 3
valid_transactions = []

for i in range(num_txns):
    if accounts[txns[i]["from"]] >= txns[i]["amt"]:
        accounts[txns[i]["from"]] -= txns[i]["amt"]
        accounts[txns[i]["to"]] += txns[i]["amt"]

        # Store concatenated transaction string
        merkle_data[count] = txns[i]["from"] + txns[i]["to"] + str(txns[i]["amt"])
        valid_transactions.append(txns[i])
        count += 1

        if count == 3:
            block_count += 1
            merkle_tree = MerkleTree(merkle_data)

            transactions_array = [
                [tx["from"], tx["to"], tx["amt"], tx["extra_data"]]
                for tx in valid_transactions[-3:]  # Get last 3 valid transactions
            ]
            
            current_block_hash = hash_data(str(prev_block_hash) + str(block_count) + merkle_tree.get_root())

            print(block_count)
            print(f"Block hash for Block {block_count}",current_block_hash)
            print(transactions_array)
            print(f"Merkle Root for Block {block_count}", merkle_tree.get_root())
            
            # Reset for next batch
            merkle_data = [None] * 3
            count = 0
            prev_block_hash = current_block_hash
    else:
        continue

if count > 0:
    block_count += 1
    valid_txns = [tx for tx in merkle_data if tx is not None]
    if valid_txns:
        merkle_tree = MerkleTree(valid_txns)
        transactions_array = [
        [tx["from"], tx["to"], tx["amt"], tx["extra_data"]]
        for tx in valid_transactions[-count:]  # Get last 'count' transactions
        ]

        current_block_hash = hash_data(str(prev_block_hash) + str(block_count) + merkle_tree.get_root())
        
        print(block_count)
        print(f"Block hash for Block {block_count}",current_block_hash)
        print(transactions_array)
        print(f"Merkle Root for Block {block_count}", merkle_tree.get_root())


# print("Accounts with their new balances: ", accounts)

