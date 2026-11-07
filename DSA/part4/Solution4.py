from collections import Counter

class node:
    def __init__(self,head,next = None):
        self.head = head
        self.next = None
    
    def display(self):
        curr = self
        while curr:
            print(curr.head,end = "->")
            curr = curr.next
        print(curr)
    
    def print_unique(value):
        freq = Counter()

        curr = value
        while curr:
            freq[curr.head] += 1
            curr = curr.next

        curr = value
        while curr:
            if freq[curr.head] == 1:
                print(curr.head, end=" ")
            curr = curr.next
if __name__ == "__main__":
    a = [1,2,1,3,2,5]
    head = node(a[0])
    curr = head
    for i in range(1,len(a)):
        curr.next = node(a[i])
        curr = curr.next
    head.display()
    
    head.print_unique()
    print("\n")
    nums = [-1,0] 
    head = node(nums[0])
    curr = head
    for i in range(1,len(nums)):
        curr.next = node(nums[i])
        curr = curr.next
    head.display()
    head.print_unique()
        
        
    
    