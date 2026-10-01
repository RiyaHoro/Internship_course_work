# Part A: Integer List Operations

nums = [1, 2, 3, 4, 5, 5, 7, 7]


# 1. Multiply all items
product = 1

for i in nums:
    product *= i

print("Product:", product)


# 2. Largest number
largest = max(nums)

print("Largest:", largest)


# 3. Smallest number
smallest = min(nums)

print("Smallest:", smallest)


# 4. Remove duplicates while preserving order
newList = []

for i in nums:
    if i not in newList:
        newList.append(i)

print("Without duplicates:", newList)


# 5. Check whether list is empty
if len(nums) == 0:
    print("List is empty")
else:
    print("List is not empty")


# 6. Find largest odd number
oddNumbers = []

for i in nums:
    if i % 2 != 0:
        oddNumbers.append(i)

if len(oddNumbers) == 0:
    print("No odd numbers found")
else:
    print("Largest odd number:", max(oddNumbers))


# 7. Remove elements at indexes 0, 4 and 5
# Remove from highest index to lowest index
# so that indexes do not shift incorrectly

indexes = [5, 4, 0]

for i in indexes:
    if i < len(nums):
        nums.pop(i)

print("After removing indexes:", nums)



# Part B: Tuple List Sorting

tupleList = [(1, 3), (2, 1), (4, 2)]

for i in range(len(tupleList)):
    for j in range(i + 1, len(tupleList)):

        if tupleList[i][-1] > tupleList[j][-1]:
            tupleList[i], tupleList[j] = tupleList[j], tupleList[i]

print("Sorted tuples:", tupleList)



# Part C: Word List Analysis

words = ["Hello", "python", "WORLD"]

lowercaseCount = 0

for word in words:
    for letter in word:
        if letter.islower():
            lowercaseCount += 1

print("Total lowercase letters:", lowercaseCount)



# Part D: Consecutive Element Extraction

nums = [1, 1, 3, 4, 4, 5, 6, 7]
k = 2

result = []

i = 0

while i < len(nums):

    current = nums[i]
    count = 1

    while i + count < len(nums) and nums[i + count] == current:
        count += 1

    if count == k:
        result.append(current)

    i += count

print("Elements appearing exactly", k, "times consecutively:", result)