a=int(input())
b=int(input())
c=int(input())
if a==b and b==c and c==a:
    print("Equailateral Traingle")
elif a==b or b==c or a==c:
    print("Isosceles Traingle")
else:
    print("Scalene Traingle")