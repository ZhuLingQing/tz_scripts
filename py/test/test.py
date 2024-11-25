
class test:
    def __init__(self, seed):
        self.seed = seed
        
    def do_power(self, input):
        return list(map(test.power, input))
    
    @staticmethod
    def power(i):
        return i * i

t = test(5)
o = t.do_power(input=[1,2,3,4])
print(o)