#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
#
# @param head ListNode类
# @param n int整型
# @return ListNode类
#
#
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self , head: ListNode, n: int) -> ListNode:
        ori=ListNode(0,head)
        slow=fast=ori

        for _ in range(n+1):
            fast=fast.next

        while fast:
            fast=fast.next
            slow=slow.next

        slow.next=slow.next.next

        return ori.next
