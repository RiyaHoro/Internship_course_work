class Solution:
    def maxSubArray(self, nums):

        current_sum = nums[0]
        max_sum = nums[0]

        for i in range(1, len(nums)):

            current_sum = max(nums[i], current_sum + nums[i])

            max_sum = max(max_sum, current_sum)

        return max_sum


# Main program
if __name__ == "__main__":

    nums1 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    nums2 = [1]
    nums3 = [5, 4, -1, 7, 8]

    obj = Solution()

    print("Example 1:", obj.maxSubArray(nums1))
    print("Example 2:", obj.maxSubArray(nums2))
    print("Example 3:", obj.maxSubArray(nums3))