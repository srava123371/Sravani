'''rama_h=1.3
raja_h=1.7
if rama_h>raja_h:
    print(rama_h)
else:
    print(raja_h)
    '''
total=float(input())
if total>=1000:
    discount=total*(10/100)
    final_amount=total-discount
    print(discount)
    print(final_amount)
else:
    print(total)