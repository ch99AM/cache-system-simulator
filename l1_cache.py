
import time
import numpy as np

class L1Cache():
    
    def __init__(self, clock):
        self.mem = [[[str(i+j*2), "I", "", "0000"] for i in range(2)] for j in range(2)]
        self.clock = clock

    def read(self, dir):
        if self.find_dir(dir):
            time.sleep(0.1*self.clock)
            set_m = int(dir[3], 2)
            for block in self.mem[set_m]:
                if dir == block[2]:
                    return block
        else:
            return "cache miss"
    
    # write-through
    # remplazo aleatorio
    def write(self, dir, state, data):
        set_m = int(dir[3], 2)
        block = np.random.randint(2)
        print("wirte to main memory and write miss")
        time.sleep(0.1*self.clock)
        self.mem[set_m][block][3] = data
        self.mem[set_m][block][1] = state
        self.mem[set_m][block][2] = dir

    def find_dir(self, dir):
        for block_m in self.mem[int(dir[3], 2)]:
            if dir == block_m[2] and block_m[1] != "I":
                return True
        return False




c = L1Cache(1)
c.write('0010', 'E', 'ABCD')
c.write('1101', 'E', 'FFFF')
print(c.read("0010"))
print(c.read("1101"))
print(c.read("0000"))
