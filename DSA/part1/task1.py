def longest_subarray(arr, k):
    prefix_sum = 0
    max_length = 0

    # Store the first index where each prefix sum appears
    first_index = {0: -1}

    for i in range(len(arr)):
        prefix_sum += arr[i]

        # Check if there is a previous prefix sum
        # such that current_sum - previous_sum = k
        if prefix_sum - k in first_index:
            length = i - first_index[prefix_sum - k]
            max_length = max(max_length, length)

        # Store only the first occurrence
        if prefix_sum not in first_index:
            first_index[prefix_sum] = i

    return max_length


# Main
if __name__ == "__main__":
    arr = [10, 5, 2, 7, 1, -10]
    k = 15

    print(longest_subarray(arr, k))