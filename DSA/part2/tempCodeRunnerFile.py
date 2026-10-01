    # --- Test Case 1 ---
    head1 = Node(2)
    head1.next = Node(3)
    head1.next.next = Node(4)
    head1.next.next.next = Node(5)

    head1.display()
    print("The middle element is", head1.get_middle())
    print()