class node:
    def __init__(self,value):
        self.value = value
        self.next = None
    def display(self):
        curr = self
        while curr is not None:
            print(curr.value,end="->")
            curr = curr.next
        print(curr)
    def findMid(self):
        slow = self
        fast = self
        counter = 0
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            counter+=1
        return counter
    def deleteMid(self,mid):
        
        p1= head
        p2 = head
        for i in range(mid-1):
            p1 = p1.next
        p1.next = p1.
    
#test case 1
head = node(1)
head.next = node(2)
head.next.next = node(3)
head.next.next.next = node(4)
head.next.next.next.next = node(5)

head.display()
delN = node.findMid(head) + 1
print(delN)

