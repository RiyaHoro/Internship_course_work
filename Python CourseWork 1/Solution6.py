a = int(input("Enter any num: "))
num = 0 
while a > 0:
    num = (num * 10)+(a % 10) 
    a = a // 10
print(num)