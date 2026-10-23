class Solution:
    def removeDuplicates(self, s: str) -> str:
        stack = []
        for char in s:
            if stack and stack[-1] == char:
                stack.pop()  # Remove the duplicate pair
            else:
                stack.append(char)  # Add the character to the stack
                
        return "".join(stack)

# --- Example Usage ---
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    s1 = "abbaca"
    print(sol.removeDuplicates(s1))  # Output: "ca"
    
    # Example 2
    s2 = "azxxzy"
    print(sol.removeDuplicates(s2))  # Output: "ay"