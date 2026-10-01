# %%
# Part A tuple creation and Access
#1 Create a tuple containing elements of different data types (e.g., integer, float, string, boolean).
tup = (1,"Apple",3.14,False)

#2. Create a tuple containing at least five numbers and Print one specific element (choose any valid index).
num = (3,56,1,67,89)

#3. Retrieve the 4th element from the end of a given tuple. If the tuple contains fewer than 4 elements, display an appropriate message. The program must not crash.
num1 =(12,3,4)
print(num[4])
try:
    print(num1[4])
except:
    print("less than 4 elements in the tuple")
    

# %%
#B.adding an element by concatenation 
num1 = num1 + (2,)
print(num1)

# %%
#Part C: Tuple Conversion

#5. Convert a tuple into a dictionary. If the tuple contains key-value pairs (e.g., ( ("a",1), ("b",2) )), convert directly. If the tuple is a simple sequence of values, convert it into a dictionary where: Keys are the index positions, Values are the tuple elements. The program must clearly handle one of the given approaches.

a = (1,2,45,6,23)
my_dict = {}
for i in range(len(a)):
    my_dict[i] = a[i]
print(my_dict)

# If the tuple already contains key value pairs
B =  ( ("a",1), ("b",2) )
c = dict(B)
print(c)
print(type(c))
    

# %%
#Part D: Tuple Transformation in a List
#6. Given a list of tuples: [(10, 20, 40), (40, 50, 60), (70, 80, 90)], Replace the last element of each tuple with 100.
#Expected Output: [(10, 20, 100), (40, 50, 100), (70, 80, 100)]

D =  [(10, 20, 40), (40, 50, 60), (70, 80, 90)]
print(D)
for i in range(len(D)):
    D[i] = list(D[i])
    D[i][2] = 100
    D[i] = tuple(D[i])
print(D)

# %%



