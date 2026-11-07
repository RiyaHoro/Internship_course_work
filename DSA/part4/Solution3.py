
class node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

    def display(self):
        curr = self
        while curr:
            print(curr.val, end="->")
            curr = curr.next
        print("None")

    @staticmethod
    def mergeTwoLists(list1, list2):
        if not list1:
            return list2

        if not list2:
            return list1

        if list1.val <= list2.val:
            list1.next = node.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = node.mergeTwoLists(list1, list2.next)
            return list2


if __name__ == "__main__":
    head = node(1)
    head.next = node(2)
    head.next.next = node(3)

    head2 = node(1)
    head2.next = node(3)
    head2.next.next = node(4)

    print("First list:")
    head.display()

    print("Second list:")
    head2.display()

    a = node.mergeTwoLists(head, head2)

    print("Merged list:")
    a.display()
