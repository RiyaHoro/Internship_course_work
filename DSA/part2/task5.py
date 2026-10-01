class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    @classmethod
    def create_linked_list(cls, values):
        if not values:
            return None
        head = cls(values[0])
        curr = head
        for val in values[1:]:
            curr.next = cls(val)
            curr = curr.next
        return head

    def display(self):
        curr = self
        res = []
        while curr:
            res.append(str(curr.value))
            curr = curr.next
        print("".join(res))


def add_one_single_pass(head):
    if not head:
        return Node(1)

    # Dummy head to handle overflow cases like 999 -> 1000 seamlessly
    dummy = Node(0)
    dummy.next = head

    # Find the rightmost node that isn't 9
    last_not_nine = dummy
    curr = head

    while curr:
        if curr.value != 9:
            last_not_nine = curr
        curr = curr.next

    # Increment the last non-9 digit
    last_not_nine.value += 1

    # Change all trailing 9s to 0s
    curr = last_not_nine.next
    while curr:
        curr.value = 0
        curr = curr.next

    # If dummy value changed to 1 (e.g. 999 -> 1000), dummy is the new head
    return dummy if dummy.value == 1 else dummy.next


if __name__ == "__main__":
    test_cases = [1999, 3453, 9999]

    for num in test_cases:
        # Convert integer directly to linked list using map/str
        digits = [int(d) for d in str(num)]
        head = Node.create_linked_list(digits)

        print(f"Original: ", end="")
        head.display()

        head = add_one_single_pass(head)

        print(f"After +1:  ", end="")
        head.display()
        print("-" * 20)