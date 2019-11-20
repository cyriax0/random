

from fractions import gcd
def gcd_based():
    i=3
    smallnum=bignum = 2
    s = 2
    goal = 1000000
    while i < goal:
        if gcd(smallnum,i) == 1 and gcd(bignum,i) == 1:
            print("prime:",i)
            bignum *= i
            if bignum<60000:
                smallnum = bignum
            s += i
        i += 2
    print("Sum:",s)
    

class PrimarityTest:
    def __init__(self):
        self.primedata = [2]
        self.primesum = 2
    def test(self,x):
        for p in self.primedata:
            if gcd(p,x) > 1:
                return False
        self.append(x)
        return True
    def append(self,prime):
        self.primesum += prime
        if self.primedata[-1] * prime < 60000:
            self.primedata[-1] *= prime
        else:
            self.primedata.append(prime)

prime=PrimarityTest()

class Wheel:
    def __init__(self,size):
        assert size >= 0
        prime = PrimarityTest()
        module = 2
        self.wheel_start = [2]
        x = 2
        while size:
            x += 1
            #print(x)
            if prime.test(x):
                #print("prime",x)
                module *= x
                self.wheel_start.append(x)
                print("Found",x)
                size -= 1
                if size < 1: break
        #print("Module:",module)
        while x < module:
            x += 1
            #print(x)
            if prime.test(x):
                #print("prime",x)
                self.wheel_start.append(x)
        #wheel = list(range(module+1,module*2+1))
        gaps = []
        gap = 0
        start = 0
        #print("Start Gaps")
        while x < module*2:
            x+=1
            #print(x)
            gap += 1
            if prime.test(x):
                #print("Prime",x)
                if start == 0: start = x
                self.wheel_start.append(x)
                gaps.append(gap)
                gap=0
        if gap > 0:
            gaps.append(gap+gaps[0])
            gaps=gaps[1:]
        #print(gaps)
        self.gaps = gaps
        self.start = start+module
        self.cycle = len(gaps)
        self.prime = prime
        #print(self.wheel_start)
        #print("Start",self.start)

    def __iter__(self):
        for x in self.wheel_start:
            yield x
        i = 0
        x = self.start
        while True:
            if self.prime.test(x):
                yield x
            x += self.gaps[i]
            i += 1
            i %= self.cycle
    def limit(self,limit):
        for x in self:
            if x > limit: break
            yield x


import time
class PerformanceTimer:
    def __init__(self):
        self.inittime = time.clock()
        self.initwalltime = time.time()
        self.times = [["init", self.inittime]]
    def point(self, timepointname):
        self.times.append([timepointname, time.clock()])
    def report(self):
        oldtime = self.times[0]
        print("TIME",3,"--Time Report--")
        for timept in self.times[1:]:
            print("TIME",3,"{0:.4f}".format(timept[1] - oldtime[1])+ "s " + timept[0])
            oldtime = timept
        print("TIME",3,"{0:.4f}".format(self.times[-1][1] - self.inittime)+ "s TOTAL")
        print("TIME",3,"{0:.4f}".format(time.time() - self.initwalltime)+ "s WALLTIME")
        print("TIME",3,"--Time Report--")


timer = PerformanceTimer()
print(sum(Wheel(0).limit(10000)))
timer.point("Wheel 0")
print(sum(Wheel(1).limit(10000)))
timer.point("Wheel 1")
print(sum(Wheel(2).limit(10000)))
timer.point("Wheel 2")
print(sum(Wheel(3).limit(10000)))
timer.point("Wheel 3")
timer.report()




