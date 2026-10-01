num = input("Enter numbers separeated by comma: ").split(",")
a = [int(i.strip()) for i in num]
print(a[1:len(a):2])