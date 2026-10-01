a = input("Enter any string: ")
vowels = "AEIOUaeiou"
vowel = 0
Consonants = 0
for ch in a:
    if ch in vowels:
        vowel += 1
    else:
        Consonants+=1
print(f"vowel={vowel}")
print(f"Consonants={Consonants}")