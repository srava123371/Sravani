p=1000
t=2
r=10
si=(p*t*r)/100
print("simple interest",si)
ci=p*(1+(r/100))**t-p
print(ci)
'''average'''
p=90
b=80
e=90
avg=(p+b+e)/3
print(avg)
'''swapping'''
a=10
b=20
a,b=b,a
print(a,b)
'''swapping another method'''
a=10
b=20
a=a+b
b=a-b
a=a-b
print(a,b)
'''user input'''
a=int(input())
b=int(input())
print(a+b)