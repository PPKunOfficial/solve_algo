# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        ori=ListNode(0,head) # 幽灵节点
        slow=fast=ori

        # 制造n+1差距
        for _ in range(n+1):
            fast=fast.next

        # fast遍历完之后，slow刚好停在待删除的前一个
        # 因为前面制造n+1差距，而fast在最后，slow则是倒数n+1
        while fast:
            fast=fast.next
            slow=slow.next

        # 直接跳过下一个，将当前的next设为下一个的next，即两个中间的没有被指向
        slow.next=slow.next.next

        return ori.next
