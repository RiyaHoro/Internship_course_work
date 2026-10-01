#Read an integer N. For all non-negative integers i < N, print i^2 as a list.
a = int(input("Enter a non negative integer: "))
Square = []
for i in range(0,a):
    Square.append(i*i)
print(Square)
    
