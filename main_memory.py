
import time

class Memory():
    
    def __init__(self):
        self.mem = ['0000' for i in range(16)]

    def __deco_dir(self, dir):
        return int(dir, 2)

    def read(self, dir, clock):
        time.sleep(1.5*clock)
        d_dir = self.__deco_dir(dir)
        return self.mem[d_dir]
    
    def write(self, dir, data, clock):
        time.sleep(1.5*clock)
        d_dir = self.__deco_dir(dir)
        self.mem[d_dir] = data
"""
m = Memory()
m.write('1010', 'ABCD', 1)
print(m.read('1010', 1))
m.write('1111', 'FFFD', 1)
print(m.read('1111', 1))
"""