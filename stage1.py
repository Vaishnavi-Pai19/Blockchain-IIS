import hashlib

class Block:
    def __init__(self, block_num, block_hash, txns, merkle_root):
        self.block_num = block_num
        self.block_hash = block_hash
        self.txns = txns
        self.merkle_root = merkle_root

class Blockchain:
    def __init__(self):
        self.blocks = []

    def add_block(self, block_num, block_hash, txns, merkle_root):
        self.blocks.append(Block(block_num, block_hash, txns, merkle_root))

    def print_blocks(self):
        for block in self.blocks:
            print(block.block_num)
            print(f"Block hash for Block {block.block_num}: {block.block_hash}")
            print(block.txns)
            print(f"Merkle Root for Block {block.block_num}: {block.merkle_root}")

class MerkleTree:
    
    def __init__(self, transactions):
        self.transactions = [tx for tx in transactions if tx is not None]
        self.root = self.build_tree()
    
    def hash_data(self, data):
        return hashlib.sha3_256(data.encode()).hexdigest()

    def build_tree(self):
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

blockchain = Blockchain()

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

            blockchain.add_block(
                block_count,
                current_block_hash,
                transactions_array,
                merkle_tree.get_root()
            )

            merkle_data = [None] * 3
            count = 0
            prev_block_hash = current_block_hash
    else:
        continue

if count > 0:
    block_count += 1
    merkle_tree = MerkleTree([tx for tx in merkle_data if tx is not None])
    transactions_array = [
        [tx["from"], tx["to"], tx["amt"], tx["extra_data"]]
        for tx in valid_transactions[-count:]
    ]
    current_block_hash = hash_data(str(prev_block_hash) + str(block_count) + merkle_tree.get_root())
    
    blockchain.add_block(
        block_count,
        current_block_hash,
        transactions_array,
        merkle_tree.get_root()
    )

blockchain.print_blocks()