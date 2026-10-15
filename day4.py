'''cpu_hours=int(input("cpu_hours:"))
storage=int(input("storage:"))
data_transfer=int(input("data_transfer:"))
cpu_cost=cpu_hours*5
storage_cost=storage*2
data_transfer_cost=data_transfer*1
total_amount=cpu_cost+storage_cost+data_transfer_cost
if cpu_hours>100:
    print(total_amount+500)
else:
    print(total_amount)
'''
'''if elif elsecondition'''
uptime=float(input())
bill=int(input())
if uptime>=99.9:
    refund=0
elif uptime>=98:
    refund=bill*(10/100)
else:
    refund=bill*(25/100)
print(refund)