n = int(input())

entries = {}


# N
for i in range(n):
    a, b = input().split()
    a = int(a)
    b = int(b)
    # if entries[b]:
    try:
        entries[b] = entries[b] + a
    except:
        entries[b] = a

# print(entries)

# N^2
s_entries = sorted(entries.items())  # , key=lambda item: item[1])

# print(s_entries)

# N^2
# def qsort(list):
# return list
# entries = qsort(entries)

summations = [s_entries[0][1]]

maximum = s_entries[0][1]

# N
for i in range(1, len(s_entries)):
    summations += [summations[i - 1] + s_entries[i][1]]

    if summations[i] > maximum:
        maximum = summations[i]

# print(summations)

print(maximum)
