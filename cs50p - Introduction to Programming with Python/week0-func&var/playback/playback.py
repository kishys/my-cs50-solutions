a = input("")

lst=[]

for i in a:
    if i == " ":
        lst.append("...")
    else:
        lst.append(i)

print(*lst, sep='')
