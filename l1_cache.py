
import time
import numpy as np

class L1Cache(object):
    
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
            return "CM"
    
    # write-through
    # remplazo aleatorio
    def write(self, dir, state, data):
        print("Hola")
        set_m = int(dir[3], 2)
        if self.find_dir(dir):
            print("Hol1")
            for i in range(len(self.mem[set_m])):
                if dir == self.mem[set_m][i][2]:
                    self.mem[set_m][i][3] = data
                    self.mem[set_m][i][1] = state
                    self.mem[set_m][i][2] = dir  
                    import bus
                    bus.write_mem(self.mem[set_m][i])            
        else: 
            print("Hol2")
            block = np.random.randint(2)
            self.mem[set_m][block][3] = data
            self.mem[set_m][block][1] = state
            self.mem[set_m][block][2] = dir            
            from bus import write_mem
            write_mem(self.mem[set_m][block])     
        time.sleep(0.1*self.clock)

    def find_dir(self, dir):
        for block_m in self.mem[int(dir[3], 2)]:
            if dir == block_m[2]:
                return True
        return False




c = L1Cache(1)
c.write('0010', 'E', 'ABCD')
c.write('1101', 'E', 'FFFF')
print(c.read("0010"))
print(c.read("1101"))
print(c.read("0000"))
