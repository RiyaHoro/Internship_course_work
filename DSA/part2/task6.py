class Node:
    """Standard Node class representation."""
    def __init__(self, data):
        self.data = data
        self.next = None


# Helper functions
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def print_list(head):
    curr = head
    elems = []
    while curr:
        elems.append(str(curr.data))
        curr = curr.next
    print(" -> ".join(elems) + " -> NULL")


# -------------------------------------------------------------------
# MAIN CORE FUNCTION (This is the primary deliverable tested)
# -------------------------------------------------------------------
def addTwoNumbers(l1: Node, l2: Node) -> Node:
    # Step 1: Reverse both lists so LSBs are at the front
    l1 = reverse_list(l1)
    l2 = reverse_list(l2)

    dummy_head = Node(0)
    curr = dummy_head
    carry = 0

    # Step 2: Add digits from right to left
    while l1 or l2 or carry:
        val1 = l1.data if l1 else 0
        val2 = l2.data if l2 else 0

        total = val1 + val2 + carry
        carry = total // 10
        curr.next = Node(total % 10)

        curr = curr.next
        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next

    # Step 3: Reverse result back to original order (MSD first)
    return reverse_list(dummy_head.next)



def create_linked_list(arr):
    if not arr:
        return None
    head = Node(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = Node(val)
        curr = curr.next
    return head


if __name__ == "__main__":
    # Test Case 1: 563 + 842 = 1405
    l1 = create_linked_list([5, 6, 3])
    l2 = create_linked_list([8, 4, 2])

    print("Input 1:")
    print_list(l1)
    print_list(l2)
    result1 = addTwoNumbers(l1, l2)
    print("Output 1:")
    print_list(result1)

    print("\n" + "=" * 30 + "\n")

    # Test Case 2: 75946 + 84 = 76030
    l3 = create_linked_list([7, 5, 9, 4, 6])
    l4 = create_linked_list([8, 4])

    print("Input 2:")
    print_list(l3)
    print_list(l4)
    result2 = addTwoNumbers(l3, l4)
    print("Output 2:")
    print_list(result2)