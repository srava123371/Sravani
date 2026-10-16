age=int(input())
if age>=18:
    print("allowed for match")
    if age>18 and age<=30:
        print("2$ for ticket")
    elif age>30 and age<=60:
        print("1$ for ticket")
    else:
        print("0$ ticket")
else:
    print("not allowed")