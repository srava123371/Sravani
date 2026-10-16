w=float(input())
h=float(input())
bmi=w/(h)**2
if bmi<18.5:
    print("under weight")
elif bmi<25:
    print("normal")
elif bmi<30:
    print("over weight")
else:
    print("obese")


    

