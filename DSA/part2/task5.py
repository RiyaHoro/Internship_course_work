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
            print(curr.value,end="")
            curr = curr.next
        print("\n")
    def reverseL(self):
        prev = None
        curr = self
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev
    def add(self):
        curr = self
        head = curr
        curr.value = curr.value+1
        carry = 0
        if curr.value>9:
            carry = curr.value // 10
            curr.value = curr.value % 10
            curr = curr.next
        while curr is not None and carry >=1 :
            
            curr.value = curr.value+carry
            if curr.value>9:
                carry = curr.value // 10
                curr.value = curr.value % 10
            curr = curr.next
        return head
                
                
            
if __name__ == "__main__":
    a = 1999
    listA = []
    while a > 0:
        num = a % 10
        listA.append(num)
        a = a//10
    listA.reverse()
    #print(listA)       
    head = Node.createLinkedList(listA)

    head.display()
    #reverse the linked list first
    NewHead = head.reverseL()
   
    #Adding 1
    Add1 = NewHead.add()
    
    #Reversee the new linked list
    reverseAdd1 = Add1.reverseL()
    reverseAdd1.display()
    #test case 2
    a = 3453
    listA = []
    while a > 0:
        num = a % 10
        listA.append(num)
        a = a//10
    listA.reverse()
    #print(listA)       
    head = Node.createLinkedList(listA)

    head.display()
    #reverse the linked list first
    NewHead = head.reverseL()
   
    #Adding 1
    Add1 = NewHead.add()
    
    #Reversee the new linked list
    reverseAdd1 = Add1.reverseL()
    reverseAdd1.display()
   
    
    
    
    