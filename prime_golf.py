i=3;b=s=2
while i<1E6:
 x,y=b,i
 while x:x,y=y%x,x
 if y<2:b*=i;s+=i
 i+=2
print(s)
