lt = {}
seq = eval(input(""))
for i in seq:
    lt[i] = lt.get(i,0) + 1
ret = list(lt.items())
#print("ret = {}".format(ret))
ret.sort(reverse = True, key = lambda x : x[1])
Num,n = ret[0]
print(Num)