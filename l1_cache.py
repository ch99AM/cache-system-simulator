
import time

class L1Cache():
    
    def __init__(self, clock):
        self.mem = [[[str(i+j*2), "I", "", "0000"] for i in range(2)] for j in range(2)]
        self.clock = clock
    
    def __deco_dir(self, dir):
        row = int(dir[3], 2)
        column = int(dir[0:3], 2)
        return [row, column%2]

    def read(self, dir):
        time.sleep(0.1*self.clock)
        d_dir = self.__deco_dir(dir)
        return self.mem[d_dir[0]][d_dir[1]]
    
    def write(self, dir, state, data):
        time.sleep(0.1*self.clock)
        d_dir = self.__deco_dir(dir)
        self.mem[d_dir[0]][d_dir[1]][3] = data
        self.mem[d_dir[0]][d_dir[1]][1] = state
        self.mem[d_dir[0]][d_dir[1]][2] = dir


"""
c = L1Cache(1)
c.write('0010', 'E', 'ABCD')
c.write('1101', 'E', 'FFFF')
print(c.read('0010'))
print(c.mem)

m.write('1010', 'ABCD')
print(m.read('1010'))
m.write('1111', 'FFFD')
print(m.read('1111'))
"""