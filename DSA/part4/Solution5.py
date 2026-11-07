class SparseVector:
    def __init__(self, nums):
        self.values = {}

        for i in range(len(nums)):
            if nums[i] != 0:
                self.values[i] = nums[i]

    def dotProduct(self, vec):
        result = 0

        for index in self.values:
            if index in vec.values:
                result += self.values[index] * vec.values[index]

        return result


nums1 = [1, 0, 0, 2, 3]
nums2 = [0, 3, 0, 4, 0]

v1 = SparseVector(nums1)
v2 = SparseVector(nums2)

print(v1.dotProduct(v2))  # 8