# a lot of sort algorithm

class SortSet:
    def __init__(self):
        pass

    def bubble_while_with_flag(self, nums: list[int]):
        swapped: bool = True
        while (swapped):
            swapped = False
            for i in range(len(nums)-1):
                if nums[i] > nums[i+1]:
                    nums[i+1], nums[i] = nums[i], nums[i+1]
                    swapped = True

    def bubble_for(self, nums: list[int]):
        n = len(nums)
        for i in range(n-1):
            for j in range(n-1-i):
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]

    

sort = SortSet()
nums = [4, 5, 7, 1, 8]
sort.bubble_for(nums)
print(nums)
