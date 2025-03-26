import hashlib

num_acc = int(input("Enter the number of accounts: "))

accounts = {}

for i in range(num_acc):
    acc, bal = input(f"Enter details of account {i+1}: ").split()
    accounts[acc] = int(bal)

print("Accounts with their balances: ", accounts)

num_txns = int(input("Enter the number of transations: "))

txns = []

for _ in range(num_txns):
    acc1, acc2, amount, extra_data = input().split()  
    txns.append({
        "from": acc1,
        "to": acc2,
        "amt": int(amount),
        "extra_data": int(extra_data),
    })

# print("Transactions:", transactions)
# print(txns[0]["from"])
# print(accounts[txns[0]["from"]])

count = 0
merkle_data = [None] * 3

for i in range(num_txns):
    # print (accounts[txns[i]["from"]], txns[i]["amt"])
    if (accounts[txns[i]["from"]] >= txns[i]["amt"]):
        accounts[txns[i]["from"]] -= txns[i]["amt"]
        accounts[txns[i]["to"]] += txns[i]["amt"]
        merkle_data[count] = txns[i]["from"] + txns[i]["to"] + str(txns[i]["amt"])
        count += 1
        if (count == 3 or i == num_txns-1):
            print(merkle_data)
            count = 0
            merkle_data = [None] * 3
    else:
        continue

print("Accounts with their new balances: ", accounts)