def main():
    m=int(input())
    left=1
    right=2
    s=3
    while right<m:
        while s<m:
            right+=1
            s+=right
        if s==m:
            print(f"{left} {right}")
        s-=left
        left+=1

if __name__=="__main__":
    main()