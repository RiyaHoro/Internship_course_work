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
    a = int(input)
    
    
    
    
    
    