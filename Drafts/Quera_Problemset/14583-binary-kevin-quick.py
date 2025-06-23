s = input()
n = len(s)
c = 0

# Ones before
s1 = n * [0]
for i in range(0,n-1):
    s1[i+1] = s1[i] + int(s[i])

# Zeroes after
s0 = n * [0]
for i in range(n-2,-1,-1):
    s0[i] = s0[i+1] + (not int(s[i+1]) | 0)

for i in range(n):
    if s1[i] >=2 and s0[i]>=0:
        c = int(c % (10**9 +7))
        c += (s1[i])*(s1[i]-1)*(s0[i])/2

print(int(c % (10**9 +7)))
