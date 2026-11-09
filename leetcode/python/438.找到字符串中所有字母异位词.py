# 这道题不用滑动窗口不行！
class Solution:
    def findAnagrams(self, s: str, p: str) -> list[int]:
        s_len, p_len = len(s), len(p)

        if s_len < p_len:
            return []

        ans = []
        p_count = [0] * 26
        s_count = [0] * 26

        for ch in p:
            p_count[ord(ch) - ord('a')] += 1

        for i in range(s_len):
            # 右边界扩张，新的加入窗口
            s_count[ord(s[i])-ord('a')]+=1

            # 左边界收缩，如果窗口超过p_len则把前面的去掉
            if i>=p_len:
                s_count[ord(s[i - p_len]) - ord('a')] -= 1

            if i >= p_len - 1 and s_count == p_count:
                    ans.append(i - p_len + 1)

        return ans


if __name__=="__main__":
    s=Solution()
    print(s.findAnagrams("bbbb","aaac"))
