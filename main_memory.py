
import time

class memory():
    
    def __init__(self, clock):
        self.mem = [["" for i in range(2)] for j in range(8)]
        self.clock = clock
    
    def __deco_dir(self, dir):
        row = dir[0:3]
        column = dir[3]
        row = int(row, 2)
        column = int(column,2)
        return [row, column]
    def read(self, dir):
        time.sleep(1.5*self.clock)
        d_dir = self.__deco_dir(dir)
        return self.mem[d_dir[0]][d_dir[1]]
    
    def write(self, dir, data):
        time.sleep(1.5*self.clock)
        d_dir = self.__deco_dir(dir)
        self.mem[d_dir[0]][d_dir[1]] = data

"""
m = memory(1)
m.write('1010', 'ABCD')
print(m.read('1010'))
"""