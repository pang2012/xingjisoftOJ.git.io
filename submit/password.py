string=list(input())

for i in range(0,len(string)-1,2):

    print(string[i+1],end="")

    print(string[i],end="")

if (len(string)%2==1):

    print(string[i+2])