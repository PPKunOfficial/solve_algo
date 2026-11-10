class ListNode:
    def __init__(self, x, next=None):
        self.val = x
        self.next: ListNode | None = next


class Solution:
    def EntryNodeOfLoop(self, pHead: ListNode):
        if not pHead or not pHead.next:
            return None

        slow, fast = pHead, pHead

        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

            if fast == slow:
                break
        else:
            return None

        fast = pHead
        while fast is not slow:
            fast = fast.next
            slow = slow.next

        return fast
