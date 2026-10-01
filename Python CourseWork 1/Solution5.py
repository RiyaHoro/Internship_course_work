a = 2
b = int(input("Enter any number: "))
sum= 0 
for i in range(b):
    sum+=a
    a = (a*10) + 2
print(sum)