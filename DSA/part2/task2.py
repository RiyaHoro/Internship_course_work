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
    def displayNew(self):
        curr = self
        while curr is not None:
            print(curr.value,end=" ")
            curr = curr.next
        print("\n")
    def deleteMid(self):
        slow = self
        fast = self
        prev = None
        while fast and fast.next :
            prev = slow
            slow = slow.next
            fast = fast.next.next
        prev.next = slow.next
        return self
if __name__=="__main__":   
    #test case 1
    head = node(1)
    head.next = node(2)
    head.next.next = node(3)
    head.next.next.next = node(4)
    head.next.next.next.next = node(5)

    head.display()
    DeleteMid = node.deleteMid(head)
    DeleteMid.displayNew()
    #test case 2
    head2 = node(2)
    head2.next = node(4)
    head2.next.next = node(6)
    head2.next.next.next = node(7)
    head2.next.next.next.next = node(5)
    head2.next.next.next.next.next = node(1)

    head2.display()
    newList = node.deleteMid(head2)
    newList.displayNew()
