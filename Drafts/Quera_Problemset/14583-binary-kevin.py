s=input()
ls=len(s)
num=0
for i in range(ls-3):
    if s[i] == '1':
        for j in range(i+1,ls-2):
            if s[j] == '1':
                for l in range(j+2,ls):
                    if s[l] == '0':
                        num+=2
print(num % ((10**9)+7))
