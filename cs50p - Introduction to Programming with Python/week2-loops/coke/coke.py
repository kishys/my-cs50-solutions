price = 50
totalpaid = 0
coins = [25, 10, 5]

while price > 0:
    print(f"Amount Due: {price}")
    pay = int(input("Insert Coin: "))
    if pay in coins:
        price = price - pay
        totalpaid = totalpaid + pay

if totalpaid >= price:
    print(f"Change Owed: {totalpaid - 50}")
