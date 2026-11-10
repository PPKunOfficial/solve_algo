import sys

def main():
    n = int(input())
    boys = list(map(int, sys.stdin.readline().split()))
    m = int(input())
    girls = list(map(int, sys.stdin.readline().split()))

    boys.sort()
    girls.sort()
    i,j=0,0
    ans = 0

    while i<n and j<m:
        # 两个相差小，一起后退
        if abs(boys[i]-girls[j])<=1:
            ans+=1
            i+=1
            j+=1

        elif boys[i]<girls[j]: # 男的比女的差得多，就男的后退（男的选更强的）
            i+=1
        else: # 女的同理
            j+=1
    print(ans)


if __name__ == "__main__":
    main()
