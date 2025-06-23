try:
    num = int(input())
except:
    raise TypeError("Should be an integer")

items = input().split(" ")
items = [int(x) for x in items]
# print(items)
# assert len(items)==num, "Did not split properly"

max_sum = 0

for i in range(len(items)):
    for j in range(i,len(items)):
        x = items[i:j+1]
        s = sum(x)
        # print(x)
        max_sum = max(max_sum, s)

print(max_sum)
