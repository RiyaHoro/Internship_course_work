numbers = input("Enter numbers separateed by commas : ").split(",")
numbers = [int(num.strip()) for num in numbers]
result = []
for i in numbers:
    if i%5 == 0 & i< 500:
        if i > 150:
            continue
        result.append(i)
print(result)       