total=float(input())
if total>=1000:
    discount=total*(10/100)
    final_amount=total-discount
    print(discount)
    print(final_amount)
else:
    print(total)