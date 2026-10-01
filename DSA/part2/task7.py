class Node:
    """Represents a single node in a singly linked list."""

    def __init__(self, data):
        self.data = data
        self.next = None


def find_second_last(head: Node):
    """Finds and returns the value of the second last element in the linked list.

    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    # Edge Case: List is empty or has only 1 element
    if head is None or head.next is None:
        return None

    curr = head
    # Traverse until curr.next.next is None (meaning curr is at the second last node)
    while curr.next.next is not None:
        curr = curr.next

    return curr.data


def create_linked_list(arr):
    """Helper function to build a linked list from a Python list."""
    if not arr:
        return None
    head = Node(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = Node(val)
        curr = curr.next
    return head


if __name__ == "__main__":
    # Test Case 1
    list1 = create_linked_list([2, 4, 6, 8, 33, 67])
    print("Input 1: 2 -> 4 -> 6 -> 8 -> 33 -> 67 -> NULL")
    print("Output 1:", find_second_last(list1))  # Expected: 33

    print("-" * 35)

    # Test Case 2
    list2 = create_linked_list([1, 2, 3, 4, 5])
    print("Input 2: 1 -> 2 -> 3 -> 4 -> 5 -> NULL")
    print("Output 2:", find_second_last(list2))  # Expected: 4