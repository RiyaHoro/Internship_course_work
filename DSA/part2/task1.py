class Node:

    def __init__(self, value):
        self.value = value
        self.next = None

    def display(self):
        """Prints the linked list from this node to the end."""
        curr = self
        while curr:
            print(curr.value, end=" -> ")
            curr = curr.next
        print("NULL")

    def get_length(self):
        """Calculates total node count."""
        count = 0
        curr = self
        while curr:
            count += 1
            curr = curr.next
        return count

    def get_middle(self):
        """Finds middle node using fast and slow pointers in one pass."""
        slow = self
        fast = self
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow.value

if __name__ == "__main__":
    # --- Test Case 1 ---
    head1 = Node(2)
    head1.next = Node(3)
    head1.next.next = Node(4)
    head1.next.next.next = Node(5)

    head1.display()
    print("The middle element is", head1.get_middle())
    print()

# --- Test Case 2 ---
head2 = Node(1)
head2.next = Node(2)
head2.next.next = Node(3)
head2.next.next.next = Node(4)
head2.next.next.next.next = Node(5)

head2.display()
print("The middle element is", head2.get_middle())