def maximum_product_triplet(arr):
    arr.sort()
    n = len(arr)

    product1 = arr[n - 1] * arr[n - 2] * arr[n - 3]
    product2 = arr[0] * arr[1] * arr[n - 1]

    if product1 >= product2:
        return arr[n - 3], arr[n - 2], arr[n - 1]
    else:
        return arr[0], arr[1], arr[n - 1]


if __name__ == "__main__":
    arr = [-4, 1, -8, 9, 6]
    triplet = maximum_product_triplet(arr)
    print("The triplet having the maximum product is", triplet)