
import time

class Memory():
    
    def __init__(self, clock):
        self.mem = [[""] for i in range(16)]
        self.clock = clock
    
    def __deco_dir(self, dir):
        return int(dir, 2)

    def read(self, dir):
        time.sleep(1.5*self.clock)
        d_dir = self.__deco_dir(dir)
        return self.mem[d_dir]
    
    def write(self, dir, data):
        time.sleep(1.5*self.clock)
        d_dir = self.__deco_dir(dir)
        self.mem[d_dir] = data

"""
m = memory(1)
m.write('1010', 'ABCD')
print(m.read('1010'))
m.write('1111', 'FFFD')
print(m.read('1111'))
"""