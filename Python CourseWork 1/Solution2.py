a = input("Enter any string: ")
newString = ""
for ch in a:
    if not (ch in newString):
        newString = newString + ch
print(newString)