s = input()
n = len(s)
MOD = 10**9 + 7

# Step 1: Build suffix array
zeros_after = [0] * (n + 1)
for i in range(n - 1, -1, -1):
    zeros_after[i] = zeros_after[i + 1] + (s[i] == '0')

# Step 2: Loop over i, j, k
count = 0
for i in range(n - 3):
    if s[i] != '1':
        continue
    for j in range(i + 1, n - 2):
        if s[j] != '1':
            continue
        for k in range(j + 1, n - 1):
            # Only (1,1,*,0) needed, so any s[k] is okay
            count += zeros_after[k + 1]

print(count % MOD)
