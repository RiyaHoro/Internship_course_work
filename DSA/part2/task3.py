class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def display(self):
        curr = self

        while curr is not None:
            print(curr.value, end="->")
            curr = curr.next

        print("NULL")

    def removeDuplicates(self):
        curr = self

        while curr and curr.next:
            if curr.value == curr.next.value:
                curr.next = curr.next.next
            else:
                curr = curr.next

        return self


def create_linked_list(values):
    head = Node(values[0])
    curr = head

    for value in values[1:]:
        curr.next = Node(value)
        curr = curr.next

    return head


if __name__ == "__main__":

    # TEST CASE 1
    head = create_linked_list([11, 11, 11, 13, 13, 20])

    head.display()
    head.removeDuplicates()
    head.display()

    # TEST CASE 2
    head1 = create_linked_list(
        [10, 15, 15, 15, 20, 20, 20, 23, 25, 25]
    )

    head1.display()
    head1.removeDuplicates()
    head1.display()