password=input("enter your password:")
alpha=""
num=""
sp=""
for ch in password:
    if ch.isalpha():
        alpha=alpha+ch
    elif ch.isdigit():
        num=num+ch
    else:
        sp=sp+ch
if len(alpha)>=3 and len(sp)>=1 and len(num)>=2:
    print("password is valid")
else:
    print("password is invalid")