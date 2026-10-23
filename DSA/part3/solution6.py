# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        current = head
        
        while current and current.next:
            if current.val == current.next.val:
                # Skip the duplicate node
                current.next = current.next.next
            else:
                # Move to the next distinct node
                current = current.next
                
        return head

# Helper functions to test the code
def list_to_linked_list(lst):
    dummy = ListNode(0)
    curr = dummy
    for val in lst:
        curr.next = ListNode(val)
        curr = curr.next
    return dummy.next

def linked_list_to_list(node):
    lst = []
    while node:
        lst.append(node.val)
        node = node.next
    return lst

if __name__ == "__main__":
    # Example 2: head = [1, 1, 2, 3, 3]
    head = list_to_linked_list([1, 1, 2, 3, 3])
    
    sol = Solution()
    result = sol.deleteDuplicates(head)
    print(linked_list_to_list(result))  # Output: [1, 2, 3]