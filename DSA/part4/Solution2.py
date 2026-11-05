class Solution:
    def __init__(self,head,next=None):
        self.head = head
        self.next = None
    def display(self):
        curr = self
        while(curr != None):
            print(curr.head,end="->")
            curr = curr.next
        print(curr)
    def pairSum(self, head):
        slow = fast = head

        # Find middle
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Reverse second half
        prev = None
        curr = slow

        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        # Find maximum twin sum
        max_sum = 0
        first = head
        second = prev

        while second:
            max_sum = max(max_sum, first.head + second.head)
            first = first.next
            second = second.next

        return max_sum
    
if __name__ == "__main__":
    a = Solution(5)
    a.next = Solution(4)
    a.next.next = Solution(2)
    a.next.next.next = Solution(1)
    a.display()
    print(Solution.pairSum(a,a))
    