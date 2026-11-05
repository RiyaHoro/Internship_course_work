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
    
if __name__ == "__main__":
    a = Solution(2)
    a.next = Solution(3)
    a.next.next = Solution(4)
    a.next.next.next = Solution(5)
    a.display()
    ##Test case 1
    newHead = Solution(1)
    newHead.next = a
    newHead.display()
    ##Test case 2
    Head2 = Solution(9)
    
    
    