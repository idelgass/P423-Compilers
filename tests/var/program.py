i = 0
sum = 1
while i != 10:
    t = (sum, sum,)
    sum = (t[0] + t[1])
    i = (i + 1)
print((42 + (sum - sum)))