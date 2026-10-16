units=int(input())
if units<=100:
    bill=units*1
elif units<=200:
    bill=100*1+(units-100)*2
else:
    bill=100*1+100*2+(units-200)*5
print("electricity_Bill:",bill)