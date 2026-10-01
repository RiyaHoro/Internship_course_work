a = int(input("Input First number:"))
b = int(input("Input Second number:"))
c = int(input("Input Third number:"))
num = []
num.extend([a,b,c])
num.sort()

print("Output: ",num[len(num) // 2])