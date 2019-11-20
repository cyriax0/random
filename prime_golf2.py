s=0
for i in range(2,100):
 s+=i
 for j in range(2,i):
  if i%j==0:s-=i;break
print(s)
