class Node:
    def __init__(self,value):
        self.value = value
        self.next = None
    def createLinkedList(self):
        head = Node(self[0])
        curr = head
        for val in self[1:]:
            curr.next = Node(val)
            curr = curr.next
        return head
    def display(self):
        curr = self
        while curr is not None:
            print(curr.value,end="->")
            curr = curr.next
        print(curr)
    def reverse(self):
        prev = None
        curr = self
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev
            
if __name__ == "__main__":
    values = [1,2,3,4]
    head = Node.createLinkedList(values)
    head.display()
    newH = head.reverse()
    newH.display()
    #test case 2
    values2 = [1,2,3,4,5]
    head2 = Node.createLinkedList(values2)
    head2.display()
    newH1 = head2.reverse()
    newH1.display()
    
    
    