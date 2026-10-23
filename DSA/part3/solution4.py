import heapq

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: list[ListNode]) -> ListNode:
        dummy = ListNode(0)
        curr = dummy
        heap = []
        
        # Use a counter as a unique tie-breaker to prevent comparing ListNode objects directly
        counter = 0
        for l in lists:
            if l:
                heapq.heappush(heap, (l.val, counter, l))
                counter += 1
                
        while heap:
            val, _, node = heapq.heappop(heap)
            curr.next = node
            curr = curr.next
            
            # If there is a next node, push it into the heap with a new unique counter
            if node.next:
                heapq.heappush(heap, (node.next.val, counter, node.next))
                counter += 1
                
        return dummy.next

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
    # Example with duplicates across and within lists
    lists = [
        list_to_linked_list([1, 4, 5]),
        list_to_linked_list([1, 3, 4]),
        list_to_linked_list([2, 6])
    ]
    
    sol = Solution()
    result = sol.mergeKLists(lists)
    print(linked_list_to_list(result))  # Output: [1, 1, 2, 3, 4, 4, 5, 6]