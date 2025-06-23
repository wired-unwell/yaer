from re import match as find

n = int(input())

for i in range(n):
    phone_number = input()
    if find(r"^09\d{9}$", phone_number):
        print("+98" + phone_number[1:])
    elif find(r"^98\d{10}$", phone_number):
        print("+" + phone_number)
    elif find(r"^\+98\d{10}$", phone_number):
        print(phone_number)
    else:
        print("invalid")
    
