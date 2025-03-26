import hashlib

class Block:
    def __init__(self, block_num, block_hash, txns, merkle_root, nonce_miner):
        self.block_num = block_num
        self.block_hash = block_hash
        self.txns = txns
        self.merkle_root = merkle_root
        self.nonce_miner = nonce_miner

class Blockchain:
    def __init__(self):
        self.blocks = []

    def add_block(self, block_num, block_hash, txns, merkle_root, nonce_miner):
        self.blocks.append(Block(block_num, block_hash, txns, merkle_root, nonce_miner))

    def print_blocks(self):
        for block in self.blocks:
            print(block.block_num)
            print(f"Block hash for Block {block.block_num}: {block.block_hash}")
            print(block.txns)
            print(f"Merkle Root for Block {block.block_num}: {block.merkle_root}")
            print(block.nonce_miner)

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
            
        # Handle case with 3 transactions
        if len(hashes) == 3:
            h1, h2, h3 = hashes
            h12 = self.hash_data(h1 + h2)
            return self.hash_data(h12 + h3)
        
        # Full merkle tree with 4 transactions
        h1, h2, h3, h4 = hashes
        h12 = self.hash_data(h1 + h2)
        h34 = self.hash_data(h3 + h4)
        return self.hash_data(h12 + h34)

    def get_root(self):
        return self.root
            
def hash_data(data):
    return hashlib.sha3_256(data.encode()).hexdigest()

def sort_txns(txns):
    idx_txns = [(idx, tx) for idx, tx in enumerate(txns)]

    idx_txns.sort(key=lambda item: (-item[1]["incentive"], item[1]["to"], item[0]))

    return [tx for _, tx in idx_txns]

def find_nonce(block_hash):
    nonce = 0

    while True:
        data = block_hash + str(nonce)
        hashed_data = hash_data(data)

        if hashed_data.endswith('0'):
            return nonce
        
        nonce += 1

def find_miner(miners, block_num):
    bss_scores = []
    max_score = 0
    sel_miner = ' '

    for miner in miners:
        bhs = miner["bhsa"][block_num % 8]
        bss_score = miner["com_score"] * bhs
        bss_scores.append((miner["miner_id"], bss_score))
        if (bss_score > max_score):
            max_score = bss_score
            sel_miner = miner["miner_id"]

    return sel_miner



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
    acc1, acc2, amount, incentive = input().split()  
    txns.append({
        "from": acc1,
        "to": acc2,
        "amt": int(amount),
        "incentive": int(incentive),
    })

txns = sort_txns(txns)

block_reward = int(input("Enter the block reward available: "))

num_miners = int(input("Enter the number of miners: "))
miners = []

for _ in range(num_miners):
    inputs = input().split()
    miner_id = inputs[0]
    com_score = int(inputs[1])
    bhsa = list(map(int, inputs[2:10]))

    miners.append({
        "miner_id": miner_id,
        "com_score": com_score,
        "bhsa": bhsa
    })

count, block_count, prev_block_hash = 0, 0, 0
merkle_data = [None] * 4
valid_transactions = []

for i in range(num_txns):
    if accounts[txns[i]["from"]] >= txns[i]["amt"]:
        accounts[txns[i]["from"]] -= txns[i]["amt"]
        accounts[txns[i]["to"]] += txns[i]["amt"]

        # Store concatenated transaction string
        merkle_data[count] = txns[i]["from"] + str(txns[i]["incentive"]) + txns[i]["to"] + str(txns[i]["amt"])
        valid_transactions.append(txns[i])
        count += 1

        if count == 4:
            print(merkle_data)
            block_count += 1
            merkle_tree = MerkleTree(merkle_data)

            transactions_array = [
                [tx["from"], tx["to"], tx["amt"], tx["incentive"]]
                for tx in valid_transactions[-4:]  # Get last 3 valid transactions
            ]
            
            current_block_hash = hash_data(str(prev_block_hash) + str(block_count) + merkle_tree.get_root())

            nonce = find_nonce(current_block_hash)
            bhs_miner = find_miner(miners, block_count)
            nonce_miner = str(nonce) + ' ' + bhs_miner

            accounts[bhs_miner] += block_reward

            blockchain.add_block(
                block_count,
                current_block_hash,
                transactions_array,
                merkle_tree.get_root(),
                nonce_miner
            )

            merkle_data = [None] * 4
            count = 0
            prev_block_hash = current_block_hash
    else:
        continue

if count > 0:
    block_count += 1
    merkle_tree = MerkleTree([tx for tx in merkle_data if tx is not None])
    transactions_array = [
        [tx["from"], tx["to"], tx["amt"], tx["incentive"]]
        for tx in valid_transactions[-count:]
    ]

    current_block_hash = hash_data(str(prev_block_hash) + str(block_count) + merkle_tree.get_root())
    nonce = find_nonce(current_block_hash)
    bhs_miner = find_miner(miners, block_count)
    nonce_miner = str(nonce) + ' ' + bhs_miner

    accounts[bhs_miner] += block_reward
    
    blockchain.add_block(
        block_count,
        current_block_hash,
        transactions_array,
        merkle_tree.get_root(),
        nonce_miner
    )

blockchain.print_blocks()

# print("Accounts with their new balances: ", accounts)