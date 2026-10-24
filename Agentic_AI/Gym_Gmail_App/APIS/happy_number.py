n=int(input("enter value:"))
while n!=1 and n!=4:
    total=0
    while n>0:
        digit=n%10
        total=total+digit**2
        n=n//10
    n=total
if n==1:
    print("happy number")
else:
    print("not happy number")



