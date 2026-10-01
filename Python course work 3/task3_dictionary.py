# %%
'''Part A: Sorting a Dictionary by Value
Given a dictionary with numeric values: Sort the dictionary in ascending order and descending order by value. Display both results clearly.
'''
d = {0:23,1:4,3:45,5:-2,7:36}
values = list(d.values())
values.sort()

asc_d = {}
for value in values:
   for key in d.keys():
       if d[key] == value:
           asc_d[key] = value
print("Ascending order",asc_d)
values.sort(reverse=True)
dsc_d ={}
for value in values:
   for key in d.keys():
       if d[key] == value:
           dsc_d[key] = value
print("descending order:",dsc_d)


# %%
d.items()

# %%
''' Part B: Iterating Through a Dictionary
Demonstrate how to iterate through a dictionary using for loops:
Iterate over keys only.
Iterate over values only.
Iterate over key-value pairs. Display the results clearly.
'''

for key in d.keys():
    print(key,end=" ")
print("\n")
for value in d.values():
    print(value,end=" ")
print("\n")
for i in d.keys():
        print(i,d[i])
    
    

# %%
''' Part C: Merging Dictionaries
Merge two dictionaries into a single dictionary.'''

fruits = {'apple':'red','mango':"yellow","grapes":"green","peach":"pink"}
price ={'apple':100,1:200,2:300}
newD = fruits | price

print(newD)

# %%
''' Part D: Aggregation Operations
Calculate the sum of all numeric values in a dictionary.
Calculate the product (multiplication) of all numeric values in a dictionary.

Requirements:
1. Assume values are numeric.
2. Handle the case of an empty dictionary appropriately.'''
def dictOp(a):
    sum = 0
    mul = 1
    if len(a) == 0:
        return sum , mul
    else:
        for i in a.values():
            sum+=i
            mul*=i
    return sum,mul
d = {34:1,45:2,9:3,3:4}
d1 = {}
dictOp(d)





# %%
'''Part E: Sorting by Key
Sort a dictionary in ascending order by key. Display the sorted result clearly.'''
values = d.values()
keys = sorted(d.keys())
sorted_d = {}
for i in keys:
    sorted_d[i] = d[i]
print(sorted_d)

# %%

''' 
Part F: Removing Duplicates
Remove duplicate values from a dictionary.
Clarification:
Since dictionary keys must be unique, “duplicate” refers to duplicate values.
If multiple keys share the same value, keep only the first occurrence and remove the others.
Example:
Input: {'a': 10, 'b': 20, 'c': 10}
Output: {'a': 10, 'b': 20}'''

def removeDuplicates(d):
    newD={}
    values = d.values()
    for i in d.keys():
        if d[i] not in newD.values():
           newD[i] = d[i]
    print(newD)  
      
k = {'a': 10, 'b': 20, 'c': 10}
print(k)
removeDuplicates(k)

# %%



