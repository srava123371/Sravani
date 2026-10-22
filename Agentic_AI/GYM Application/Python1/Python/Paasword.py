password="Sravani@1234#"
for attempt in range(1,4):
    user=input()
    if user==password:
        print("Account successfully Login")
        break
    else:
        print("wrong password")
        if attempt==3:
            print("Account Locked")

    