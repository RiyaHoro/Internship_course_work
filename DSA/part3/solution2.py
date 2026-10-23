class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        
        m = len(matrix)
        n = len(matrix[0])
        
        row = 0
        col = n - 1
        
        while row < m and col >= 0:
            current = matrix[row][col]
            
            if current == target:
                return True
            elif current > target:
                col -= 1  # Eliminate the current column
            else:
                row += 1  # Eliminate the current row
                
        return False

if __name__ == "__main__":
    matrix = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30]
    ]
    target = 5
    
    sol = Solution()
    print(sol.searchMatrix(matrix, target))  # Output: True
    matrix = [[1,4,7,11,15]
              ,[2,5,8,12,19]
              ,[3,6,9,16,22]
              ,[10,13,14,17,24]
              ,[18,21,23,26,30]]
    target = 20
    sol1 = Solution()
    print(sol.searchMatrix(matrix, target))