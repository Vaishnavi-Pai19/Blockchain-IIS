import hashlib

# Input data
data = input("Enter data to be hashed: ")

# Compute SHA-256 hash
sha256_hash = hashlib.sha3_256(data.encode()).hexdigest()

print("SHA-256 Hash:", sha256_hash)