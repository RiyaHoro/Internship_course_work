class Solution:
    def countConsistentStrings(self, allowed: str, words: list[str]) -> int:
        allowed_set = set(allowed)
        count = 0
        
        for word in words:
            # Check if all characters of the word are in the allowed set
            if all(char in allowed_set for char in word):
                count += 1
                
        return count

# --- Example Usage ---
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    allowed = "ab"
    words = ["ad", "bd", "aaab", "baa", "badab"]
    print(sol.countConsistentStrings(allowed, words))  # Output: 2
    
    # Example 2
    allowed = "abc"
    words = ["a", "b", "c", "ab", "ac", "bc", "abc"]
    print(sol.countConsistentStrings(allowed, words))  # Output: 7
    