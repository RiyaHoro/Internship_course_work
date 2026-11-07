class Solution:
    def trap(self, height):
        left = 0
        right = len(height) - 1

        left_max = 0
        right_max = 0

        water = 0

        while left < right:

            if height[left] < height[right]:

                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    water += left_max - height[left]

                left += 1

            else:

                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    water += right_max - height[right]

                right -= 1

        return water


# Main program
if __name__ == "__main__":

    height1 = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    height2 = [4, 2, 0, 3, 2, 5]

    obj = Solution()

    print("Example 1:", obj.trap(height1))
    print("Example 2:", obj.trap(height2))