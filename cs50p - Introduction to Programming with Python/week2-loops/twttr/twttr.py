text = input("Input: ")
vowels = ["a", "e", "i", "o", "u"]
output = print("Output: ", end="")

for c in text:
    if c.lower() not in vowels:
        print(c, end="")
