def successful_pairs(spells, potions, success):
    potions.sort()
    result = []

    for spell in spells:
        left = 0
        right = len(potions)

        while left < right:
            mid = (left + right) // 2

            if spell * potions[mid] >= success:
                right = mid
            else:
                left = mid + 1

        result.append(len(potions) - left)

    return result


if __name__ == "__main__":
    spells = [5, 1, 3]
    potions = [1, 2, 3, 4, 5]
    success = 7

    print(successful_pairs(spells, potions, success))