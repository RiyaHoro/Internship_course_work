class Solution:
    def __init__(self,nums):
        self.nums = nums
    def productExceptSelf(self):
        n = len(self)
        answer = [1] * n

        # Prefix products
        prefix = 1
        for i in range(n):
            answer[i] = prefix
            prefix *= self[i]

        # Suffix products
        suffix = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= suffix
            suffix *= self[i]

        return answer
a = [1,2,3,4]
print(Solution.productExceptSelf(a))
            